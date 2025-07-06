import pandas as pd
import numpy as np
import ast
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer


class DataLoader:
    def __init__(self, dataset_path="dataset_movies_api.csv"):
        self.dataset_path = dataset_path
        self.df = None
        self.tfidf = None
        self.tfidf_matrix = None
        self.cosine_sim = None
        self.rf_pipeline = None
        self.feature_columns = ['budget', 'popularity', 'runtime', 'release_year', 'num_genres', 'num_cast']
        
    def load_data(self):
        """Carga y preprocesa el dataset"""
        try:
            # Verificar si el dataset existe
            if not os.path.exists(self.dataset_path):
                # Buscar en el directorio padre
                parent_path = os.path.join("..", self.dataset_path)
                if os.path.exists(parent_path):
                    self.dataset_path = parent_path
                else:
                    raise FileNotFoundError(f"No se encontró el dataset: {self.dataset_path}")
            
            # Cargar dataset
            self.df = pd.read_csv(self.dataset_path)
            
            # Preprocesamiento básico
            self.df['release_date'] = pd.to_datetime(self.df['release_date'], errors='coerce')
            self.df['overview'] = self.df['overview'].fillna('')
            self.df['director'] = self.df['director'].fillna('Unknown')
            self.df = self.df.drop_duplicates(subset=['id'])
            
            # Convertir listas en string a listas reales
            cols_listas = ['genres', 'cast', 'production_companies']
            for col in cols_listas:
                self.df[col] = self.df[col].apply(ast.literal_eval)
            
            # Crear características adicionales
            self.df['release_year'] = self.df['release_date'].dt.year
            self.df['num_genres'] = self.df['genres'].apply(len)
            self.df['num_cast'] = self.df['cast'].apply(len)
            
            # Crear content profile
            self.df['content_profile'] = self.df.apply(self._crear_content_profile, axis=1)
            
            print(f"Dataset cargado exitosamente: {len(self.df)} películas")
            return True
            
        except Exception as e:
            print(f"Error al cargar el dataset: {str(e)}")
            return False
    
    def _crear_content_profile(self, row):
        """Crea el perfil de contenido para cada película"""
        genres = ' '.join(row['genres'])
        cast = ' '.join(row['cast'])
        companies = ' '.join(row['production_companies'])
        director = row['director']
        overview = row['overview']
        
        profile = f"{genres} {cast} {companies} {director} {overview}"
        return profile.lower()
    
    def create_similarity_matrix(self):
        """Crea la matriz de similitud TF-IDF"""
        try:
            # Crear vectorizador TF-IDF
            self.tfidf = TfidfVectorizer(
                max_features=5000,
                stop_words='english',
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.8
            )
            
            # Ajustar y transformar
            self.tfidf_matrix = self.tfidf.fit_transform(self.df['content_profile'])
            
            # Calcular similitud coseno
            self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)
            
            print(f"Matriz de similitud creada: {self.tfidf_matrix.shape}")
            return True
            
        except Exception as e:
            print(f"Error al crear matriz de similitud: {str(e)}")
            return False
    
    def train_prediction_model(self):
        """Entrena el modelo de predicción de calificaciones"""
        try:
            # Preparar datos para el modelo
            df_model = self.df[self.feature_columns + ['vote_average']].dropna()
            X = df_model[self.feature_columns]
            y = df_model['vote_average']
            
            # Crear pipeline
            preprocessor = ColumnTransformer(
                transformers=[
                    ('num', StandardScaler(), self.feature_columns)
                ]
            )
            
            self.rf_pipeline = Pipeline([
                ('preprocessor', preprocessor),
                ('regressor', RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1))
            ])
            
            # Entrenar modelo
            self.rf_pipeline.fit(X, y)
            
            print("Modelo de predicción entrenado exitosamente")
            return True
            
        except Exception as e:
            print(f"Error al entrenar modelo: {str(e)}")
            return False
    
    def save_models(self, models_dir="models/saved"):
        """Guarda los modelos entrenados"""
        try:
            os.makedirs(models_dir, exist_ok=True)
            
            # Guardar vectorizador TF-IDF
            with open(os.path.join(models_dir, "tfidf_vectorizer.pkl"), "wb") as f:
                pickle.dump(self.tfidf, f)
            
            # Guardar matriz TF-IDF
            with open(os.path.join(models_dir, "tfidf_matrix.pkl"), "wb") as f:
                pickle.dump(self.tfidf_matrix, f)
            
            # Guardar matriz de similitud coseno
            with open(os.path.join(models_dir, "cosine_similarity.pkl"), "wb") as f:
                pickle.dump(self.cosine_sim, f)
            
            # Guardar modelo de predicción
            with open(os.path.join(models_dir, "rf_pipeline.pkl"), "wb") as f:
                pickle.dump(self.rf_pipeline, f)
            
            print("Modelos guardados exitosamente")
            return True
            
        except Exception as e:
            print(f"Error al guardar modelos: {str(e)}")
            return False
    
    def load_models(self, models_dir="models/saved"):
        """Carga los modelos pre-entrenados"""
        try:
            # Cargar vectorizador TF-IDF
            with open(os.path.join(models_dir, "tfidf_vectorizer.pkl"), "rb") as f:
                self.tfidf = pickle.load(f)
            
            # Cargar matriz TF-IDF
            with open(os.path.join(models_dir, "tfidf_matrix.pkl"), "rb") as f:
                self.tfidf_matrix = pickle.load(f)
            
            # Cargar matriz de similitud coseno
            with open(os.path.join(models_dir, "cosine_similarity.pkl"), "rb") as f:
                self.cosine_sim = pickle.load(f)
            
            # Cargar modelo de predicción
            with open(os.path.join(models_dir, "rf_pipeline.pkl"), "rb") as f:
                self.rf_pipeline = pickle.load(f)
            
            print("Modelos cargados exitosamente")
            return True
            
        except Exception as e:
            print(f"Error al cargar modelos: {str(e)}")
            return False
    
    def initialize_system(self):
        """Inicializa todo el sistema de datos y modelos"""
        print("Iniciando sistema de recomendación...")
        
        # Cargar datos
        if not self.load_data():
            return False
        
        # Intentar cargar modelos existentes
        if self.load_models():
            print("Sistema inicializado con modelos pre-entrenados")
            return True
        
        # Si no existen modelos, crearlos
        print("Creando nuevos modelos...")
        if not self.create_similarity_matrix():
            return False
        
        if not self.train_prediction_model():
            return False
        
        # Guardar modelos para uso futuro
        self.save_models()
        
        print("Sistema inicializado exitosamente")
        return True
