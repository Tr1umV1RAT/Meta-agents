class Memory:
    """Mémoire centrale pouvant être partagée entre plusieurs agents."""
    
    def __init__(self):
        self.global_memory = []
    
    def store(self, info):
        """Ajoute une information à la mémoire globale."""
        self.global_memory.append(info)
    
    def retrieve(self, n=5):
        """Récupère les dernières informations mémorisées."""
        return self.global_memory[-n:]