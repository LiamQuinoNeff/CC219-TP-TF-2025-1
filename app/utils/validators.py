import re
import unicodedata
from rapidfuzz import process, fuzz
from collections import defaultdict


def normalize_text(s):
    """Normaliza texto: minúsculas, sin acentos, solo letras y números"""
    # Quitar acentos
    s = unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode()
    # Minúsculas
    s = s.lower()
    # Solo letras y números
    s = re.sub(r'[^a-z0-9]+', ' ', s)
    # Colapsar espacios múltiples
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def validate_float(value_str, min_val=None, max_val=None):
    """Valida y convierte string a float"""
    try:
        value = float(value_str)
        if min_val is not None and value < min_val:
            return None, f"El valor debe ser mayor o igual a {min_val}"
        if max_val is not None and value > max_val:
            return None, f"El valor debe ser menor o igual a {max_val}"
        return value, None
    except ValueError:
        return None, "Debe ser un número válido"


def validate_int(value_str, min_val=None, max_val=None):
    """Valida y convierte string a int"""
    try:
        value = int(value_str)
        if min_val is not None and value < min_val:
            return None, f"El valor debe ser mayor o igual a {min_val}"
        if max_val is not None and value > max_val:
            return None, f"El valor debe ser menor o igual a {max_val}"
        return value, None
    except ValueError:
        return None, "Debe ser un número entero válido"


def validate_text(text, max_length=None):
    """Valida texto de entrada"""
    if not text or not text.strip():
        return None, "El texto no puede estar vacío"
    
    text = text.strip()
    if max_length and len(text) > max_length:
        return None, f"El texto no puede exceder {max_length} caracteres"
    
    return text, None


class TextCorrector:
    """Clase para corrección de títulos y nombres usando fuzzy matching"""
    
    def __init__(self, df):
        self.df = df
        self._build_indexes()
    
    def _build_indexes(self):
        """Construye índices para búsqueda rápida"""
        # Índices para actores, directores y productoras
        self.actor_index = defaultdict(set)
        self.director_index = defaultdict(set)
        self.company_index = defaultdict(set)
        
        for idx, row in self.df.iterrows():
            # Cast
            for actor in row['cast']:
                na = normalize_text(actor)
                self.actor_index[na].add(idx)
            
            # Director
            nd = normalize_text(row['director'])
            self.director_index[nd].add(idx)
            
            # Productoras
            for comp in row['production_companies']:
                nc = normalize_text(comp)
                self.company_index[nc].add(idx)
        
        # Índice de títulos
        self.norm_to_titles = {}
        for title in self.df['title'].tolist():
            nt = normalize_text(title)
            self.norm_to_titles.setdefault(nt, []).append(title)
        
        self.titulos_norm = list(self.norm_to_titles.keys())
        self.actor_names = list(self.actor_index.keys())
        self.director_names = list(self.director_index.keys())
        self.company_names = list(self.company_index.keys())
    
    def corregir_titulo(self, titulo_input, threshold=70):
        """Corrige título usando fuzzy matching"""
        if not titulo_input or not titulo_input.strip():
            return titulo_input
        
        ni = normalize_text(titulo_input)
        
        resultado = process.extractOne(
            ni,
            self.titulos_norm,
            scorer=fuzz.token_sort_ratio
        )
        
        if resultado and resultado[1] >= threshold:
            key_norm = resultado[0]
            originales = self.norm_to_titles[key_norm]
            
            if len(originales) == 1:
                return originales[0]
            
            # Desempate
            best = process.extractOne(
                titulo_input,
                originales,
                scorer=fuzz.token_sort_ratio
            )
            return best[0] if best else titulo_input
        
        return titulo_input
    
    def corregir_nombre_entidad(self, nombre, entidad, threshold=75):
        """Corrige nombre de actor, director o productora"""
        if not nombre or not nombre.strip():
            return nombre
        
        nombre_norm = normalize_text(nombre)
        
        if entidad == 'actor':
            candidates = self.actor_names
        elif entidad == 'director':
            candidates = self.director_names
        elif entidad == 'company':
            candidates = self.company_names
        else:
            return nombre_norm
        
        resultado = process.extractOne(
            nombre_norm, 
            candidates, 
            scorer=fuzz.token_sort_ratio
        )
        
        if resultado and resultado[1] >= threshold:
            return resultado[0]
        
        return nombre_norm
