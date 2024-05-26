from bs4 import BeautifulSoup
import requests

def get_student_data_by_url(url:str):
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using Beautiful Soup
        soup = BeautifulSoup(response.text, 'html.parser')

        data = {}
        image = soup.find_all('img')
        
        data['image'] = image[1].get('src')
    for row in soup.find_all('tr'):
        key, value = [item.strip() for item in row.text.split(':')]
        if key == 'Nombre':
            data['first_name'], data['middle_name'], data['last_name'] = parse_full_name(value)
        elif key == 'Carrera':
            data['career'] = value
        elif key == 'Número de Control':
            data['control_number'] = value
    
    return data
        
def parse_full_name(full_name):
    names = full_name.split()
    first_name = names[0]
    middle_name = names[1] if len(names) > 2 else ""
    last_name = names[2] if len(names) > 2 else names[1]
    return first_name, middle_name, last_name