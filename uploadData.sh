#!/bin/bash

curl -X GET http://localhost:5000/api/DataSave -o datos.csv

if [ -f "datos.csv" ]; then
    echo "Archivo descargado correctamente."

    # Agregar el archivo descargado a Git
    git add datos.csv

    # Hacer commit con un mensaje
    git commit -m "Subida de datos"

    # Subir los cambios al repositorio remoto
    git push origin test-webpage

    echo "Archivo subido correctamente."

else
    echo "Error: El archivo no se descargó correctamente."
fi
