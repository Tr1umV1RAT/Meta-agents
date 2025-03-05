from environments.base_env import BaseEnvironment
from config import Config  # Pour le logging

class DebateEnvironment:
    """Gère l'échange entre les agents dans un débat."""

    def __init__(self, agents, rounds=3):
        self.agents = agents
        self.rounds = rounds

    def start(self, topic):
        """Lance le débat sur un nombre défini de rounds."""
        print(f"🎙️ Début du débat sur : {topic}")

        for round_num in range(1, self.rounds + 1):
            print(f"\n🔄 Round {round_num}/{self.rounds}\n")
            for i in range(0, len(self.agents), 2):  # Paires d'agents
                if i + 1 < len(self.agents):  # Vérifie qu'on a un adversaire
                    agent1, agent2 = self.agents[i], self.agents[i + 1]
                    response1 = agent1.debate(topic, agent2)
                    response2 = agent2.debate(topic, agent1)

                    print(f"🎙️ {agent1.name}: {response1}")
                    print(f"🎙️ {agent2.name}: {response2}")
