# COORDINADOR_ELECTRICO 
# Proyecto de Predicción con LSTM

Este proyecto utiliza una red LSTM para predecir valores basados en datos históricos. Los datos se almacenan en un archivo CSV y el entrenamiento del modelo se realiza utilizando CML (Continuous Machine Learning).

## Archivos

- `train.py`: Script de entrenamiento del modelo.
- `requirements.txt`: Lista de dependencias del proyecto.
- `data.csv`: Archivo de datos utilizado para el entrenamiento.
- `cml.yaml`: Archivo de configuración de CML para ejecutar el workflow.

## Ejecución

1. Clonar el repositorio.
2. Instalar las dependencias: `pip install -r requirements.txt`.
3. Ejecutar el script de entrenamiento: `python train.py`.

# Plataforma web
# Funcionamiento de la pagina
## Backend
La pagina levanta el servidor de manera local con express, de la misma manera con el frontend.

El servidor al estar ejecutado de manera local genera conflictos con CORS al realizar peticiones locales por lo que como middleware se utiliza un proxy que omite estos requisitos. Este middleware deberia ser removido en produccion.

La pagina es ejecutada de manera local y redireccionada con nginx para su acceso publico, posteriormente se utiliza ngrok para su acceso externo.
## Frontend
Este frontend esta construido en HTML sin frameworks por temas de rendimiento y ahorro de memoria.

## Ejecucion 

### JSON Ejecucion local
```
cd /frontend/jsonFiles
python -m http.server 3000 --bind <HOST IP>
```
### Backend - Static Frontend
```
cd /backend/src
npm i
npm run start
```
### Entrenamiento
Para realizar el entrenamiento y dejarlo automatizado se deben configurar los comandos crontab mediante ```crontab -e```.

Dentro de este archivo deben ir los tiempos especificos para la ejecucion de cada codigo, por ejemplo:
```
6 * * * * ~/<carpeta raiz>/microProcesadores/proyecto_meteologica/webpage/backend/src/downloadData.sh
5 * * * * ~/<carpeta raiz>/proyecto_meteologica/uploadData.sh 
```
Recordar que **downloadData.sh** descarga los datos entrenados que representan a la prediccion y **uploadData.sh** envia los datos recogidos por los sensores.
# Funcionalidades
- Puede recibir valores en formato JSON desde un archivo desde misma ip local con distinto puerto.
- Dichos valores se almacenan cada 10 segundos de manera local y cada 1 hora se envian a la base de datos.
- Son almacenados en la base de datos en formato JSON.
- Posee un script que carga los datos para ser utilizados en entrenamiento, estos datos estan en formato csv y dentro del front y son descargados desde la base de datos, al ser enviado mediante un push ejecuta el runner dentro del github.
- Posee un script que descarga los datos de entrenamiento con el resultado de la temperatura o datos a predecir, esta dentro del backend y se envia al front para ser visualizado.
### Estructura de datos env en backend
```
BACKEND_PORT= <Puerto del host/servidor>

JSON_PORT= <Puerto desde donde se extraen los datos>

MONGO_URI= <URI para mongo>

IP_HOST= <IP del host>

JSON_IP= <IP desde donde se extraen los datos>

UPLOAD_TIME= <Tiempo de espera para la carga en milisegundos>

LOAD_INFO= <Tiempo de actualizacion de rastreo de los datos de los sensores>
```
# TODO
- ~~Al recibir los datos con el backend crear script para enviarlos cada 24 horas a alguna base de datos o metodo de respaldo.~~
- ~~Separar datos recibidos para dos interfaces distintas, separando por arduinos 1 y 2.~~
- ~~Script que lea los datos cada 10 segundos.~~
- ~~Mejorar la interfaz visual (frontend).~~
- ~~Crear llamada para pedir los valores guardados en backend y funcion para ejecutarlo con un boton.~~
- ~~Unir todo en conjunto.~~
- ~~Probablemente falle por:~~
  - ~~Nombres de las columnas.~~
  - ~~Puertos incorrectos.~~
  - ~~Sobrecarga de archivos locales.~~
  - ~~Se cierra la pagina de navegador.~~
  - ~~En general errores con cors.~~
- Realizar prueba real con todo armado.
- Balancear minutos de carga, descarga y entrenamiento ajustando comandos cron.
- Balancear tiempo carga en la base de datos.
