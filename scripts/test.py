# Import du package complet

import os
import sys
sys.path.append("c:/Users/quent/ProjetMETAagents")

from config import Config
from tools.extractor_key_info import ExtractKeyInfoTool


# Instanciation
extractor = ExtractKeyInfoTool()

# Texte à analyser
text = "Jean Dupont a acheté 3 pommes pour 5.50€ le 12 février 2024."

# Patterns d'extraction
patterns = {
    "nom": r"\b[A-Z][a-z]+ [A-Z][a-z]+\b",
    "quantité": r"\b\d+ pommes\b",
    "prix": r"\b\d+\.\d{2}€\b",
    "date": r"\d{1,2} [a-zéû]+ \d{4}"
}

# Exécution
resultats = extractor.run(text, patterns, use_llm=False, memory_key="achat")

# Affichage
print(resultats)
