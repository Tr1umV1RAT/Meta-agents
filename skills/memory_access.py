from config import Config
from skills.base_skill import BaseSkill

class MemorySkill(BaseSkill):
    """Permet à l'agent d'accéder à la mémoire partagée."""

    def perform(self, action: str, *args, **kwargs):
        """Choisit l’action mémoire en fonction de la commande reçue."""
        actions = {
            "store": self.store_memory,
            "retrieve": self.retrieve_memory,
            "forget": self.forget_memory
        }
        if action in actions:
            return actions[action](*args, **kwargs)
        else:
            Config.debug_log(f"❌ Action mémoire inconnue : {action}")

    def store_memory(self, key: str, value: str):
        """Stocke une donnée en mémoire."""
        Config.update_memory(self.agent.name, key, value)
        Config.debug_log(f"🧠 {self.agent.name} a mémorisé {key} : {value}")

    def retrieve_memory(self, key: str):
        """Récupère une donnée en mémoire."""
        value = Config.retrieve_memory(self.agent.name, key)
        if value is None:
            Config.debug_log(f"⚠️ {self.agent.name} n'a aucune mémoire pour {key}")
        else:
            Config.debug_log(f"🔍 {self.agent.name} récupère {key} : {value}")
        return value

    def forget_memory(self, key: str):
        """Efface une mémoire spécifique uniquement si elle existe."""
        if Config.retrieve_memory(self.agent.name, key) is not None:
            Config.update_memory(self.agent.name, key, None)
            Config.debug_log(f"🚮 {self.agent.name} a oublié {key}")
        else:
            Config.debug_log(f"⚠️ {self.agent.name} ne pouvait pas oublier {key} (non existant)")
