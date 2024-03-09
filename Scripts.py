from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

# Configura el servicio de ChromeDriver
service = Service('PYTHON\WebScraping\chromedriver-win64\chromedriver.exe')
service.start()

# Inicia una instancia del navegador Chrome
driver = webdriver.Chrome(service=service)

# Abre la página web
driver.get("https://apuestas.wplay.co/es")

# Espera a que aparezcan los elementos pager-item
wait = WebDriverWait(driver, 10)
pager_items = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "pager-item")))

# Función para imprimir los detalles del evento
def print_event_details(team_a, team_b, time, date, odds):
    print("Evento:", team_a, "vs", team_b)
    print("Hora:", time)
    print("Fecha:", date)
    print("Equipo A:", team_a)
    print("Cuota A:", odds[0])
    print("Empate (cuota):", odds[1])    
    if len(odds) >= 3:  # Verificar si hay al menos 3 elementos en la lista
        print("Equipo B:", team_b)
        print("Cuota B:", odds[2])
        print("-------------------------------")
    else:
        print("Cuota B no disponible")  # Mensaje alternativo si no hay cuota B

# Lista para almacenar los eventos
eventos = []

# Recorre cada "pager-item"
for pager_item in pager_items:
    try:
        # Extracción de fecha y hora del evento
        event_info = pager_item.find_element(By.CLASS_NAME, "inline-scoreboard")
        date = event_info.find_element(By.CLASS_NAME, "date").text
        time = event_info.find_element(By.CLASS_NAME, "time").text

        # Extraer el HTML interno del pager-item
        html = pager_item.get_attribute('innerHTML')

        # Parsear el HTML interno
        soup = BeautifulSoup(html, 'html.parser')

        # Encontrar los nombres de los equipos y sus cuotas
        teams = soup.find_all('span', class_='seln-name')
        odds = soup.find_all('span', class_='dec')

        # Crear un diccionario para el evento actual
        evento_actual = {
            "Equipo A": teams[0].text.strip(),
            "Equipo B": teams[1].text.strip(),
            "Hora": time,
            "Fecha": date,
            "Cuota A": odds[0].text.strip(),
            "Cuota Empate": odds[1].text.strip(),
        }

        # Verificar si hay cuota para el Equipo B
        if len(odds) >= 3:
            evento_actual["Cuota B"] = odds[2].text.strip()

        # Agregar el diccionario del evento a la lista de eventos
        eventos.append(evento_actual)

    except NoSuchElementException:
        # Si no se encuentra la sección de mercados, pasar al siguiente pager-item
        continue

# Cierra el navegador
driver.quit()

# Imprimir la lista de eventos almacenados
print(eventos)