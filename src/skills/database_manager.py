import sqlite3
from pathlib import Path
from abc import ABC, abstractmethod
from skills.base_skill import BaseSkill
from config import Config

class DatabaseManagerSkill(BaseSkill):
    def __init__(self, agent):
        super().__init__(agent)
        self.connection = None
        self.cursor = None

    def perform(self, action, *args, **kwargs):
        """Méthode principale pour exécuter une action sur la base de données."""
        actions = {
            "insert": self.insert,
            "query": self.query,
            "delete": self.delete,
            "update": self.update,
            "store_data": self.store_data,
            "retrieve_data": self.retrieve_data,
            "init": self.initialize_database  # Initialisation différée
        }

        if action in actions:
            return actions[action](*args, **kwargs)
        else:
            raise ValueError(f"Action '{action}' non reconnue. Actions disponibles: {list(actions.keys())}")

    def initialize_database(self, agent, db_path):
        """Crée ou adapte les tables selon les besoins évolutifs."""
        agent.log(f"🔧 Initialisation de la base de données: {db_path}")
        
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

        if self.use_ai and self.config:
            prompt = (
                "Ton objectif est de créer ou adapter les tables en fonction des nouvelles données disponibles. "
                "Réponds en respectant STRICTEMENT cette structure :\n"
                "TITRE:\n"
                "CREATE TABLE IF NOT EXISTS nom_table (\n"
                "    id INTEGER PRIMARY KEY AUTOINCREMENT,\n"
                "    colonne1 TYPE,\n"
                "    colonne2 TYPE\n"
                ");"
            )
            response = self.config.query_llm(prompt)
            self.cursor.execute(response)
        else:
            for table_name, table_query in self.table_definitions.items():
                self.cursor.execute(table_query)

        self.connection.commit()
        agent.log("✅ Base de données initialisée avec succès.")


    def insert(self, table, data):
        """Insère des données dans une table, avec adaptation si nécessaire."""
        try:
            print(type(data))
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in data])
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            self.cursor.execute(query, tuple(data.values()))
            self.connection.commit()
            return self.cursor.lastrowid
        except sqlite3.OperationalError:
            Config.debug_log(f"⚠️ Table {table} inexistante, tentative de création automatique.")
            self._initialize_database()
            return self.insert(table, data)

    def query(self, table, conditions=None):
        """Récupère des données d'une table avec conditions optionnelles."""
        query = f"SELECT * FROM {table}"
        if conditions:
            query += " WHERE " + ' AND '.join([f"{k}=?" for k in conditions.keys()])
        self.cursor.execute(query, tuple(conditions.values()) if conditions else ())
        return self.cursor.fetchall()

    def delete(self, table, conditions):
        """Supprime des entrées d'une table selon des conditions."""
        query = f"DELETE FROM {table} WHERE " + ' AND '.join([f"{k}=?" for k in conditions.keys()])
        self.cursor.execute(query, tuple(conditions.values()))
        self.connection.commit()

    def update(self, table, data, conditions):
        """Met à jour des données dans une table selon des conditions."""
        set_clause = ', '.join([f"{k}=?" for k in data.keys()])
        where_clause = ' AND '.join([f"{k}=?" for k in conditions.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        self.cursor.execute(query, tuple(data.values()) + tuple(conditions.values()))
        self.connection.commit()

    def store_data(self, key, value, use_memory_threshold=256):
        """Choisit dynamiquement où stocker les données (mémoire ou base)."""
        if len(value) <= use_memory_threshold:
            Config.update_memory(self.agent.name, key, value)
            Config.debug_log(f"🧠 {self.agent.name} a stocké {key} en mémoire.")
        else:
            self.insert("long_term_storage", {"key": key, "value": value})
            Config.debug_log(f"💾 {self.agent.name} a stocké {key} en base de données.")

    def retrieve_data(self, key):
        """Récupère une donnée en priorisant la mémoire puis la base de données."""
        value = Config.retrieve_memory(self.agent.name, key)
        if value:
            return value
        else:
            result = self.query("long_term_storage", {"key": key})
            return result[0][1] if result else None


    def close(self):
        """Ferme la connexion à la base de données."""
        self.connection.close()
