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

# Función para imprimir detalles del evento
def print_event_details(team_a, team_b, time, date, odds):
    print("Evento:", team_a, "vs", team_b)
    print("Hora:", time)
    print("Fecha:", date)
    print("Equipo A:", team_a)
    print("Cuota A:", odds[0])
    print("Empate (cuota):", odds[1])
    print("Equipo B:", team_b)
    print("Cuota B:", odds[2])
    print("--------------------")

# Recorre cada "pager-item"
for pager_item in pager_items:
    try:
        # Extraer fecha y hora del evento
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

        # Imprimir los detalles del evento
        print_event_details(teams[0].text.strip(), teams[1].text.strip(), time, date, [odd.text.strip() for odd in odds])

    except NoSuchElementException:
        print("No se pudo encontrar la sección de mercados.")

# Cierre del navegador
driver.quit()

# Preguntar al usuario sobre el equipo para ver estadísticas
equipo_buscar = input("Ingrese el nombre del equipo para ver sus estadísticas: ")

# Recorre cada "pager-item" nuevamente para buscar el equipo específico
for pager_item in pager_items:
    try:
        # Extraer el HTML interno del pager-item
        html = pager_item.get_attribute('innerHTML')

        # Parsear el HTML interno
        soup = BeautifulSoup(html, 'html.parser')

        # Encontrar los nombres de los equipos
        teams = soup.find_all('span', class_='seln-name')

        # Verificar si el equipo buscado está en el evento
        if equipo_buscar.lower() in [team.text.strip().lower() for team in teams]:
            # Extraer fecha y hora del evento
            event_info = pager_item.find_element(By.CLASS_NAME, "inline-scoreboard")
            date = event_info.find_element(By.CLASS_NAME, "date").text
            time = event_info.find_element(By.CLASS_NAME, "time").text

            # Encontrar los nombres de los equipos y sus cuotas
            odds = soup.find_all('span', class_='dec')

            # Imprimir los detalles del evento específico
            print_event_details(teams[0].text.strip(), teams[1].text.strip(), time, date, [odd.text.strip() for odd in odds])

    except NoSuchElementException:
        print("No se pudo encontrar la sección de mercados.")
