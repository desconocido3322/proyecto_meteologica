import numpy as np
import tensorflow as tf
import sys

# Configuración de semillas para reproducibilidad
seed = 12122008
np.random.seed(seed)
tf.random.set_seed(seed)

# Verificar argumentos
if len(sys.argv) < 2:
    print("Error: Debes pasar una lista de 3 valores como argumento.")
    sys.exit(1)

# Convertir el argumento a una lista de valores
try:
    datos = eval(sys.argv[1])  # Convierte el argumento en una lista
    if not isinstance(datos, list) or len(datos) != 3:
        raise ValueError
except:
    print("Error: El argumento debe ser una lista de 3 valores. Ejemplo: '[13.2, 13.3, 13.4]'")
    sys.exit(1)

# Cargar el modelo entrenado
try:
    model = tf.keras.models.load_model("model.h5")
except Exception as e:
    print(f"Error al cargar el modelo: {e}")
    sys.exit(1)

# Convertir la lista de datos a un formato compatible con el modelo
datos = np.array(datos).reshape((1, 3, 1))

# Generar predicciones para completar una hora (12 predicciones si son intervalos de 5 minutos)
ultimo_valor = None
for _ in range(12):  # 12 predicciones = 1 hora si los intervalos son de 5 minutos
    # Realizar la predicción
    prediccion = model.predict(datos, verbose=0)[0][0]
    ultimo_valor = prediccion  # Guardar el último valor predicho
    
    # Actualizar la lista de entrada
    datos = np.append(datos[0, 1:], [[prediccion]], axis=0).reshape((1, 3, 1))

# Retornar el último valor predicho
print(f"ultimo valor predicho después de 1 hora: {ultimo_valor:.2f}")
