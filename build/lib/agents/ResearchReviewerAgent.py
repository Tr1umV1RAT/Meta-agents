from config import Config
from agents.base_agent import BaseAgent
from skills.llm_skill import LLMSkill
from skills.memory_access import MemorySkill
from skills.communication import CommunicationSkill
from skills.research_evaluator_skill import ResearchEvaluatorSkill
from skills.prompt_ameliorator_skill import PromptAmelioratorSkill

class ResearchReviewerAgent(BaseAgent):
    """
    Agent spécialisé dans l'analyse et l'optimisation des résultats de recherche.
    Il peut être utilisé dans divers contextes nécessitant une évaluation des données récupérées.
    """
    
    def __init__(self, name="ResearchReviewer", role_description="Agent d'analyse des résultats de recherche", role=None):
        super().__init__(name, role)
        
        # Ajout des skills nécessaires
        
        self.add_skill(LLMSkill)
        self.add_skill(MemorySkill)
        self.add_skill(CommunicationSkill)
        self.add_skill(ResearchEvaluatorSkill)
        self.add_skill(PromptAmelioratorSkill)
        
    def evaluate_search_results(self, search_results, search_criteria, agent_context, use_top_results=False, use_ai=True):
        """
        Évalue la pertinence des résultats de recherche en fonction des critères définis.
        """
        return self.skills["ResearchEvaluatorSkill"].perform(search_results, search_criteria, agent_context, use_top_results, use_ai)
    
    def improve_search_prompt(self, search_results, original_query, search_criteria, agent_context, use_ai=True):
        """
        Propose une amélioration de la requête de recherche en fonction des résultats obtenus.
        """
        return self.skills["PromptAmelioratorSkill"].perform(search_results, original_query, search_criteria, agent_context, use_ai)
    
    def perform(self, search_results, original_query, search_criteria, agent_context):
        """
        Processus complet d'évaluation et d'amélioration d'une recherche.
        - Évalue les résultats existants.
        - Améliore la requête si nécessaire.
        """
        Config.debug_log("🔎 Début du processus de revue de recherche...")
        evaluated_results = self.evaluate_search_results(search_results, search_criteria, agent_context)
        improved_query = self.improve_search_prompt(search_results, original_query, search_criteria, agent_context)
        return evaluated_results, improved_query
