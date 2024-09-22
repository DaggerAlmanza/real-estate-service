# Proyecto de Microservicios Inmobiliarios

## Descripción del Proyecto
Este proyecto implementa dos microservicios:

1. Servicio de Consulta de Inmuebles: Permite a los usuarios consultar los inmuebles disponibles (en pre_venta, en_venta y vendido), aplicando filtros como el año de construcción, ciudad y estado del inmueble.

2. Servicio de Me Gusta (Conceptual): El servicio conceptual permite a los usuarios dar "Me gusta" a un inmueble. Aunque este servicio no está implementado en el código, se incluye un diagrama de Entidad-Relación y el código SQL necesario para extender la base de datos y soportar esta funcionalidad.

# **Tecnologías y lenguajes**
En este proyecto, utilizaremos Python como lenguaje de programación, para la parte del servidor HTTP, emplearemos la librería http.server para evitar el uso de frameworks (flask, django, fastapi, etc), la base de datos será MySQL, utilizando las credenciales proporcionadas, las pruebas unitarias se llevarán a cabo utilizando pytest, y por ultimo el estilo del código será pythonic, respetando el Zen de Python y siguiendo las convenciones de estilo definidas por PEP 8.

### Construido
* Lenguaje: Python 3.12.3
* Base de dato: MySQL
* Pruebas: pytest
* Manejo de peticiones HTTP: HTTPServer

### Entorno de trabajo y dependencias

1. Instalar virtualEnv e instalarlo
Linux
```sh
$ virtualenv -p python3 venv
o
$ python3 -m venv venv
```
```sh
$ source venv/bin/activate
o
$ . venv/bin/activate
```
Windows
```sh
$ python -m venv venv
```
```sh
$ venv/Scripts/activate
```
2. Instalar requirements.txt
```sh
$ pip3 install -r requirements.txt
```

## Configuración

1. Se debe configurar el archivo .env con las credenciales de acceso a la base de datos.
```sh
DB_HOST=
DB_NAME=
DB_PASSWORD=
DB_PORT=
DB_USER=
```

2. Ejecuta las pruebas:

```sh
pytest
```

- Test de Conexión a la Base de Datos
- Test de Consulta de Inmuebles

3. Ejecuta el servidor:
```sh
python consult.py
```

## Rutas del Proyecto
1. Servicio de Consulta de Inmuebles (GET http://127.0.0.1:8000/property)

    Este servicio permite a los usuarios consultar los inmuebles disponibles, con la posibilidad de aplicar filtros.

### Validación de Consultas
Realizo tres acciones para validar las consultas:

1. Validar que los parámetros recibidos en la consulta sean solo los permitidos (year, city, state). Si hay parámetros no permitidos, devuelvo un error 400 (Bad Request).

2. Validar que el parámetro year sea un número. Si no es un número, responde con un error 400 (Bad Request).

3. Validar que no existan caracteres SQL en los parámetros recibidos, ejemplo (SELECT,FROM,AND,OR,WHERE,DROP,TABLE,',"; y -). Si existen, responde con un error 400 (Bad Request).

### Filtros Disponibles:
- year: Filtra por el año de construcción del inmueble.
- city: Filtra por ciudad.
- state: Filtra por estado del inmueble.
- El archivo filters.json tiene la estructura del filtrado, ejemplo:
    ```sh
    {
        "year": 2019,
        "city": "pereira",
        "state": "vendido"
    }
    ```
2. Servicio Conceptual de "Me Gusta"

    - Entidad-Relación
        [![entidad-relaci-n.png](https://i.postimg.cc/NFB55fby/entidad-relaci-n.png)](https://postimg.cc/34fKqhs7)

        Creamos una sola tabla llamada PROPERTY_LIKE, relación muchos a muchos: Un usuario puede dar "me gusta" a muchos inmuebles, y un inmueble puede recibir "me gusta" de muchos usuarios. 

    - SQL
        ```sh
        CREATE TABLE PROPERTY_LIKE (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            property_id INT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES AUTH_USER(id) ON DELETE CASCADE,
            FOREIGN KEY (property_id) REFERENCES PROPERTY(id) ON DELETE CASCADE,
            UNIQUE KEY unique_like (user_id, property_id)
        );
        ```
3. Mejorar el modelo actual de la base de datos

    - Entidad-Relación
        [![entidad-relacion-estructura.png](https://i.postimg.cc/1Xm3y75w/entidad-relacion-estructura.png)](https://postimg.cc/YGPH33FC)

        Normalización de ciudades reduciendo la redundancia de datos de ciudades, tambien permite consultas más eficientes reñacionadas con las ciudades.

4. Además, he desplegado el servicio de consulta de inmuebles en una instancia de EC2 en AWS, el sevicio esta disponible en:

    ```sh
    http://54.209.230.73:8000/property
    ```
5. La documentación del servicio se encuentra en:

    ```sh
    http://54.209.230.73:8000/docs
    ```
