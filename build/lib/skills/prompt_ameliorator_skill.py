from abc import ABC, abstractmethod
from config import Config
from skills.base_skill import BaseSkill

class PromptAmelioratorSkill(BaseSkill):
    """Skill permettant d'améliorer le prompt de recherche en fonction des résultats obtenus."""
    
    def __init__(self, agent):
        super().__init__(agent)
    
    def perform(self, search_results, original_query, search_criteria, agent_context, use_ai=True):
        """
        Analyse les résultats obtenus et propose une amélioration du prompt de recherche.
        
        :param search_results: Liste des résultats récupérés.
        :param original_query: La requête de recherche initiale.
        :param search_criteria: Critères de recherche sous forme de texte.
        :param agent_context: Contexte de l'agent (définissant ses priorités).
        :param use_ai: Si True, utilise l'IA pour générer un meilleur prompt.
        :return: Une version améliorée de la requête de recherche, à envoyer au chercheur d'annonces.
        """
        if not search_results:
            Config.debug_log("🔍 Aucun résultat trouvé. Modification de la recherche nécessaire.")
            return self.modify_query(original_query, search_criteria)
        
        if use_ai:
            prompt = f"""
            {agent_context}
            Ton objectif est d'améliorer la requête de recherche pour obtenir des résultats plus pertinents.
            
            ---- Requête initiale ----
            {original_query}

            ---- Critères de recherche ----
            {search_criteria}

            ---- Résultats obtenus ----
            {search_results}

            ---- Instructions ----
            - Analyse les résultats et leur pertinence par rapport aux critères de recherche.
            - Si les résultats sont satisfaisants, renvoie exactement la même requête.
            - Si certains critères sont mal représentés, ajuste la requête pour mieux les inclure.
            - Si les résultats sont trop éloignés des critères, propose une nouvelle requête plus précise.
            - La réponse doit contenir **uniquement** la requête optimisée qui sera envoyée au chercheur d'annonces.
            """
            
            Config.debug_log("🤖 Génération d'une requête optimisée via l'IA...")
            response = Config.query_llm(prompt)
            print("🔍 query_ameliorator OUTPUT:", repr(response))

            print("🔍 Résultats bruts de query_ameliorator :", type(response), response[:3])
            return response.strip()
        
        return original_query  # Retour de la requête initiale si l'IA n'est pas utilisée.
    
    def modify_query(self, original_query, search_criteria):
        """Améliore basiquement la requête en ajoutant des précisions des critères de recherche."""
        Config.debug_log("✍️ Génération d'une requête améliorée sans IA.")
        return f"{original_query} {search_criteria}"
