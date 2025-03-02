import ollama

class Config:
    DEBUG_MODE = True
    LLM_MODEL = "llama3"
    LLM_SETTINGS = {
        "temperature": 0.7,
        "max_tokens": 512,
        "top_p": 0.9,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "ollama_host": "http://localhost:11434",  # URL du serveur Ollama
    }

    MEMORY = {}  # Stockage centralisé de la mémoire partagée

    @staticmethod
    def query_llm(prompt):
        """Effectue une requête au LLM via Ollama"""
        response = ollama.chat(model=Config.LLM_MODEL, messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"]

    @staticmethod
    def update_memory(agent_name, key, value):
        """Met à jour la mémoire partagée pour un agent spécifique"""
        if agent_name not in Config.MEMORY:
            Config.MEMORY[agent_name] = {}
        Config.MEMORY[agent_name][key] = value

    @staticmethod
    def retrieve_memory(agent_name, key):
        """Récupère un élément de la mémoire partagée"""
        return Config.MEMORY.get(agent_name, {}).get(key, None)
    DEBUG_MODE = True  # Passe à False en production

    @staticmethod
    def debug_log(message: str):
        """Affiche les logs uniquement si DEBUG_MODE est activé."""
        if Config.DEBUG_MODE:
            print(message)