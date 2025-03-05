from agents.base_agent import BaseAgent
from config import Config
from skills.llm_skill import LLMSkill
from tools.web_search_tool import WebSearchTool  # Assurez-vous que l'outil est bien importé
from tools.web_cleaner_tool import WebCleanerTool  # Import du cleaner aussi

class RequestChercheurAgent(BaseAgent):
    def __init__(self, name="RequestChercheur", role=None, skills=None):
        super().__init__(name, role, skills)
        
        # Ajout du LLM
        if "LLMSkill" not in self.skills:
            self.add_skill(LLMSkill)

        # Instanciation des outils
        self.web_search_tool = WebSearchTool()
        self.web_cleaner_tool = WebCleanerTool()
    
    def query_ameliorator(self, search_criteria, research_reviewer_agent=None):
        """Améliore la requête avant exécution."""
        prompt = f"Tu es un spécialiste de la recherche d'information {self.role.context}. On t'a fait la demande suivante : {search_criteria}."
        
        if research_reviewer_agent and hasattr(research_reviewer_agent, "improved_criteria"):
            prompt += f"\nLe rewiever te propose d'utiliser {research_reviewer_agent.improved_criteria}. Tu peux le prendre en compte dans ta réflexion."
        
        prompt += "\nFormule une requête optimisée sous forme de mots-clés."

        Config.debug_log(f"🔍 [RequestChercheur] Amélioration de la requête : {search_criteria}")
        improved_query = self.execute_skill("LLMSkill", prompt)
        prompt =  f"A partir de tes réflexions et conclusions dont voici le contenu : {improved_query} ,écrit UNIQUEMENT le contenu à rentrer dans la barre de recherche du navigateur, sans rien ajouter ni commenter et sans utiliser d'apostrophes, d'accents ou de guillemets."
        improved_query = self.execute_skill("LLMSkill", prompt)
        return improved_query.strip()
    
    def execute_search(self, search_criteria, max_results=5, research_reviewer_agent=None):
        """Exécute la recherche améliorée et nettoie les résultats."""
        improved_query = self.query_ameliorator(search_criteria, research_reviewer_agent)
        Config.debug_log(f"🔍 [RequestChercheur] Requête améliorée : {improved_query}")

        if not hasattr(self, "web_search_tool"):
            Config.debug_log("⚠️ Aucun outil de recherche n'est disponible !")
            return None

        # 🔎 Exécution de la recherche web
        raw_results = self.web_search_tool.run(improved_query, max_results)
        Config.debug_log(f"🔎 [RequestChercheur] Résultats bruts : {raw_results}")

        # 🧹 Nettoyage des résultats
        cleaned_results = [self.web_cleaner_tool.run(result) for result in raw_results]
        Config.debug_log(f"🧹 [RequestChercheur] Résultats nettoyés : {cleaned_results}")

        return cleaned_results
