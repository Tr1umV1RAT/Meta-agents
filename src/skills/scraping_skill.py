import requests
from bs4 import BeautifulSoup
from config import Config
from .base_skill import BaseSkill

class ScrapingSkill(BaseSkill):
    """Skill permettant d'effectuer du scraping web et d'extraire le texte brut d'une page."""

    name = "scraping"

    def __init__(self, agent):
        super().__init__(agent)

    def perform(self, url, css_selector=None):
        """Scrape une page et extrait le texte pertinent.

        Args:
            url (str): L'URL de la page à scraper.
            css_selector (str, optional): Un sélecteur CSS pour extraire une partie spécifique.

        Returns:
            str: Texte brut extrait.
        """
        Config.debug_log(f"🌐 {self.agent.name} exécute ScrapingSkill sur {url} avec sélecteur: {css_selector}")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Vérifie si l'URL est valide

            soup = BeautifulSoup(response.text, "html.parser")

            if css_selector:
                elements = soup.select(css_selector)
                extracted_text = " ".join([el.get_text(strip=True) for el in elements])
            else:
                extracted_text = soup.get_text(separator=" ", strip=True)  # Récupération du texte brut

            Config.debug_log(f"✅ Scraping terminé, {len(extracted_text)} caractères extraits.")
            return extracted_text

        except requests.exceptions.RequestException as e:
            Config.debug_log(f"❌ Erreur lors du scraping de {url}: {str(e)}")
            return None
