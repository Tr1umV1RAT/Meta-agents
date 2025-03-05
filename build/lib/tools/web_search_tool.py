from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
from config import Config  # Gestion des logs
from tools.base_tool import BaseTool  # Classe de base pour les outils
from bs4 import BeautifulSoup
import requests

class WebSearchTool(BaseTool):
    def __init__(self, name="GoogleScraper"):
        super().__init__(name)

    def setup_driver(self, headless=True):
        """ Initialise le driver Selenium avec des options optimisées """
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1280,800")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def fetch_page_content(self, url):
        """ Télécharge le contenu HTML d'une page cible """
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException:
            return None

    def extract_content(self, html):
        """ Extrait le titre et une description d'une page cible """
        if not html:
            return None
        
        soup = BeautifulSoup(html, "html.parser")
        
        # Titre de la page
        title = soup.title.text if soup.title else "Titre non trouvé"
        
        # Description via la meta description
        description = ""
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and "content" in meta_desc.attrs:
            description = meta_desc["content"]

        # Si pas de meta description, prendre le premier paragraphe significatif
        if not description:
            paragraphs = soup.find_all("p")
            if paragraphs:
                description = paragraphs[0].text.strip()

        return {
            "title": title,
            "description": description
        }

    def run(self, query, max_results=5, headless=True):
        """ Exécute une recherche Google et récupère les résultats enrichis """
        driver = self.setup_driver(headless)
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}&num={max_results}"
        driver.get(url)
        
        time.sleep(random.uniform(2, 5))  # Pause aléatoire pour éviter les blocages
        
        results = []
        search_results = driver.find_elements(By.CSS_SELECTOR, "div.tF2Cxc")

        for result in search_results[:max_results]:
            try:
                title = result.find_element(By.TAG_NAME, "h3").text
                link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
                description = result.find_element(By.CSS_SELECTOR, "div.VwiC3b").text

                # Scraper la page de destination pour un contenu détaillé
                html = self.fetch_page_content(link)
                page_data = self.extract_content(html) if html else {}

                results.append({
                    "title": page_data.get("title", title),
                    "link": link,
                    "description": description,
                    "content": page_data.get("description", "Contenu non trouvé"),
                })
            except Exception:
                pass

        driver.quit()
        return results
