from skills.base_skill import BaseSkill
from config import Config

class CommunicationSkill(BaseSkill):
    """Skill permettant la communication entre agents, avec un humain ou avec le LLM."""

    def send_to_agent(self, recipient, message):
        """Envoie un message à un autre agent."""
        if "CommunicationSkill" in recipient.skills:
            Config.debug_log(f"📢 {self.agent.name} dit à {recipient.name} : {message}")
            recipient.execute_skill("CommunicationSkill", "receive_message", message)
        else:
            Config.debug_log(f"⚠️ {recipient.name} ne peut pas recevoir de messages (pas de CommunicationSkill)")

    def broadcast(self, agents, message):
        """Envoie un message à plusieurs agents."""
        Config.debug_log(f"📣 {self.agent.name} envoie à toute l’équipe : {message}")
        for agent in agents:
            self.send_to_agent(agent, message)

    def talk_to_llm(self, prompt):
        """Dialogue avec le modèle LLM."""
        Config.debug_log(f"🗨️ {self.agent.name} parle au LLM...")
        return Config.query_llm(prompt)

    def receive_message(self, message):
        """Réception d'un message (placeholder, peut être personnalisé par agent)."""
        Config.debug_log(f"📨 {self.agent.name} a reçu : {message}")

    def perform(self, mode, *args, **kwargs):
        """Exécute le bon mode de communication."""
        actions = {
            "agent": self.send_to_agent,
            "broadcast": self.broadcast,
            "llm": self.talk_to_llm,
            "receive_message": self.receive_message,
        }
        if mode in actions:
            return actions[mode](*args, **kwargs)
        else:
            Config.debug_log(f"⚠️ Mode de communication inconnu : {mode}")
