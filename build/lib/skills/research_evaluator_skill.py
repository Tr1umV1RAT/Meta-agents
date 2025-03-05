from abc import ABC, abstractmethod
from config import Config
from skills.base_skill import BaseSkill
import re
from fuzzywuzzy import fuzz  # Pour une meilleure correspondance floue

class ResearchEvaluatorSkill(BaseSkill):
    """Skill d'évaluation des résultats de recherche en fonction des critères définis."""
    
    def __init__(self, agent):
        super().__init__(agent)
    
    def perform(self, search_results, search_criteria, agent_context, use_top_results=False, use_ai=True):
        """Évalue et trie les résultats de recherche en fonction des critères donnés."""
        if not search_results:
            Config.debug_log("🔍 Aucun résultat de recherche à évaluer.")
            return []

        if use_top_results:
            Config.debug_log("⚠️ Filtrage par mots-clés activé.")
            search_results = self.filter_by_keywords(search_results, search_criteria)

        if use_ai:
            prompt = f"""
            {agent_context}
            Ton objectif est d'évaluer et classer les résultats suivants en fonction des critères donnés et de tes objectifs comme agent.

            ---- Critères de recherche ----
            {search_criteria}

            ---- Résultats de recherche ----
            {search_results}

            ---- Instructions ----
            - Analyse chaque résultat en fonction des critères et attentes de l'agent.
            - Classe-les du plus pertinent au moins pertinent.
            - Retourne une liste JSON correcte contenant les résultats triés.
            """

            Config.debug_log("🤖 Envoi des résultats à l'IA pour évaluation...")
            try:
                response = Config.query_llm(prompt)
                if isinstance(response, str):
                    response = response.strip()
                    if response.startswith("[") and response.endswith("]"):
                        import json
                        response = json.loads(response)
                elif not isinstance(response, list):
                    response = [response]  # Fallback si l'IA renvoie un texte brut
                
                return response  # Liste des résultats classés
            except Exception as e:
                Config.debug_log(f"⚠️ Erreur lors de l'analyse IA: {e}")
                return search_results  # Retour des résultats bruts en cas d'erreur

        return search_results  # Retour brut si l'IA n'est pas utilisée

    def filter_by_keywords(self, search_results, search_criteria):
        """Filtrage basé sur des mots-clés et une correspondance floue."""
        keywords = re.findall(r'\b\w+\b', search_criteria.lower())
        filtered_results = []
        for result in search_results:
            score = sum(fuzz.partial_ratio(word, result.lower()) for word in keywords) / len(keywords)
            if score > 70:  # Seuil de pertinence
                filtered_results.append(result)
        return filtered_results
