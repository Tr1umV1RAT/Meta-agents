from agents.base_agent import BaseAgent
from skills.communication import CommunicationSkill
from skills.memory_access import MemorySkill
from skills.llm_skill import LLMSkill
from skills.database_manager import DatabaseManagerSkill
from config import Config
import json
class ArchivistAgent(BaseAgent):
    def __init__(self, role, name = "ArchivistAgent",  db_name="database.sqlite"):
        
        super().__init__(name, role, skills=[CommunicationSkill, MemorySkill, LLMSkill, DatabaseManagerSkill])
        self.db_name = db_name  # Stocke le nom de la DB
        self.name = "ArchivistAgent"
    def init_database(self):
        """Initialise explicitement la base de données avec le nom spécifié."""
        self.execute_skill("DatabaseManagerSkill", "init", self, self.db_name)
    context = "L'équipe de recherche cherche à répondre à {search_criteria}"
    
    
    def analyze_results(self, results, context):
        """Analyse une liste de résultats et génère une remarque contextuelle."""
        if not results:
            return "Aucune donnée pertinente trouvée."
        
        Config.debug_log(f"🔍 {self.name} analyse {len(results)} résultats...")
        summary_prompt = f"Contexte: {context}\nNombre de résultats: {len(results)}\n"
        summary_prompt += "Exemples:\n" + "\n".join(str(result) for result in results[:3])
        summary_prompt += "\nFournis un résumé concis et pertinent."
        
        summary = Config.query_llm(summary_prompt)
        return summary or "Analyse indisponible."
    
    def store_data(self, table_name, data):
        """Stocke des données dans une table spécifique et en mémoire."""
        if isinstance(data, str):
                 try:
                          data = json.loads(data)  # Convertir en liste de dictionnaires
                 except json.JSONDecodeError:
                          raise ValueError("❌ Impossible de convertir 'data' en JSON.")
        Config.debug_log(f"💾 {self.name} insère des données dans {table_name}...")
        self.execute_skill("DatabaseManagerSkill", "insert", table_name, data)
        self.execute_skill("MemorySkill", "store", table_name, data)
    
    def query_data(self, table, conditions=None):
        """Effectue une requête SQL générique et stocke les résultats."""
        Config.debug_log(f"📊 {self.name} exécute une requête SQL sur {table}...")
        results = self.execute_skill("DatabaseManagerSkill", "query", table, conditions)
        self.execute_skill("MemorySkill", "store", "last_query_results", results)
        return results
    
    def retrieve_memory(self, key):
        """Récupère une information en mémoire persistante ou en base de données si nécessaire."""
        value = self.execute_skill("MemorySkill", "retrieve", key)
        if value:
            return value
        return self.execute_skill("DatabaseManagerSkill", "retrieve_data", key)
    
    def communicate(self, recipient, message):
        """Envoie un message à un autre agent."""
        self.execute_skill("CommunicationSkill", "send_to_agent", recipient, message)
