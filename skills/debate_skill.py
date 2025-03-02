from .base_skill import BaseSkill
from config import Config

class DebateSkill(BaseSkill):
    """Skill permettant de générer des arguments en fonction du rôle et du contexte."""
    name = "debate"

    def __init__(self, agent):
        super().__init__(agent)
        
    def perform(self, topic, opponent_name):
        """Génère une réponse argumentée dans un débat."""
        
        prompt = f"""
Tu es {self.agent.name}, un {self.agent.role.name}.
Tu débats avec {opponent_name} sur le sujet : {topic}.

Réponds directement à {opponent_name} en défendant ta position :
{self.agent.role.description}

🧠 Ton raisonnement est influencé par ces biais : {', '.join(self.agent.role.cognitive_biases)}
"""
        return self.agent.execute_skill("llm", prompt)
