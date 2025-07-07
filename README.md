# Sistema de Recomendación de Películas 🎬

Un sistema completo de recomendación de películas que combina análisis de datos, machine learning y una interfaz gráfica moderna. Este proyecto incluye un análisis exploratorio de datos, sistema de recomendación basado en contenido, modelo predictivo de calificaciones y una aplicación de escritorio desarrollada en PyQt5.

## 📋 Descripción del Proyecto

Este proyecto fue desarrollado por **Rafael Chui, Rodrigo Meza, Axel Pariona & Liam Quino Neff** como parte de un trabajo de análisis de datos aplicado al sistema de recomendación de películas. Utiliza datos de la API de TMDb (The Movie Database) para crear un sistema inteligente que puede:

- **Recomendar películas similares** basándose en contenido
- **Predecir calificaciones** usando características de las películas
- **Búsqueda inteligente** por actores, directores y palabras clave
- **Corrección automática** de nombres y títulos
- **Interfaz gráfica moderna** para una experiencia de usuario optimizada

## 🏗️ Estructura del Proyecto

```
MovieRecommendation/
├── README.md                    # Documentación principal
├── data/
│   └── dataset_movies_api.csv  # Dataset con 10,000+ películas de TMDb
├── code/
│   └── Data_____TF_Chui_Meza_Pariona_Quino.ipynb  # Análisis completo en Jupyter
└── app/
    ├── main.py                 # Aplicación principal PyQt5
    ├── requirements.txt        # Dependencias del proyecto
    ├── build_exe.py           # Script para generar ejecutable
    ├── README_APP.md          # Documentación específica de la app
    ├── models/
    │   ├── __init__.py
    │   ├── recommender.py     # Sistema de recomendación
    │   ├── predictor.py       # Modelo predictivo
    │   └── saved/            # Modelos entrenados guardados
    └── utils/
        ├── __init__.py
        ├── data_loader.py     # Carga y preprocesamiento de datos
        └── validators.py      # Validadores de entrada
```

## 🚀 Características Principales

### 1. **Sistema de Recomendación Basado en Contenido**
- Utiliza TF-IDF y similitud coseno
- Análisis de géneros, actores, directores y sinopsis
- Recomendaciones personalizadas por similitud de contenido

### 2. **Modelo Predictivo de Calificaciones**
- Random Forest Regressor optimizado
- Predice `vote_average` basándose en:
  - Presupuesto de la película
  - Popularidad
  - Duración (runtime)
  - Año de lanzamiento
  - Número de géneros
  - Número de actores principales

### 3. **Búsqueda Inteligente**
- Búsqueda por similitud de títulos
- Filtrado por actores y directores
- Corrección automática ortográfica usando RapidFuzz
- Búsqueda por palabras clave en sinopsis

### 4. **Interfaz Gráfica Moderna**
- Desarrollada en PyQt5
- Diseño intuitivo y responsive
- Múltiples pestañas para diferentes funcionalidades
- Indicadores de progreso y retroalimentación visual

## 📊 Dataset

El proyecto utiliza un dataset de **10,000+ películas** extraídas de la API de TMDb con las siguientes características:

- **Información básica**: título, fecha de lanzamiento, géneros, sinopsis
- **Métricas**: popularidad, calificación promedio, número de votos
- **Detalles técnicos**: duración, presupuesto, compañías productoras
- **Elenco**: actores principales y director
- **Identificadores únicos**: ID de TMDb para cada película

## 🛠️ Instalación y Configuración

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Opción 1: Ejecutar desde Código Fuente

1. **Clonar el repositorio:**
```bash
git clone [url-del-repositorio]
cd MovieRecommendation
```

2. **Instalar dependencias:**
```bash
cd app
pip install -r requirements.txt
```

3. **Ejecutar la aplicación:**
```bash
python main.py
```

### Opción 2: Generar Ejecutable

1. **Instalar dependencias y generar ejecutable:**
```bash
cd app
pip install -r requirements.txt
python build_exe.py
```

2. **Ejecutar el archivo generado:**
```bash
./dist/MovieRecommendation.exe
```

## 🔧 Dependencias Principales

- **pandas** (2.0.3): Manipulación y análisis de datos
- **numpy** (1.24.3): Computación numérica
- **scikit-learn** (1.3.0): Machine learning y minería de datos
- **matplotlib** (3.7.2): Visualización de datos
- **seaborn** (0.12.2): Visualización estadística
- **rapidfuzz** (3.2.0): Corrección ortográfica y búsqueda difusa
- **PyQt5** (5.15.9): Interfaz gráfica de usuario
- **requests** (2.31.0): Peticiones HTTP
- **pyinstaller** (5.13.0): Generación de ejecutables

## 📈 Metodología y Análisis

### 1. **Análisis Exploratorio de Datos (EDA)**
- Distribución de calificaciones y popularidad
- Análisis temporal de lanzamientos
- Correlaciones entre variables
- Visualizaciones interactivas

### 2. **Preprocesamiento de Datos**
- Limpieza y normalización de texto
- Manejo de valores faltantes
- Codificación de variables categóricas
- Escalado de características numéricas

### 3. **Sistema de Recomendación**
- **TF-IDF Vectorization**: Para análisis de texto de sinopsis
- **Cosine Similarity**: Para calcular similitud entre películas
- **Content-Based Filtering**: Recomendaciones basadas en características

### 4. **Modelo Predictivo**
- **Random Forest Regressor**: Modelo principal para predicción
- **Feature Engineering**: Creación de características relevantes
- **Cross-Validation**: Validación cruzada para robustez
- **Hyperparameter Tuning**: Optimización de parámetros

## 🎯 Funcionalidades de la Aplicación

### **Pestaña de Recomendaciones**
- Buscar películas por título
- Obtener recomendaciones similares
- Ver detalles de calificaciones y popularidad
- Exportar resultados

### **Pestaña de Búsqueda Inteligente**
- Búsqueda por actores y directores
- Filtrado avanzado por criterios múltiples
- Corrección automática de nombres
- Resultados ordenados por relevancia

### **Pestaña de Predicción**
- Predecir calificación de nuevas películas
- Entrada intuitiva de características
- Visualización de importancia de características
- Análisis de factores influyentes

## 📚 Uso del Jupyter Notebook

El notebook `Data_____TF_Chui_Meza_Pariona_Quino.ipynb` contiene:

1. **Instalación de dependencias**
2. **Funciones de verificación de entradas**
3. **Recolección y carga de datos**
4. **Análisis exploratorio completo**
5. **Preprocesamiento y limpieza**
6. **Implementación del sistema de recomendación**
7. **Desarrollo del modelo predictivo**
8. **Visualizaciones y gráficos**
9. **Búsqueda inteligente y corrección de texto**
10. **Funciones de corrección para actores, directores y productoras**
11. **Interfaz interactiva para pruebas**

## 🔍 Ejemplos de Uso

### Recomendaciones por Similitud
```python
# Buscar películas similares a "The Avengers"
recommendations = recommender.get_movie_recommendations("The Avengers", 5)
```

### Predicción de Calificaciones
```python
# Predecir calificación de una película
rating = predictor.predict_rating(
    budget=150000000,
    popularity=500.0,
    runtime=120,
    year=2024,
    num_genres=3,
    num_cast=5
)
```

### Búsqueda Inteligente
```python
# Buscar películas con corrección automática
results = recommender.buscar_peliculas_similares("Tom Hanks", 10)
```

## 🤝 Contribuciones

Este proyecto fue desarrollado por:
- **Rafael Chui**
- **Rodrigo Meza** 
- **Axel Pariona**
- **Liam Quino Neff**

Como parte de un trabajo académico de análisis de datos y machine learning aplicado a sistemas de recomendación.

## 📝 Licencia

Este proyecto es desarrollado con fines académicos y de investigación.

## 🆘 Soporte

Para preguntas o problemas:
1. Revisar la documentación en `app/README_APP.md`
2. Consultar el notebook para ejemplos detallados
3. Verificar que todas las dependencias estén instaladas correctamente

---

**¡Disfruta descubriendo nuevas películas con nuestro sistema de recomendación! 🍿**
