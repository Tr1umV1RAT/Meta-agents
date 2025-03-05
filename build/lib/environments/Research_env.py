from environments.base_env import BaseEnvironment
from config import Config
from agents import RequestChercheurAgent, ResearchReviewerAgent, ArchivistAgent

class ResearchEnvironment(BaseEnvironment):
    """
    Environnement de recherche orchestrant les interactions entre RequestChercheurAgent, ResearchReviewerAgent et ArchivistAgent.
    """
    
    def __init__(self, name="ResearchEnv", agents=None):
        super().__init__(name, agents)
        Config.debug_log(f"🔧 Initialisation de l'environnement {name} avec {len(agents) if agents else 0} agents.")
    
    def run_research(self, search_criteria):
        """Lance le cycle de recherche avec un critère donné."""
        
        Config.debug_log(f"🚀 Lancement de la recherche sur : {search_criteria}")
        research_agent = RequestChercheurAgent()
        research_reviewer = ResearchReviewerAgent()
        archivist = ArchivistAgent()
        
        if not research_agent or not research_reviewer or not archivist:
            Config.debug_log("❌ Erreur : Agents nécessaires non trouvés dans l'environnement.")
            raise ValueError("L'environnement nécessite RequestChercheurAgent, ResearchReviewerAgent et ArchivistAgent")
        
        # Étape 1 : Recherche initiale
        Config.debug_log("🔍 Début de la recherche initiale...")
        raw_results = research_agent.query_ameliorator(search_criteria, research_reviewer)
        Config.debug_log(f"📄 Résultats initiaux : {len(raw_results) if raw_results else 0} éléments trouvés.")
        
        # Étape 2 : Amélioration et évaluation de la recherche
        Config.debug_log("🔎 Début du processus de revue de recherche...")
        evaluated_results, improved_query = research_reviewer.process_search_review(raw_results, search_criteria, search_criteria, None)
        Config.debug_log(f"✨ Nouveau critère de recherche : {improved_query}")
        
        refined_results = research_agent.query_ameliorator(improved_query, research_reviewer)
        Config.debug_log(f"📑 Résultats raffinés : {len(refined_results) if refined_results else 0} éléments trouvés.")
        
        # Étape 3 : Archivage des résultats
        Config.debug_log("💾 Archivage des résultats...")
        archivist.store_data("research_results", refined_results)
        archivist_feedback = archivist.analyze_results(refined_results, f"L'équipe de recherche cherche à répondre à {search_criteria}")
        Config.debug_log(f"🗄️ Feedback de l'archiviste : {archivist_feedback}")
        
        # Étape 4 : Feedback et amélioration continue
        Config.debug_log("🔄 Mise à jour du ResearchEvaluatorSkill avec le feedback de l'archiviste...")
        research_reviewer.update_skill("ResearchEvaluatorSkill", archivist_feedback)
        
        Config.debug_log(f"✅ Recherche terminée, feedback final : {archivist_feedback}")
        return refined_results
