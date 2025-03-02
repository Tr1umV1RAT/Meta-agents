from config import Config
from tools.base_tool import BaseTool
import requests
from bs4 import BeautifulSoup

class WebSearchTool(BaseTool):
    def __init__(self, name="WebSearchTool", num_results=10):
        super().__init__(name)
        self.num_results = num_results  # Nombre de résultats modifiable par rôle

    def run(self, query):
        return self.search(query)

    def search(self, query):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        url = f"https://www.google.com/search?q={query}&num={self.num_results}"
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            links = []
            for g in soup.find_all("div", class_="tF2Cxc"):
                link = g.find("a")["href"]
                if "google.com" not in link:  # Filtre les liens internes
                    links.append(link)
                if len(links) >= self.num_results:
                    break
            
            Config.debug_log(f"🔍 [WebSearchTool] Recherche '{query}' - {len(links)} résultats trouvés")
            return links
        
        except requests.RequestException as e:
            Config.debug_log(f"⚠️ [WebSearchTool] Erreur lors de la recherche: {e}")
            return []
