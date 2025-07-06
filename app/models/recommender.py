import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


class MovieRecommender:
    """Sistema de recomendación de películas basado en contenido"""
    
    def __init__(self, data_loader, text_corrector):
        self.data_loader = data_loader
        self.text_corrector = text_corrector
        self.df = data_loader.df
        self.tfidf = data_loader.tfidf
        self.tfidf_matrix = data_loader.tfidf_matrix
        self.cosine_sim = data_loader.cosine_sim
    
    def get_movie_recommendations(self, title, num_recommendations=10):
        """Obtiene recomendaciones para una película específica por título"""
        try:
            # Buscar índice de la película por título
            idx = self.df[self.df['title'].str.lower() == title.lower()].index
            
            if len(idx) == 0:
                return None, f"Película '{title}' no encontrada en el dataset"
            
            idx = idx[0]
            
            # Obtener puntuaciones de similitud para esa película
            sim_scores = list(enumerate(self.cosine_sim[idx]))
            
            # Ordenar por similitud de mayor a menor
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            
            # Obtener índices de las películas más similares (excluyendo la misma)
            movie_indices = [i[0] for i in sim_scores[1:num_recommendations+1]]
            
            # Crear DataFrame con resultados
            recommendations = self.df.iloc[movie_indices][
                ['title', 'vote_average', 'popularity', 'release_date', 'genres']
            ].copy()
            
            recommendations['similarity_score'] = [
                score[1] for score in sim_scores[1:num_recommendations+1]
            ]
            
            return recommendations, None
            
        except Exception as e:
            return None, f"Error al obtener recomendaciones: {str(e)}"
    
    def buscar_peliculas_similares(self, query, num_recommendations=10):
        """Búsqueda semántica de películas similares"""
        try:
            if not query or not query.strip():
                return None, "La consulta no puede estar vacía"
            
            # Corregir ortografía del título si es posible
            query_corregido = self.text_corrector.corregir_titulo(query)
            if not query_corregido:
                query_corregido = query
            
            # Vectorizar consulta del usuario
            query_vec = self.tfidf.transform([query_corregido.lower()])
            
            # Calcular similitud coseno contra todas las películas
            sim_scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
            
            # Buscar si hay coincidencia exacta (case-insensitive)
            idx_exact = self.df[self.df['title'].str.lower() == query_corregido.lower()].index
            movie_indices = sim_scores.argsort()[-num_recommendations:][::-1]
            
            # Si hay coincidencia exacta, ponerla primero
            if not idx_exact.empty:
                idx_exact = idx_exact[0]
                indices_finales = [idx_exact] + [i for i in movie_indices if i != idx_exact][:num_recommendations-1]
            else:
                indices_finales = movie_indices[:num_recommendations]
            
            # Crear DataFrame con resultados
            recommendations = self.df.iloc[indices_finales][
                ['title', 'vote_average', 'release_date', 'genres']
            ].copy()
            
            recommendations['similarity_score'] = sim_scores[indices_finales]
            
            return recommendations, None
            
        except Exception as e:
            return None, f"Error en la búsqueda: {str(e)}"
    
    def buscar_inteligente(self, pelicula="", actores="", directores="", top_n=10):
        """Búsqueda inteligente con filtros específicos"""
        try:
            # Filtrado por actores
            idxs = None
            
            if actores.strip():
                actores_lista = [
                    self.text_corrector.corregir_nombre_entidad(a.strip(), 'actor') 
                    for a in actores.split(',') if a.strip()
                ]
                sets = [
                    self.text_corrector.actor_index[a] 
                    for a in actores_lista 
                    if a in self.text_corrector.actor_index
                ]
                if sets:
                    idxs = set.intersection(*sets) if len(sets) > 1 else sets[0].copy()
                else:
                    idxs = set()
            
            # Filtrado por directores
            if directores.strip():
                directores_lista = [
                    self.text_corrector.corregir_nombre_entidad(d.strip(), 'director') 
                    for d in directores.split(',') if d.strip()
                ]
                sets = [
                    self.text_corrector.director_index[d] 
                    for d in directores_lista 
                    if d in self.text_corrector.director_index
                ]
                if sets:
                    director_idxs = set.intersection(*sets) if len(sets) > 1 else sets[0].copy()
                    idxs = (idxs & director_idxs) if idxs is not None else director_idxs
                else:
                    idxs = set() if idxs is None else set()
            
            # Si no hay filtros específicos o no hay resultados, usar búsqueda semántica global
            if idxs is None or not idxs:
                return self.buscar_peliculas_similares(pelicula, num_recommendations=top_n)
            
            # Ranking semántico dentro del subconjunto filtrado
            q_vec = self.tfidf.transform([pelicula.lower()]) if pelicula.strip() else self.tfidf.transform([""])
            idx_list = list(idxs)
            sims = cosine_similarity(q_vec, self.tfidf_matrix[idx_list]).flatten()
            
            ranked = sorted(
                zip(idx_list, sims),
                key=lambda x: x[1],
                reverse=True
            )
            
            resultados_idx = [i for i, _ in ranked][:top_n]
            
            # Priorizar coincidencia exacta en el subconjunto filtrado
            if pelicula.strip():
                idx_exact = [
                    i for i in resultados_idx 
                    if self.df.iloc[i]['title'].lower() == pelicula.lower()
                ]
                if idx_exact:
                    resultados_idx = idx_exact + [i for i in resultados_idx if i not in idx_exact]
                    resultados_idx = resultados_idx[:top_n]
            
            # Crear DataFrame con resultados
            recs = self.df.iloc[resultados_idx][
                ['title', 'vote_average', 'release_date', 'genres']
            ].copy()
            
            recs['similarity_score'] = [
                cosine_similarity(q_vec, self.tfidf_matrix[[i]]).flatten()[0]
                for i in resultados_idx
            ]
            
            return recs, None
            
        except Exception as e:
            return None, f"Error en la búsqueda inteligente: {str(e)}"
    
    def get_movie_details(self, title):
        """Obtiene detalles completos de una película"""
        try:
            movie = self.df[self.df['title'].str.lower() == title.lower()]
            if movie.empty:
                return None, f"Película '{title}' no encontrada"
            
            movie_data = movie.iloc[0]
            return {
                'title': movie_data['title'],
                'vote_average': movie_data['vote_average'],
                'release_date': movie_data['release_date'],
                'genres': movie_data['genres'],
                'cast': movie_data['cast'],
                'director': movie_data['director'],
                'overview': movie_data['overview'],
                'popularity': movie_data['popularity'],
                'runtime': movie_data['runtime'],
                'production_companies': movie_data['production_companies']
            }, None
            
        except Exception as e:
            return None, f"Error al obtener detalles: {str(e)}"
