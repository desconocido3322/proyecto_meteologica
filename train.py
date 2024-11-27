import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import LSTM, Input, Dense
from tensorflow.keras.models import Sequential, load_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import random as rd
import matplotlib.pyplot as plt
import os

# Ruta para guardar/cargar el modelo
model_path = "model.h5"

# Cargar los datos
datos_combinadosAJAHUEL_H1 = pd.read_csv('final.csv')
y3 = datos_combinadosAJAHUEL_H1['ts'].values

# Preparar los datos
yw = []
yt = []
for i in range(len(y3) - 3):
    row = [y3[i], y3[i+1], y3[i+2]]
    yw.append(row)
    yt.append(y3[i+3])

# Convertir a arrays numpy
yw = np.array(yw)
yt = np.array(yt)

# Dividir en conjunto de entrenamiento y prueba
seed = 12122008
rd.seed(seed)
np.random.seed(seed)
tf.random.set_seed(seed)
yw_train, yw_test, yt_train, yt_test = train_test_split(yw, yt, test_size=0.3, random_state=seed)

# Reestructurar los datos para que sean compatibles con el modelo LSTM
yw_train = yw_train.reshape((yw_train.shape[0], 3, 1))
yw_test = yw_test.reshape((yw_test.shape[0], 3, 1))

# Verificar si el modelo ya existe y cargarlo si es así
if os.path.exists(model_path):
    print(f"Cargando modelo existente desde {model_path}...")
    model = load_model(model_path)
else:
    print("No se encontró un modelo existente. Creando uno nuevo...")
    # Definir y compilar el modelo LSTM
    model = Sequential()
    model.add(Input(name="serie", shape=(3, 1)))
    model.add(LSTM(250, activation='relu'))
    model.add(Dense(1, activation='linear'))
    model.compile(optimizer='adam', loss='mse')

# Resumen del modelo
model.summary()

# Entrenar el modelo
history = model.fit(yw_train, yt_train,batch_size=136, epochs=14, validation_data=(yw_test, yt_test), verbose=0)

# Guardar el modelo entrenado
model.save(model_path)
print(f"Modelo guardado en {model_path}.")

# Evaluar el modelo
loss = model.evaluate(yw_test, yt_test, verbose=0)
print(f'Validation loss: {loss}')

# Calcular métricas adicionales
predictions = model.predict(yw_test, verbose=0)
r2 = r2_score(yt_test, predictions)
mae = mean_absolute_error(yt_test, predictions)
mse = mean_squared_error(yt_test, predictions)

print(f'R^2: {r2}')
print(f'MAE: {mae}')
print(f'MSE: {mse}')

plt.figure(figsize=(8, 6))
plt.plot(y_test, label="Valores Reales", marker='o', linestyle='--')
plt.plot(predictions.flatten(), label="Predicciones", marker='o', linestyle='-')
plt.title(f"Comparación de Valores Reales y Predicciones\nMSE: {mse:.4f}")
plt.xlabel("Índice")
plt.ylabel("Temperatura (°C)")
plt.legend()
plt.grid()

# Guardar gráfico como archivo de imagen
plot_path = "clusters_plot.png"
plt.savefig(plot_path)
print(f"Gráfico guardado en {plot_path}")
