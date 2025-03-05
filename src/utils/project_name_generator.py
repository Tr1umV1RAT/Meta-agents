import os
import ollama
from config import Config

class ProjectNameGenerator:
    """
    Utilitaire pour générer un nom de projet basé sur le contexte et les paramètres de recherche.
    """

    def __init__(self, base_path="projects"):
        self.base_path = base_path
        self.ensure_base_directory()

    def ensure_base_directory(self):
        """Crée le dossier de base pour les projets s'il n'existe pas."""
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def generate_project_name(self, context, search_criteria=None):
        """
        Génère un nom de projet à partir du contexte et des critères de recherche.
        """
        prompt = (f"Vous êtes une IA chargée de générer des noms de projets pertinents. {context}\n"
                  f"Si applicable, voici les critères de recherche : {search_criteria}\n"
                  "Générez un nom de projet court et descriptif, sans texte supplémentaire.")
        
        project_name = Config.query_llm(prompt).strip().replace(" ", "_")
        return project_name

    def create_project_directory(self, project_name):
        """Crée un répertoire pour le projet et retourne son chemin."""
        project_path = os.path.join(self.base_path, project_name)
        os.makedirs(project_path, exist_ok=True)
        return project_path
