"""
Script para crear el ejecutable de la aplicación de recomendación de películas
"""

import os
import shutil
import subprocess
import sys


def install_dependencies():
    """Instala las dependencias necesarias"""
    print("📦 Instalando dependencias...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al instalar dependencias: {e}")
        return False


def prepare_files():
    """Prepara los archivos necesarios para el ejecutable"""
    print("📁 Preparando archivos...")
    
    # Verificar que existe el dataset
    dataset_path = "../dataset_movies_api.csv"
    if not os.path.exists(dataset_path):
        print(f"❌ No se encontró el dataset en: {dataset_path}")
        print("Por favor, asegúrate de que el archivo dataset_movies_api.csv esté en el directorio padre")
        return False
    
    # Copiar dataset al directorio de la app
    try:
        shutil.copy2(dataset_path, "dataset_movies_api.csv")
        print("✅ Dataset copiado exitosamente")
    except Exception as e:
        print(f"❌ Error al copiar dataset: {e}")
        return False
    
    return True


def build_executable():
    """Construye el ejecutable usando PyInstaller"""
    print("🔨 Construyendo ejecutable...")
    
    # Comando de PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",                    # Un solo archivo ejecutable
        "--windowed",                   # Sin ventana de consola
        "--name", "MovieRecommender",   # Nombre del ejecutable
        "--add-data", "dataset_movies_api.csv;.",  # Incluir dataset
        "--add-data", "models;models",  # Incluir carpeta models
        "--add-data", "utils;utils",    # Incluir carpeta utils
        "--distpath", "dist",           # Directorio de salida
        "--workpath", "build",          # Directorio de trabajo temporal
        "--specpath", ".",              # Directorio para el archivo .spec
        "main.py"                       # Archivo principal
    ]
    
    try:
        subprocess.check_call(cmd)
        print("✅ Ejecutable creado exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al crear ejecutable: {e}")
        return False
    except FileNotFoundError:
        print("❌ PyInstaller no encontrado. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        try:
            subprocess.check_call(cmd)
            print("✅ Ejecutable creado exitosamente")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error al crear ejecutable: {e}")
            return False


def cleanup():
    """Limpia archivos temporales"""
    print("🧹 Limpiando archivos temporales...")
    
    # Eliminar archivos temporales
    temp_files = ["dataset_movies_api.csv"]
    for file in temp_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"🗑️ Eliminado: {file}")
    
    # Eliminar carpetas temporales (opcional)
    temp_dirs = ["build", "__pycache__"]
    for dir_name in temp_dirs:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🗑️ Eliminado directorio: {dir_name}")


def main():
    """Función principal del script de construcción"""
    print("🎬 Sistema de Recomendación de Películas - Generador de Ejecutable")
    print("=" * 70)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("main.py"):
        print("❌ Error: No se encontró main.py")
        print("Asegúrate de ejecutar este script desde el directorio app/")
        return
    
    # Paso 1: Instalar dependencias
    if not install_dependencies():
        print("❌ Falló la instalación de dependencias")
        return
    
    # Paso 2: Preparar archivos
    if not prepare_files():
        print("❌ Falló la preparación de archivos")
        return
    
    # Paso 3: Construir ejecutable
    if not build_executable():
        print("❌ Falló la construcción del ejecutable")
        cleanup()
        return
    
    # Paso 4: Limpiar archivos temporales
    cleanup()
    
    print("\n" + "=" * 70)
    print("🎉 ¡Ejecutable creado exitosamente!")
    print("📂 Ubicación: dist/MovieRecommender.exe")
    print("💡 El ejecutable incluye todos los archivos necesarios")
    print("🚀 ¡Ya puedes distribuir tu aplicación!")


if __name__ == "__main__":
    main()
