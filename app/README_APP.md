# Sistema de Recomendación de Películas

Una aplicación de escritorio moderna para recomendar películas basada en análisis de contenido y machine learning.

## Características

- **Búsqueda por similitud**: Encuentra películas similares a una película específica
- **Búsqueda inteligente**: Busca por actores, directores y palabras clave
- **Predicción de calificaciones**: Predice la calificación de una película basada en sus características
- **Interfaz moderna**: Diseño intuitivo y atractivo con PyQt5
- **Corrección automática**: Corrección ortográfica automática de títulos y nombres

## Instalación y Uso

### Opción 1: Ejecutar desde código fuente

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar la aplicación:
```bash
python main.py
```

### Opción 2: Crear ejecutable

1. Ejecutar el script de construcción:
```bash
python build_exe.py
```

2. El ejecutable se creará en la carpeta `dist/`

## Estructura del Proyecto

```
app/
├── main.py              # Aplicación principal con interfaz PyQt5
├── models/
│   ├── recommender.py   # Sistema de recomendación
│   ├── predictor.py     # Modelo predictivo
│   └── saved/           # Modelos entrenados (generados automáticamente)
├── utils/
│   ├── data_loader.py   # Carga y preprocesamiento de datos
│   └── validators.py    # Validación y corrección de texto
├── requirements.txt     # Dependencias del proyecto
├── build_exe.py        # Script para crear ejecutable
└── README.md           # Este archivo
```

## Tecnologías Utilizadas

- **PyQt5**: Interfaz gráfica moderna
- **pandas**: Manipulación de datos
- **scikit-learn**: Machine learning (TF-IDF, Random Forest)
- **rapidfuzz**: Corrección ortográfica fuzzy
- **PyInstaller**: Creación de ejecutables

## Funcionalidades

### 1. Búsqueda por Similitud
- Ingresa el título de una película
- Obtén 10 películas similares basadas en contenido
- Corrección automática de ortografía

### 2. Búsqueda Inteligente
- Busca por actores, directores o palabras clave
- Combina múltiples criterios de búsqueda
- Resultados ordenados por relevancia

### 3. Predicción de Calificaciones
- Predice la calificación IMDb de una película
- Basado en presupuesto, popularidad, duración, etc.
- Visualización intuitiva del resultado

## Dataset

La aplicación utiliza un dataset de ~10,000 películas obtenidas de la API de TMDb, incluyendo:
- Información básica (título, fecha, géneros)
- Cast y director
- Métricas (calificación, popularidad, presupuesto)
- Sinopsis y productoras

## Autores

Rafael Chui, Rodrigo Meza, Axel Pariona & Liam Quino Neff
