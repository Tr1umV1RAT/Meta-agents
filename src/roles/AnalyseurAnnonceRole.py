from config import Config 
from tools.web_search_tool import WebSearchTool
from tools.web_cleaner_tool import WebCleanerTool
from roles.base_role import BaseRole

class ChercheurAnnonceRole(BaseRole):
    name = "Jean"
    tools = [WebSearchTool(), WebCleanerTool()]
    description = "Tu es un expert en recherche d'annonces immobilières. Ton objectif est de trouver des annonces correspondant aux critères fournis. Tu dois utiliser des outils spécialisés pour extraire et nettoyer les résultats."

    context = (
        "Tu es un expert en recherche d'annonces immobilières. Ton objectif est de trouver des annonces correspondant aux critères fournis. "
        "Tu dois utiliser des outils spécialisés pour extraire et nettoyer les résultats."
    )

    def rechercher_annonces(self, query, max_results=10):
        """Effectue une recherche d'annonces immobilières avec les outils disponibles."""
        
        Config.debug_log(f"🔍 Recherche d'annonces avec la requête: {query}")
        
        if "WebSearchTool" in [tool.__class__.__name__ for tool in self.tools]:
            search_results = self.use_tool("WebSearchTool", query, max_results)
        else:
            Config.debug_log("❌ WebSearchTool non disponible dans ce rôle.")
            return []

        if "WebCleanerTool" in [tool.__class__.__name__ for tool in self.tools]:
            cleaned_pages = []
            for result in search_results:
                cleaned_content = self.use_tool("WebCleanerTool", result["link"])
                cleaned_pages.append({"url": result["link"], "content": cleaned_content})
        else:
            Config.debug_log("⚠️ WebCleanerTool non disponible. Résultats non nettoyés.")
            cleaned_pages = search_results

        return {"query": query, "results": cleaned_pages}
