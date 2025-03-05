from .base_agent import BaseAgent
from skills.llm_skill import LLMSkill
from skills.debate_skill import DebateSkill
from config import Config
class DebatorAgent(BaseAgent):
    """Un agent spécialisé dans les débats."""

    def __init__(self, name, role):
        super().__init__(name, role)
        self.add_skill(LLMSkill)  # ✅ Passer la classe et non l'instance
        self.add_skill(DebateSkill)
        Config.debug_log(f"📜 Compétences de {self.name}: {list(self.skills.keys())}")

    def debate(self, topic, opponent):
        """Engage un échange avec un adversaire sur un sujet donné."""
        response = self.execute_skill("debate", topic=topic, opponent_name=opponent.name)
        return response
