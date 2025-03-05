import re
from config import Config
from tools.base_tool import BaseTool  # Vérifie que BaseTool existe bien dans ton projet


class ExtractKeyInfoTool(BaseTool):
    """Outil pour extraire des informations clés d'un texte via regex ou LLM."""
    
    def __init__(self):
        super().__init__("extract_key_info")
        self.name = "extractor"
    def run(self, text, patterns=None, use_llm=False, memory_key=None):
        """
        Extrait les informations clés d'un texte selon des patterns fournis.
        
        :param text: Texte à analyser.
        :param patterns: Dictionnaire de patterns regex.
        :param use_llm: Si True, utilise l'IA en complément.
        :param memory_key: Clé pour stocker les résultats en mémoire.
        :return: Dictionnaire des données extraites.
        """
        Config.debug_log(f"🔍 Extraction d'infos depuis un texte avec {len(patterns) if patterns else 'aucun'} patterns")

        extracted_data = {}

        # Extraction avec regex
        if patterns:
            for pattern_name, pattern in patterns.items():
                matches = re.findall(pattern, text)
                extracted_data[pattern_name] = matches

        # Optionnel : Envoi à l'IA si besoin
        if use_llm:
            prompt = f"Extrait les informations suivantes : {list(patterns.keys())} du texte suivant :\n{text}"
            llm_response = Config.query_llm(prompt)
            extracted_data["llm_analysis"] = llm_response

        # Stockage en mémoire si nécessaire
        if memory_key:
            Config.update_memory("extract_key_info", memory_key, extracted_data)

        Config.debug_log(f"📊 Résultat : {extracted_data}")
        return extracted_data
