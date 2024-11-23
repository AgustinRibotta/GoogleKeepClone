#!/bin/bash

# Verificar si Python está instalado
if ! command -v python &> /dev/null; then
    echo "Debes instalar Python desde la página oficial: https://www.python.org/"
    exit 1
fi
echo "Python está instalado correctamente."

# Verificar si pip está instalado
if ! command -v pip &> /dev/null; then
    echo "Debes instalar pip. Puedes instalarlo ejecutando 'python -m ensurepip --upgrade'."
    exit 1
fi
echo "pip está instalado correctamente."

# Instalar pipenv
echo "Instalando pipenv..."
pip install pipenv

# Verificar si pipenv está instalado
if ! command -v pipenv &> /dev/null; then
    echo "Hubo un error al instalar pipenv. Asegúrate de tener una conexión a internet y permisos adecuados."
    exit 1
fi
echo "pipenv está instalado correctamente."

# Verificar si ya hay un entorno virtual activo
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "Ya hay un entorno virtual activado."
else
    echo "No hay un entorno virtual activo. Los comandos se ejecutarán con 'pipenv run'."
fi

# Instalar dependencias desde el Pipfile usando pipenv run
echo "Instalando dependencias con pipenv..."
pipenv install
if [ $? -eq 0 ]; then
    echo "Dependencias instaladas correctamente."
else
    echo "Hubo un error al instalar las dependencias."
    exit 1
fi

# Realizar migraciones utilizando pipenv run
echo "Realizando migraciones..."
pipenv run python manage.py makemigrations
if [ $? -ne 0 ]; then
    echo "Hubo un error al ejecutar makemigrations."
    exit 1
fi

pipenv run python manage.py migrate
if [ $? -ne 0 ]; then
    echo "Hubo un error al ejecutar migrate."
    exit 1
fi

# Finalizar con instrucciones para el usuario
echo "==========================================="
echo ""
echo "¡Proceso completado exitosamente!"
echo ""
echo "Para finalizar, debes crear un superusuario ejecutando:"
echo ""
echo "  pipenv run python manage.py createsuperuser"
echo ""
echo "Luego, puedes correr el servidor de desarrollo con:"
echo ""
echo "  pipenv run python manage.py runserver"
echo ""
echo "El servidor estará disponible por defecto en: http://127.0.0.1:8000/"
echo ""
echo "En el panel de administración puedes ver las tablas de la base de datos en:"
echo ""
echo "  http://127.0.0.1:8000/admin"
echo ""
echo "==========================================="
