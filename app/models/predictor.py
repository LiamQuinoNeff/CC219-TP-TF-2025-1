import pandas as pd


class MoviePredictor:
    """Sistema de predicción de calificaciones de películas"""
    
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.rf_pipeline = data_loader.rf_pipeline
        self.feature_columns = data_loader.feature_columns
    
    def predict_rating(self, budget, popularity, runtime, year, num_genres, num_cast):
        """Predice la calificación de una película basada en sus características"""
        try:
            # Crear DataFrame con los datos de entrada
            input_data = pd.DataFrame({
                'budget': [budget],
                'popularity': [popularity],
                'runtime': [runtime],
                'release_year': [year],
                'num_genres': [num_genres],
                'num_cast': [num_cast]
            })
            
            # Hacer predicción
            prediction = self.rf_pipeline.predict(input_data)[0]
            
            # Asegurar que la predicción esté en el rango válido (0-10)
            prediction = max(0, min(10, prediction))
            
            return prediction, None
            
        except Exception as e:
            return None, f"Error en la predicción: {str(e)}"
    
    def get_feature_importance(self):
        """Obtiene la importancia de las características del modelo"""
        try:
            importancias = self.rf_pipeline.named_steps['regressor'].feature_importances_
            
            importance_dict = {}
            for i, feature in enumerate(self.feature_columns):
                importance_dict[feature] = importancias[i]
            
            # Ordenar por importancia
            sorted_importance = sorted(
                importance_dict.items(), 
                key=lambda x: x[1], 
                reverse=True
            )
            
            return sorted_importance, None
            
        except Exception as e:
            return None, f"Error al obtener importancia: {str(e)}"
    
    def validate_input_ranges(self, budget, popularity, runtime, year, num_genres, num_cast):
        """Valida que los valores de entrada estén en rangos razonables"""
        errors = []
        
        if budget < 0:
            errors.append("El presupuesto no puede ser negativo")
        
        if popularity < 0 or popularity > 1000:
            errors.append("La popularidad debe estar entre 0 y 1000")
        
        if runtime < 1 or runtime > 500:
            errors.append("La duración debe estar entre 1 y 500 minutos")
        
        if year < 1900 or year > 2030:
            errors.append("El año debe estar entre 1900 y 2030")
        
        if num_genres < 1 or num_genres > 10:
            errors.append("El número de géneros debe estar entre 1 y 10")
        
        if num_cast < 1 or num_cast > 50:
            errors.append("El número de actores debe estar entre 1 y 50")
        
        return errors
    
    def get_statistics(self):
        """Obtiene estadísticas del dataset para ayudar al usuario"""
        try:
            df = self.data_loader.df
            
            stats = {
                'budget': {
                    'min': df['budget'].min(),
                    'max': df['budget'].max(),
                    'mean': df['budget'].mean(),
                    'median': df['budget'].median()
                },
                'popularity': {
                    'min': df['popularity'].min(),
                    'max': df['popularity'].max(),
                    'mean': df['popularity'].mean(),
                    'median': df['popularity'].median()
                },
                'runtime': {
                    'min': df['runtime'].min(),
                    'max': df['runtime'].max(),
                    'mean': df['runtime'].mean(),
                    'median': df['runtime'].median()
                },
                'release_year': {
                    'min': df['release_year'].min(),
                    'max': df['release_year'].max(),
                    'mean': df['release_year'].mean(),
                    'median': df['release_year'].median()
                },
                'num_genres': {
                    'min': df['num_genres'].min(),
                    'max': df['num_genres'].max(),
                    'mean': df['num_genres'].mean(),
                    'median': df['num_genres'].median()
                },
                'num_cast': {
                    'min': df['num_cast'].min(),
                    'max': df['num_cast'].max(),
                    'mean': df['num_cast'].mean(),
                    'median': df['num_cast'].median()
                }
            }
            
            return stats, None
            
        except Exception as e:
            return None, f"Error al obtener estadísticas: {str(e)}"
