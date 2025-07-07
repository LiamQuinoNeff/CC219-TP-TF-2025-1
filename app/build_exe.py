"""
Script para crear el ejecutable de la aplicación de recomendación de películas
"""

import os
import shutil
import subprocess
import sys


def check_requirements_file():
    """Verifica que existe el archivo requirements.txt"""
    if not os.path.exists("requirements.txt"):
        print("❌ Error: No se encontró el archivo requirements.txt")
        print("Por favor, asegúrate de que requirements.txt esté en el directorio app/")
        return False
    return True


def install_dependencies():
    """Instala las dependencias necesarias"""
    print("📦 Verificando e instalando dependencias...")
    
    # Verificar que existe requirements.txt
    if not check_requirements_file():
        return False
    
    try:
        # Mostrar las dependencias que se van a instalar
        with open("requirements.txt", "r", encoding="utf-8") as f:
            requirements = f.read().strip()
            print(f"📋 Dependencias a instalar:\n{requirements}")
        
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al instalar dependencias: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado al leer requirements.txt: {e}")
        return False


def verify_project_structure():
    """Verifica que todos los archivos y carpetas necesarios existan"""
    print("🔍 Verificando estructura del proyecto...")
    
    required_files = [
        "main.py",
        "requirements.txt"
    ]
    
    required_dirs = [
        "models",
        "utils"
    ]
    
    required_model_files = [
        "models/__init__.py",
        "models/predictor.py", 
        "models/recommender.py"
    ]
    
    required_utils_files = [
        "utils/__init__.py",
        "utils/data_loader.py",
        "utils/validators.py"
    ]
    
    # Verificar archivos principales
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Error: No se encontró el archivo requerido: {file}")
            return False
    
    # Verificar directorios
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            print(f"❌ Error: No se encontró el directorio requerido: {dir_name}")
            return False
        if not os.path.isdir(dir_name):
            print(f"❌ Error: {dir_name} existe pero no es un directorio")
            return False
    
    # Verificar archivos del módulo models
    for file in required_model_files:
        if not os.path.exists(file):
            print(f"❌ Error: No se encontró el archivo requerido: {file}")
            return False
    
    # Verificar archivos del módulo utils
    for file in required_utils_files:
        if not os.path.exists(file):
            print(f"❌ Error: No se encontró el archivo requerido: {file}")
            return False
    
    print("✅ Estructura del proyecto verificada exitosamente")
    return True


def prepare_files():
    """Prepara los archivos necesarios para el ejecutable"""
    print("📁 Preparando archivos...")
    
    # Verificar que existe el dataset
    dataset_path = "dataset_movies_api.csv"
    parent_dataset_path = "../dataset_movies_api.csv"
    
    # Primero verificar si ya existe en el directorio actual
    if os.path.exists(dataset_path):
        print(f"✅ Dataset ya existe en: {dataset_path}")
        return True
    
    # Si no existe, intentar copiarlo del directorio padre
    if not os.path.exists(parent_dataset_path):
        print(f"❌ Error: No se encontró el dataset en ninguna ubicación:")
        print(f"   - {dataset_path}")
        print(f"   - {parent_dataset_path}")
        print("Por favor, asegúrate de que el archivo dataset_movies_api.csv esté disponible")
        return False
    
    # Copiar dataset al directorio de la app
    try:
        shutil.copy2(parent_dataset_path, dataset_path)
        print(f"✅ Dataset copiado exitosamente de {parent_dataset_path}")
        
        # Verificar que la copia fue exitosa
        if not os.path.exists(dataset_path):
            print("❌ Error: La copia del dataset falló")
            return False
            
    except Exception as e:
        print(f"❌ Error al copiar dataset: {e}")
        return False
    
    return True


def check_problematic_modules():
    """Verifica módulos que pueden causar problemas con PyInstaller"""
    print("🔍 Verificando módulos problemáticos...")
    
    problematic_modules = [
        "scipy._lib.array_api_compat.numpy.fft",
        "scipy._lib.messagestream", 
        "sklearn.utils._cython_blas",
        "pandas._libs.tslibs.timedeltas"
    ]
    
    missing_modules = []
    
    for module in problematic_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"⚠️ {module} - podría causar problemas")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"📋 {len(missing_modules)} módulos problemáticos detectados")
        print("💡 PyInstaller incluirá estos módulos automáticamente")
    else:
        print("✅ Todos los módulos críticos están disponibles")
    
    return True


def check_and_update_pyinstaller():
    """Verifica y actualiza PyInstaller a una versión compatible"""
    print("🔍 Verificando versión de PyInstaller...")
    
    try:
        # Obtener versión actual de PyInstaller
        result = subprocess.run([sys.executable, "-m", "PyInstaller", "--version"], 
                              capture_output=True, text=True, check=True)
        current_version = result.stdout.strip()
        print(f"📋 Versión actual de PyInstaller: {current_version}")
        
        # Verificar si es una versión reciente (6.0 o superior es recomendable)
        version_parts = current_version.split('.')
        major_version = int(version_parts[0])
        
        if major_version < 6:
            print("⚠️ Versión de PyInstaller antigua detectada. Actualizando...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pyinstaller>=6.0"])
            print("✅ PyInstaller actualizado exitosamente")
        else:
            print("✅ Versión de PyInstaller es compatible")
            
        return True
        
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError) as e:
        print(f"⚠️ Error al verificar PyInstaller: {e}")
        print("🔄 Instalando/actualizando PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pyinstaller>=6.0"])
            print("✅ PyInstaller instalado/actualizado exitosamente")
            return True
        except subprocess.CalledProcessError as install_error:
            print(f"❌ Error al instalar PyInstaller: {install_error}")
            return False


def build_executable():
    """Construye el ejecutable usando PyInstaller"""
    print("🔨 Construyendo ejecutable...")
    
    # Verificar y actualizar PyInstaller
    if not check_and_update_pyinstaller():
        return False
    
    # Verificar módulos problemáticos
    check_problematic_modules()
    
    # Verificar que todos los archivos necesarios existen antes de construir
    required_for_build = [
        "main.py",
        "dataset_movies_api.csv",
        "models",
        "utils"
    ]
    
    for item in required_for_build:
        if not os.path.exists(item):
            print(f"❌ Error: Archivo/directorio requerido no encontrado para la construcción: {item}")
            return False
    
    # Comando de PyInstaller usando módulo de Python (optimizado)
    cmd = [
        sys.executable, "-m", "PyInstaller",  # Usar PyInstaller como módulo
        "--onefile",                    # Un solo archivo ejecutable
        "--windowed",                   # Sin ventana de consola
        "--name", "MovieRecommender",   # Nombre del ejecutable
        "--add-data", "dataset_movies_api.csv;.",  # Incluir dataset
        "--add-data", "models;models",  # Incluir carpeta models
        "--add-data", "utils;utils",    # Incluir carpeta utils
        "--distpath", "dist",           # Directorio de salida
        "--workpath", "build",          # Directorio de trabajo temporal
        "--specpath", ".",              # Directorio para el archivo .spec
        "--clean",                      # Limpiar cache antes de construir
        # Solo incluir los módulos críticos que causan el error específico
        "--hidden-import", "scipy._lib.array_api_compat.numpy.fft",
        "--hidden-import", "scipy._lib.array_api_compat",
        "--hidden-import", "scipy._lib.messagestream",
        "--hidden-import", "sklearn.utils._cython_blas",
        "--hidden-import", "pandas._libs.tslibs.timedeltas",
        "--hidden-import", "PyQt5.sip",
        "--hidden-import", "rapidfuzz.fuzz",
        # Excluir módulos innecesarios para reducir tiempo de compilación
        "--exclude-module", "matplotlib.tests",
        "--exclude-module", "scipy.tests",
        "--exclude-module", "sklearn.tests",
        "--exclude-module", "pandas.tests",
        "--exclude-module", "numpy.tests",
        "--exclude-module", "PyQt5.QtWebEngine",
        "--exclude-module", "PyQt5.QtWebEngineWidgets",
        "main.py"                       # Archivo principal
    ]
    
    try:
        print("⏳ Iniciando construcción del ejecutable...")
        print("💡 Este proceso debería tomar entre 5-15 minutos...")
        print("⚠️ Para cancelar: Ctrl+C o Ctrl+Break")
        print("🆔 Si necesitas forzar la detención, busca 'python.exe' en Task Manager")
        
        import time
        import threading
        start_time = time.time()
        
        # Ejecutar PyInstaller SIN capturar la salida para ver todo el progreso
        process = subprocess.Popen(cmd, text=True, bufsize=1, universal_newlines=True)
        
        print(f"🔢 PID del proceso PyInstaller: {process.pid}")
        print("💡 Puedes usar este PID para matar el proceso si es necesario")
        print("📊 MOSTRANDO TODO EL PROGRESO DE PYINSTALLER:")
        print("=" * 60)
        
        # Función para monitorear el progreso del directorio build
        def monitor_progress():
            last_size = 0
            while process.poll() is None:
                try:
                    if os.path.exists("build"):
                        # Calcular tamaño del directorio build
                        total_size = 0
                        file_count = 0
                        for root, dirs, files in os.walk("build"):
                            for file in files:
                                try:
                                    file_path = os.path.join(root, file)
                                    total_size += os.path.getsize(file_path)
                                    file_count += 1
                                except (OSError, FileNotFoundError):
                                    pass
                        
                        size_mb = total_size / (1024 * 1024)
                        elapsed = (time.time() - start_time) / 60
                        
                        if size_mb != last_size:
                            print(f"� [{elapsed:.1f}min] Build: {size_mb:.1f}MB, {file_count} archivos")
                            last_size = size_mb
                    
                    time.sleep(30)  # Verificar cada 30 segundos
                except:
                    pass
        
        # Iniciar monitor en hilo separado
        monitor_thread = threading.Thread(target=monitor_progress, daemon=True)
        monitor_thread.start()
        
        try:
            # Esperar a que termine el proceso
            return_code = process.wait()
            total_time = (time.time() - start_time) / 60
            
            print("=" * 60)
            print(f"⏱️ Tiempo total de construcción: {total_time:.1f} minutos")
            
        except KeyboardInterrupt:
            print("\n🛑 Cancelación detectada por el usuario")
            print("⏳ Terminando proceso PyInstaller...")
            process.terminate()
            
            # Esperar un poco para que termine limpiamente
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                print("🔪 Forzando terminación del proceso...")
                process.kill()
                process.wait()
            
            print("✅ Proceso cancelado exitosamente")
            return False
        
        if return_code != 0:
            print(f"❌ Error en la construcción del ejecutable (código: {return_code})")
            print("💡 Revisa los mensajes de error mostrados arriba")
            return False
        
        # Verificar que el ejecutable se creó correctamente
        exe_path = os.path.join("dist", "MovieRecommender.exe")
        if not os.path.exists(exe_path):
            print("❌ Error: El ejecutable no se creó en la ubicación esperada")
            return False
        
        # Verificar tamaño del ejecutable (debe ser > 10MB para incluir todas las dependencias)
        exe_size = os.path.getsize(exe_path) / (1024 * 1024)  # Tamaño en MB
        print(f"📊 Tamaño del ejecutable: {exe_size:.1f} MB")
        
        if exe_size < 10:
            print("⚠️ Advertencia: El ejecutable es muy pequeño, puede que falten dependencias")
        
        print("✅ Ejecutable creado exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error inesperado al crear ejecutable: {e}")
        return False


def cleanup():
    """Limpia archivos temporales"""
    print("🧹 Limpiando archivos temporales...")
    
    # Eliminar carpetas temporales de construcción
    temp_dirs = ["build", "__pycache__"]
    for dir_name in temp_dirs:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🗑️ Eliminado directorio temporal: {dir_name}")
    
    # NOTA: Mantenemos dataset_movies_api.csv para pruebas locales
    print("� Dataset mantenido para pruebas locales: dataset_movies_api.csv")


def main():
    """Función principal del script de construcción"""
    print("🎬 Sistema de Recomendación de Películas - Generador de Ejecutable")
    print("=" * 70)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("main.py"):
        print("❌ Error: No se encontró main.py")
        print("Asegúrate de ejecutar este script desde el directorio app/")
        return 1
    
    # Paso 0: Verificar estructura del proyecto
    if not verify_project_structure():
        print("❌ Falló la verificación de la estructura del proyecto")
        print("🛑 Empaquetado detenido")
        return 1
    
    # Paso 1: Instalar dependencias
    if not install_dependencies():
        print("❌ Falló la instalación de dependencias")
        print("🛑 Empaquetado detenido")
        return 1
    
    # Paso 2: Preparar archivos
    if not prepare_files():
        print("❌ Falló la preparación de archivos")
        print("🛑 Empaquetado detenido")
        return 1
    
    # Paso 3: Construir ejecutable
    if not build_executable():
        print("❌ Falló la construcción del ejecutable")
        cleanup()
        print("🛑 Empaquetado detenido")
        return 1
    
    # Paso 4: Limpiar archivos temporales
    cleanup()
    
    print("\n" + "=" * 70)
    print("🎉 ¡Ejecutable creado exitosamente!")
    print("📂 Ubicación: dist/MovieRecommender.exe")
    print("💡 El ejecutable incluye todos los archivos necesarios")
    print("🚀 ¡Ya puedes distribuir tu aplicación!")
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
