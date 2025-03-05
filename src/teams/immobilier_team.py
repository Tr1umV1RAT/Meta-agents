import argparse
import json
from teams.base_team import BaseTeam
from config import Config
from agents import RequestChercheurAgent, ResearchReviewerAgent, ArchivistAgent
from roles.AgentImmobilier import AgentImmobilierRole
from roles.AnalyseurAnnonceRole import ChercheurAnnonceRole
from roles.ArchivisteImmobilierRole import ArchivisteImmobilierRole
from utils.project_name_generator import ProjectNameGenerator

class TeamImmobilier(BaseTeam):
    """
    Équipe spécialisée dans la recherche et l'analyse d'annonces immobilières.
    """
    
    def __init__(self, name="TeamImmobilier", verbose=False, no_ai=False, n_round=1, search_criteria=""):
        self.context = "Recherche Immobilière"
        self.search_criteria = search_criteria
        self.project_name = ProjectNameGenerator.generate_project_name(self.context, self.search_criteria)
        
        super().__init__(self.project_name, [])
        self.verbose = verbose
        self.no_ai = no_ai
        self.n_round = n_round
        
        if self.verbose:
            Config.debug_log(f"🏡 Initialisation de {self.project_name}.")
        
        # Création des agents avec leurs rôles respectifs
        self.chercheur = RequestChercheurAgent(role=ChercheurAnnonceRole(name="Julien"))
        self.analyseur = ResearchReviewerAgent(role=AgentImmobilierRole())
        self.archiviste = ArchivistAgent(role=ArchivisteImmobilierRole(name="Jack"))
    
    def run_search(self):
        """Exécute un cycle de recherche d'annonces immobilières."""
        
        if self.verbose:
            Config.debug_log(f"🔍 Lancement de la recherche immobilière : {self.search_criteria}")
        
        for round_num in range(1, self.n_round + 1):
            if self.verbose:
                Config.debug_log(f"🔄 Round {round_num}/{self.n_round}")
            
            # Étape 1 : Recherche initiale
            raw_results = self.chercheur.query_ameliorator(self.search_criteria, self.analyseur)
            if self.verbose:
                Config.debug_log(f"📄 Résultats initiaux : {len(raw_results) if raw_results else 0} annonces trouvées.")
            
            # Étape 2 : Analyse et amélioration de la recherche
            improved_query = self.search_criteria
            if not self.no_ai:
                evaluated_results, improved_query = self.analyseur.perform(raw_results, self.search_criteria, self.search_criteria, None)
                if self.verbose:
                    Config.debug_log(f"✨ Nouvelle requête améliorée : {improved_query}")
            
            refined_results = self.chercheur.query_ameliorator(improved_query, self.analyseur)
            if self.verbose:
                Config.debug_log(f"📑 Résultats raffinés : {len(refined_results) if refined_results else 0} annonces trouvées.")
            
            # Étape 3 : Archivage des résultats
            self.archiviste.store_data("annonces_immobilier", refined_results)
            archivist_feedback = self.archiviste.analyze_results(refined_results, f"L'équipe de recherche immobilière cherche à répondre à {self.search_criteria}")
            if self.verbose:
                Config.debug_log(f"🗄️ Feedback de l'archiviste : {archivist_feedback}")
            
            # Étape 4 : Feedback et amélioration continue
            if not self.no_ai:
                self.analyseur.update_skill("ResearchEvaluatorSkill", archivist_feedback)
            
        if self.verbose:
            Config.debug_log(f"✅ Recherche immobilière terminée, feedback final : {archivist_feedback}")
        return refined_results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lancer une recherche immobilière avec l'équipe dédiée.")
    parser.add_argument("search_criteria", type=str, help="Critères de recherche entre crochets.")
    parser.add_argument("--no-ai", action="store_true", help="Désactive l'IA pour la recherche.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Active le mode debug.")
    parser.add_argument("--n_round", type=int, default=1, help="Nombre de rounds de recherche.")
    
    args = parser.parse_args()
    
    try:
        search_criteria = json.loads(args.search_criteria)
    except json.JSONDecodeError:
        search_criteria = args.search_criteria  # Gérer au cas où ce n'est pas un JSON
    
    team = TeamImmobilier(verbose=args.verbose, no_ai=args.no_ai, n_round=args.n_round, search_criteria=search_criteria)
    results = team.run_search()
    
    print("🔎 Résultats de la recherche :", results)
