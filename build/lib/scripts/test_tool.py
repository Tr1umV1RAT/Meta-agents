from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Configurer Selenium avec un mode headless (sans affichage)
options = Options()
options.add_argument("--headless")  # Mode sans fenêtre
options.add_argument("--disable-blink-features=AutomationControlled")  # Pour éviter la détection bot
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Lancer Selenium
service = Service("C:/Users/quent/ZAP/webdriver/windows64/chromedriver.exe")  # Remplace par le chemin de ton ChromeDriver
driver = webdriver.Chrome(service=service, options=options)

# Aller sur la page
url = "https://www.seloger.com/immobilier/achat/immo-paris-75/bien-appartement/type-3-pieces/"
driver.get(url)

# Attendre le chargement
time.sleep(3)

# Récupérer tout le texte visible
page_content = driver.find_element(By.TAG_NAME, "body").text

# Afficher un extrait
print("🔍 PAGE RÉCUPÉRÉE AVEC SELENIUM !")
print(page_content[:2000])

# Fermer le navigateur
driver.quit()