# SureBets
Surebets_Script




from selenium import webdriver
Importa la clase webdriver del módulo selenium. Esta clase proporciona todas las funcionalidades para controlar un navegador web de forma programática.



from selenium.webdriver.chrome.service import Service
Importa la clase Service del módulo selenium.webdriver.chrome.service. Esta clase proporciona la configuración del servicio del controlador del navegador.



from selenium.webdriver.common.by import By
Importa la clase By del módulo selenium.webdriver.common.by. Esta clase se utiliza para seleccionar elementos de la página web según varios criterios (por ejemplo, por clase, por etiqueta, por ID, etc.).



from selenium.webdriver.support.ui import WebDriverWait
Importa la clase WebDriverWait del módulo selenium.webdriver.support.ui. Esta clase proporciona funciones para esperar hasta que ciertas condiciones se cumplan antes de continuar la ejecución del script.



from selenium.webdriver.support import expected_conditions as EC
Importa el módulo expected_conditions del paquete selenium.webdriver.support y lo renombra como EC. Este módulo contiene una colección de condiciones que se pueden utilizar con WebDriverWait para esperar ciertos estados o comportamientos de la página.



from selenium.common.exceptions import NoSuchElementException
Importa la excepción NoSuchElementException del módulo selenium.common.exceptions. Esta excepción se utiliza para manejar casos en los que no se encuentra un elemento en la página web.



from bs4 import BeautifulSoup
Importa la clase BeautifulSoup del módulo bs4. Esta clase se utiliza para analizar documentos HTML y extraer información de ellos de manera más fácil y eficiente que con métodos tradicionales.



service = Service('PYTHON\WebScraping\chromedriver-win64\chromedriver.exe')
service.start()
Configura y arranca el servicio del controlador de Chrome (chromedriver). Esto es necesario para iniciar una instancia del navegador Chrome controlada programáticamente.



driver = webdriver.Chrome(service=service)
Inicia una instancia del navegador Chrome utilizando el servicio configurado anteriormente.



driver.get("https://apuestas.wplay.co/es")
Abre la página web especificada en la URL proporcionada (https://apuestas.wplay.co/es) en el navegador Chrome.



wait = WebDriverWait(driver, 10)
Crea una instancia de WebDriverWait que esperará un máximo de 10 segundos para que se cumplan las condiciones especificadas en las próximas operaciones.



pager_items = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "pager-item")))
Utiliza WebDriverWait para esperar a que todos los elementos con la clase "pager-item" estén presentes en la página. Retorna una lista de elementos que coinciden con el criterio de búsqueda especificado.



def print_event_details(team_a, team_b, time, date, odds):
    ...
Define una función llamada print_event_details que toma los detalles del evento (equipos, hora, fecha y cuotas) como argumentos e imprime estos detalles en la consola.



def print_event_statistics(statistics):
    ...
Define una función llamada print_event_statistics que toma las estadísticas del evento como argumento e imprime estas estadísticas en la consola.



eventos = []
Crea una lista vacía llamada eventos para almacenar los eventos.



for pager_item in pager_items:
    try:
        ...
    except NoSuchElementException:
        continue
Inicia un bucle for que recorre cada elemento de pager_items (que son elementos con la clase "pager-item"). Dentro del bucle, se intentará extraer información de cada elemento, y si se produce una excepción NoSuchElementException, el bucle pasará al siguiente elemento.



event_info = pager_item.find_element(By.CLASS_NAME, "inline-scoreboard")
Busca un elemento con la clase "inline-scoreboard" dentro del elemento actual del bucle for (pager_item). Este elemento contiene información sobre el evento, como la fecha, la hora y el enlace al evento.


date = event_info.find_element(By.CLASS_NAME, "date").text
time = event_info.find_element(By.CLASS_NAME, "time").text
Extrae el texto que representa la fecha y la hora del evento, encontrándolos dentro del elemento event_info.


event_link = event_info.find_element(By.TAG_NAME, "a")
event_link.click()
Encuentra y hace clic en el enlace (<a>) dentro del elemento event_info, lo que lleva a la página del evento.


stats = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "stat")))
Utiliza WebDriverWait para esperar a que todos los elementos con la clase "stat" estén presentes en la página del evento. Retorna una lista de elementos que coinciden con el criterio de búsqueda especificado.


statistics = []
for stat in stats:
    statistics.append(stat)
Crea una lista llamada statistics y la llena con los elementos encontrados que representan las estadísticas del evento.


soup = BeautifulSoup(driver.page_source, 'html.parser')
teams = soup.find_all('span', class_='seln-name')
odds = soup.find_all('span', class_='dec')
Utiliza BeautifulSoup para analizar el código fuente de la página del evento y extraer información sobre los nombres de los equipos y las cuotas de apuesta.


team_a = teams[0].text.strip()
team_b = teams[1].text.strip()
Extrae el nombre del primer y segundo equipo de la lista teams, eliminando cualquier espacio en blanco al principio o al final del texto.


print_event_details(team_a, team_b, time, date, [odd.text.strip() for odd in odds])
Llama a la función print_event_details para imprimir los detalles del evento (equipos, hora, fecha y cuotas) en la consola.


print_event_statistics(statistics)
Llama a la función print_event_statistics para imprimir las estadísticas del evento en la consola.


driver.back()
Navega de vuelta a la página anterior en el historial del navegador, lo que en este caso sería la página principal de apuestas.


driver.quit()
Cierra el navegador Chrome después de que se haya completado el bucle y se haya procesado toda la información de los eventos.