# Buscalibre Script

Este script extrae información de precios de libros desde una página web específica y guarda los datos en un archivo CSV. Cada vez que se ejecuta, el script añade nuevas entradas y actualiza las existentes, manteniendo un registro histórico de los precios.

¡Las listas deben ser públicas!

## Requisitos

- Python 3.x
- Bibliotecas:
  - requests
  - BeautifulSoup4
  - pandas

Puedes instalar las bibliotecas necesarias utilizando `pip`:

```bash
pip install requests beautifulsoup4 pandas
```
## Uso

Ejecuta el siguiente comando desde una terminal:
```
python main_bb.py
```
## Estructura CSV:
```
ID;Título;Link;YYYY-MM-DD;...
1;Nombre del libro;https://linkdelibro.com;$ 10.000;$ 0;...
2;Otro libro;https://linkdelibro.com;$ 15.000;$ 0;...
```
## Notas

Si la página web cambia su estructura, puede que sea necesario actualizar el script para adaptarse a los nuevos selectores HTML.
Asegúrate de tener una conexión a Internet estable al ejecutar el script para garantizar que la solicitud GET sea exitosa.
Si el script encuentra un libro nuevo que no estaba registrado previamente, añadirá una nueva entrada con la fecha y el precio actual, y $ 0 para las fechas anteriores.
