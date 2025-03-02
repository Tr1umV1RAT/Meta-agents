from teams.base_team import BaseTeam
from environments.debate_env import DebateEnvironment
from config import Config  # Pour le logging

class DebateTeam:
    def __init__(self, agents, environment, rounds=5):
        self.agents = agents
        self.environment = environment
        self.rounds = rounds  # Nombre de rounds configuré

    def start_debate(self, topic):
        """Lance un débat en plusieurs rounds."""
        argument = None  # Premier argument non défini

        for round_number in range(1, self.rounds + 1):
            print(f"\n🎙️ **Round {round_number}/{self.rounds}**")

            for i in range(len(self.agents)):
                speaker = self.agents[i]
                opponent = self.agents[(i + 1) % len(self.agents)]  # Tourne entre les agents
                
                argument = speaker.execute_skill("debate", topic, opponent.name, argument)
                print(f"🗣️ {speaker.name} : {argument}")

                if argument is None:
                    print(f"❌ {speaker.name} n’a pas pu répondre.")
                    return
