from config import Config  # ✅ Import de la configuration

class BaseEnvironment:
    def __init__(self, name, rules=None):
        self.name = name
        self.rules = rules if rules else {}

    def enforce_rules(self, action):
        """Vérifie si une action respecte les règles de l’environnement"""
        if action in self.rules:
            result = self.rules[action]()
            Config.debug_log(f"🌍 Règle appliquée sur {action} : {result}")
            return result
        
        Config.debug_log(f"✅ Aucune règle spécifique pour {action}, action autorisée.")
        return True  # ✅ Action autorisée par défaut
