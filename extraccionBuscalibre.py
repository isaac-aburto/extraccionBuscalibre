import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

# URL de la lista :)
url = 'https://www.buscalibre.cl/v2/carro-de-compras-guardado_1936492_l.html'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Nombre del archivo CSV que guardaremos
filename = 'libros.csv'

# Verifico si el archivo CSV existe y cargar los IDs existentes
if os.path.exists(filename):
    existing_data = pd.read_csv(filename, delimiter=';')
    libros_ids = {titulo: id_libro for titulo, id_libro in zip(existing_data['Título'], existing_data['ID'])}
    ultimo_id = max(libros_ids.values())
else:
    libros_ids = {}
    ultimo_id = 0
    existing_data = pd.DataFrame(columns=['ID', 'Título', 'Link'])

# GET
response = requests.get(url, headers=headers)
if response.status_code == 200:

    # Obtener el contenido HTML
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')

    productos = soup.find_all(class_='seccionProducto')

    ids = []
    titulos = []
    links = []
    precios = []

    fecha_actual = datetime.now().strftime('%Y-%m-%d')

    # Recorrer cada producto y extraer la información
    for producto in productos:
        titulo_div = producto.find(class_='titulo')
        titulo = titulo_div.text.strip()
        enlace = titulo_div.find('a')['href'] if titulo_div.find('a') else 'No disponible'
        
        precio_div = producto.find(class_='precioAhora')
        precio = precio_div.text.strip() if precio_div else '$ 0'

        # Asigación de ids
        if titulo not in libros_ids:
            ultimo_id += 1
            libros_ids[titulo] = ultimo_id
        id_libro = libros_ids[titulo]

        ids.append(id_libro)
        titulos.append(titulo)
        links.append(enlace)
        precios.append(precio)

    # Creo un df con la info (debería hacerlo de otra forma?)
    new_data = pd.DataFrame({
        'ID': ids,
        'Título': titulos,
        'Link': links,
        fecha_actual: precios
    })

    # Si existe un archivo CSV, combinar datos existentes con los nuevos
    if not existing_data.empty:
        combined_data = pd.merge(existing_data, new_data, on=['ID', 'Título', 'Link'], how='outer')

        # Agregar columnas faltantes en combined_data con $ 0
        # Lo siguiente me ha ayudado GPT:
        for column in combined_data.columns:
            if column not in ['ID', 'Título', 'Link'] and column not in new_data.columns:
                combined_data[column] = combined_data[column].fillna('$ 0')

        # Agregar las nuevas fechas que no estaban en existing_data
        new_dates = [col for col in new_data.columns if col not in existing_data.columns]
        for date in new_dates:
            combined_data[date] = combined_data[date].fillna('$ 0')
    else:
        combined_data = new_data

    # Ordenar las columnas para que las fechas estén al final
    non_date_columns = ['ID', 'Título', 'Link']
    date_columns = sorted([col for col in combined_data.columns if col not in non_date_columns])
    combined_data = combined_data[non_date_columns + date_columns]

    # Guardardo los datos
    combined_data.to_csv(filename, index=False, sep=';', encoding='utf-8-sig')

    print(f'Datos guardados en {filename}')
else:
    print(f'Error al obtener la página web: {response.status_code}')
