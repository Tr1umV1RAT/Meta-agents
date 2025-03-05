from config import Config  # Pour les logs

class BaseTool:
    def __init__(self, name):
        self.name = name

    def run(self, *args, **kwargs):
        """Méthode à implémenter dans les outils spécifiques"""
        Config.debug_log(f"🛠️ [BaseTool] L'outil {self.name} a été utilisé avec {args}, {kwargs}")
        raise NotImplementedError("La méthode 'run' doit être implémentée dans les sous-classes.")
