# Talana Kombat JRPG

Talana Kombat es un juego donde 2 personajes se enfrentan hasta la muerte.


## Descripción del juego

Cada personaje tiene 2 golpes especiales que se ejecutan con una combinación de movimientos + 1 botón de
golpe.


## Dependencias

### Python

Se requiere una versión de Python que sea mayor a `3.10` (por ejemplo `3.10.12`) y menor a la `3.13` (como la `3.12.1` o la `3.11.3` por ejemplo).

Este repo fue desarrollado con Python **3.12**.

### Paquetes

Se requiere Poetry para instalar las dependencias (en este repo se utilizó Poetry versión `1.8.2`).
- Para instalar todas las dependencias: `poetry install`
- Para instalar solo las dependencias principales (sin las `dev.dependencies`): `poetry install --without dev`

El listado de dependencias utilizadas es el siguiente:
* dependencias principales (`[tool.poetry.dependencies]`):
	* `Django`: framework web
	* `djangorestframework`: API REST en Django
	* `django-cors-headers`: CORS en Django
	* `python-decouple`: lee variables de entorno
* dependencias secundarias (`[tool.poetry.group.dev.dependencies]`):
	* `bandit`: análisis estático de seguridad del código
	* `black`: formateo del código
	* `codespell`: para checkeo de *spelling* en inglés
	* `coverage`: para *coverage*
	* `flake8`: análisis estático de código basada en `pycodestyle`, `pyflakes`, `mccabe`, y plugins de terceros para checkeo del estilo y calidad de código en Python
	* `ipython`: *shell* interactiva
	* `isort`: formateo del código, solo para imports
	* `mccabe`: plugin de `flake8` para checkeo de complejidad ciclomática
	* `pre-commit`: hook pre commit. Aunque después de instalarlo se ejecuta automáticamente antes de hacer cada commit, se puede checkear manualmente todos los archivos con `pre-commit run --all-files` o solo los modificados con `pre-commit run`
	* `pylint`: análisis estático de código más estricto que `flake8`
	* `pylint-django`: plugin de `pylint` para analizar estático de proyectos que utilizan `Django`
	* `prospector`: análisis estático de código basado en `flake8` y `pylint`
	* `safety`: checkeo de dependencias vulnerables

### Variables de entorno

* obligatorias
	* `SECRET_KEY`: clave secreta para el proyecto en Django
	* `ALLOWED_HOSTS`: host permitidos por Django, son valores separados por commas (por ejemplo: `'127.0.0.1, localhost, 0.0.0.0'`)
	* `DB_ENGINE`: motor de base de datos en Django (por ejemplo: `django.db.backends.sqlite3`)
	* `DB_NAME`: nombre de la base de datos
	* `DB_USER`: usuario de la base de datos
	* `DB_PASSWORD`: password para acceder a la base de datos
	* `DB_HOST`: host de la base de datos
	* `DB_PORT`: puerto de conexión a la base de datos
* opcionales
	* `MAX_PLAYER_ENERGY`: cantidad máxima de energía por cada jugador, el valor por defecto es 6
	* `MAX_MOVEMENT_LENGTH`: cantidad máxima de caracteres de cada movimiento de un jugador, el valor por defecto es 5
	* `PLAYER_1_NAME`: nombre del primer jugador, el valor por defecto es `Tonyn`
	* `PLAYER_2_NAME`: nombre del segundo jugador, el valor por defecto es `Arnaldor`

Respecto a la base de datos, para probar el proyecto solo basta utilizar el *driver* de SQLite3 (no es necesario utilizar MySQL o PostgreSQL) con las siguiente variables de entorno:
```.env
DB_ENGINE = django.db.backends.sqlite3
DB_NAME = db.sqlite3
DB_USER =
DB_PASSWORD =
DB_HOST =
DB_PORT =
```


## Tests

Se implementaron pruebas unitarias.

Para ejecutarlas se utiliza el siguiente comando dentro de la misma carpeta donde está ubicado el archivo `manage.py`: `coverage run --source='.' manage.py test --failfast kombat && coverage report && coverage html`

Eso realiza 3 acciones:
1. ejecuta las pruebas unitarias
1. genera un reporte por consola indicando la cobertura por cada archivo tomado en cuenta
1. genera archivos html con el reporte detallado de cobertura de cada archivo tomado en cuenta


## Docker

Se ha agregado 2 archivos para levantar el proyecto mediante Docker compose: `Dockerfile` y `docker-compose.yml` que incluyen todos los comandos necesarios desde la instalación de Poetry hasta la ejecución de la API REST.

Sin embargo, **es muy importante que el archivo `.env` esté dentro de la misma ruta donde está el archivo `manage.py` que es justamente donde está el archivo de ejemplo `.env.example`** 


## Uso del juego

Se implementó una API REST con 1 endpoint para probar Talana Kombat JRPG.

El endpoint (`POST /api/v1/kombat`) requiere que el *body* sea en formato JSON.

Un ejemplo de invocación con algún cliente REST como Postman o Insomnia puede ser:
- url: `http://127.0.0.1:8000/api/v1/kombat`
- método: `POST`
- *body*:
```json
{
    "player1": {
        "movimientos": ["D","DSD","S","DSD","SD"],
        "golpes": ["K","P","","K","P"]
    },
    "player2": {
        "movimientos": ["SA","SA","SA","ASA","SA"],
        "golpes": ["K","","K","P","P"]
    }
}
```

### Docs

Se ha generado un endpoint para documentación de la API en Swagger:
`GET /api/v1/schema/swagger-ui`

Para poder usar este endpoint, es necesario ejecutar el comando que recolecta los archivos estáticos para obtener los archivos estáticos asociados a Swagger:
`python manage.py collectstatic`
