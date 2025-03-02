from .base_skill import BaseSkill
from config import Config  # 🔥 Import direct de la config existante

class LLMSkill(BaseSkill):
    name = "llm"

    def __init__(self, agent):
        super().__init__(agent)

    def perform(self, prompt, **kwargs):
        """Envoie une requête au LLM configuré dans `Config`."""
        Config.debug_log(f"🤖 {self.agent.name} interroge le LLM avec : {prompt}")

        try:
            response = Config.query_llm(prompt, **kwargs)
            if not response or not isinstance(response, str):
                raise ValueError("Réponse LLM invalide")
            
            Config.debug_log(f"📨 Réponse du LLM : {response}")
            return response
        
        except Exception as e:
            Config.debug_log(f"❌ Erreur lors de la requête LLM : {e}")
            return None  # Pour éviter les crashs et permettre une gestion propre
