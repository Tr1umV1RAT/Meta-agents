from abc import ABC, abstractmethod

class BaseSkill(ABC):
    """Classe de base pour tous les skills."""
    
    def __init__(self, agent):
        self.agent = agent  # L’agent qui possède ce skill
    
    @abstractmethod
    def perform(self, *args, **kwargs):
        """Méthode principale à implémenter par chaque skill."""
        pass
