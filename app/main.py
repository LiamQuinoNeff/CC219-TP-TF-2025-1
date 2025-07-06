import sys
import os

# Agregar el directorio actual al path de Python para encontrar módulos locales
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QComboBox, QSpinBox,
    QDoubleSpinBox, QTabWidget, QMessageBox, QProgressDialog,
    QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox,
    QGridLayout, QSplashScreen, QFrame
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor, QPixmap

# Importar módulos locales
from utils import DataLoader, TextCorrector
from models import MovieRecommender, MoviePredictor


class LoadingWorker(QThread):
    """Hilo separado para cargar datos sin bloquear la interfaz"""
    
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self):
        super().__init__()
        self.data_loader = None
        self.text_corrector = None
        self.recommender = None
        self.predictor = None
    
    def run(self):
        try:
            self.progress.emit("Iniciando sistema...")
            self.data_loader = DataLoader()
            
            self.progress.emit("Cargando dataset...")
            if not self.data_loader.initialize_system():
                self.finished.emit(False, "Error al inicializar el sistema de datos")
                return
            
            self.progress.emit("Configurando corrector de texto...")
            self.text_corrector = TextCorrector(self.data_loader.df)
            
            self.progress.emit("Inicializando sistema de recomendación...")
            self.recommender = MovieRecommender(self.data_loader, self.text_corrector)
            
            self.progress.emit("Configurando modelo de predicción...")
            self.predictor = MoviePredictor(self.data_loader)
            
            self.progress.emit("¡Sistema listo!")
            self.finished.emit(True, "Sistema cargado exitosamente")
            
        except Exception as e:
            self.finished.emit(False, f"Error durante la carga: {str(e)}")


class MovieRecommendationApp(QMainWindow):
    """Aplicación principal de recomendación de películas"""
    
    def __init__(self):
        super().__init__()
        self.recommender = None
        self.predictor = None
        self.init_ui()
        self.show_loading_screen()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        self.setWindowTitle("Sistema de Recomendación de Películas")
        self.setGeometry(100, 100, 1200, 800)
        
        # Establecer estilo moderno
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTabWidget::pane {
                border: 1px solid #c0c0c0;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                border: 1px solid #c0c0c0;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 1px solid white;
            }
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox {
                border: 2px solid #ddd;
                border-radius: 4px;
                padding: 8px;
                font-size: 12px;
            }
            QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
                border-color: #4CAF50;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        # Widget central con pestañas
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Título principal
        title_label = QLabel("🎬 Sistema de Recomendación de Películas")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50; margin: 20px;")
        layout.addWidget(title_label)
        
        # Pestañas
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Crear pestañas
        self.create_similarity_tab()
        self.create_intelligent_search_tab()
        self.create_prediction_tab()
        
        # Estado inicial: deshabilitado hasta que se carguen los datos
        self.tab_widget.setEnabled(False)
    
    def create_similarity_tab(self):
        """Crea la pestaña de búsqueda por similitud"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Grupo de entrada
        input_group = QGroupBox("Búsqueda de Películas Similares")
        input_layout = QVBoxLayout(input_group)
        
        # Campo de título
        title_layout = QHBoxLayout()
        title_layout.addWidget(QLabel("Título de la película:"))
        self.similarity_title_input = QLineEdit()
        self.similarity_title_input.setPlaceholderText("Ej: Spider-Man, Avatar, The Matrix...")
        title_layout.addWidget(self.similarity_title_input)
        input_layout.addLayout(title_layout)
        
        # Botón de búsqueda
        search_btn = QPushButton("🔍 Buscar Películas Similares")
        search_btn.clicked.connect(self.search_similar_movies)
        input_layout.addWidget(search_btn)
        
        layout.addWidget(input_group)
        
        # Tabla de resultados
        results_group = QGroupBox("Resultados")
        results_layout = QVBoxLayout(results_group)
        
        self.similarity_results_table = QTableWidget()
        self.similarity_results_table.setColumnCount(4)
        self.similarity_results_table.setHorizontalHeaderLabels([
            "Título", "Calificación", "Fecha", "Géneros"
        ])
        self.similarity_results_table.horizontalHeader().setStretchLastSection(True)
        results_layout.addWidget(self.similarity_results_table)
        
        layout.addWidget(results_group)
        
        self.tab_widget.addTab(tab, "🎯 Búsqueda Similares")
    
    def create_intelligent_search_tab(self):
        """Crea la pestaña de búsqueda inteligente"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Grupo de entrada
        input_group = QGroupBox("Búsqueda Inteligente")
        input_layout = QGridLayout(input_group)
        
        # Campo de título
        input_layout.addWidget(QLabel("Título (opcional):"), 0, 0)
        self.intelligent_title_input = QLineEdit()
        self.intelligent_title_input.setPlaceholderText("Ej: acción, ciencia ficción...")
        input_layout.addWidget(self.intelligent_title_input, 0, 1)
        
        # Campo de actores
        input_layout.addWidget(QLabel("Actores:"), 1, 0)
        self.intelligent_actors_input = QLineEdit()
        self.intelligent_actors_input.setPlaceholderText("Ej: Tom Holland, Robert Downey Jr.")
        input_layout.addWidget(self.intelligent_actors_input, 1, 1)
        
        # Campo de directores
        input_layout.addWidget(QLabel("Directores:"), 2, 0)
        self.intelligent_directors_input = QLineEdit()
        self.intelligent_directors_input.setPlaceholderText("Ej: Christopher Nolan, Quentin Tarantino")
        input_layout.addWidget(self.intelligent_directors_input, 2, 1)
        
        # Botón de búsqueda
        search_btn = QPushButton("🔍 Búsqueda Inteligente")
        search_btn.clicked.connect(self.intelligent_search)
        input_layout.addWidget(search_btn, 3, 0, 1, 2)
        
        layout.addWidget(input_group)
        
        # Tabla de resultados
        results_group = QGroupBox("Resultados")
        results_layout = QVBoxLayout(results_group)
        
        self.intelligent_results_table = QTableWidget()
        self.intelligent_results_table.setColumnCount(4)
        self.intelligent_results_table.setHorizontalHeaderLabels([
            "Título", "Calificación", "Fecha", "Géneros"
        ])
        self.intelligent_results_table.horizontalHeader().setStretchLastSection(True)
        results_layout.addWidget(self.intelligent_results_table)
        
        layout.addWidget(results_group)
        
        self.tab_widget.addTab(tab, "🎭 Búsqueda Inteligente")
    
    def create_prediction_tab(self):
        """Crea la pestaña de predicción de calificaciones"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Grupo de entrada
        input_group = QGroupBox("Predicción de Calificación")
        input_layout = QGridLayout(input_group)
        
        # Presupuesto
        input_layout.addWidget(QLabel("Presupuesto (USD):"), 0, 0)
        self.budget_input = QDoubleSpinBox()
        self.budget_input.setRange(0, 999999999)
        self.budget_input.setValue(50000000)
        self.budget_input.setSuffix(" USD")
        input_layout.addWidget(self.budget_input, 0, 1)
        
        # Popularidad
        input_layout.addWidget(QLabel("Popularidad (0-1000):"), 1, 0)
        self.popularity_input = QDoubleSpinBox()
        self.popularity_input.setRange(0, 1000)
        self.popularity_input.setValue(50)
        input_layout.addWidget(self.popularity_input, 1, 1)
        
        # Duración
        input_layout.addWidget(QLabel("Duración (minutos):"), 2, 0)
        self.runtime_input = QSpinBox()
        self.runtime_input.setRange(1, 500)
        self.runtime_input.setValue(120)
        self.runtime_input.setSuffix(" min")
        input_layout.addWidget(self.runtime_input, 2, 1)
        
        # Año
        input_layout.addWidget(QLabel("Año de lanzamiento:"), 3, 0)
        self.year_input = QSpinBox()
        self.year_input.setRange(1900, 2030)
        self.year_input.setValue(2024)
        input_layout.addWidget(self.year_input, 3, 1)
        
        # Número de géneros
        input_layout.addWidget(QLabel("Número de géneros:"), 4, 0)
        self.genres_input = QSpinBox()
        self.genres_input.setRange(1, 10)
        self.genres_input.setValue(2)
        input_layout.addWidget(self.genres_input, 4, 1)
        
        # Número de actores
        input_layout.addWidget(QLabel("Número de actores principales:"), 5, 0)
        self.cast_input = QSpinBox()
        self.cast_input.setRange(1, 50)
        self.cast_input.setValue(5)
        input_layout.addWidget(self.cast_input, 5, 1)
        
        # Botón de predicción
        predict_btn = QPushButton("🔮 Predecir Calificación")
        predict_btn.clicked.connect(self.predict_rating)
        input_layout.addWidget(predict_btn, 6, 0, 1, 2)
        
        layout.addWidget(input_group)
        
        # Resultado de predicción
        result_group = QGroupBox("Resultado de Predicción")
        result_layout = QVBoxLayout(result_group)
        
        self.prediction_result = QLabel("La calificación predicha aparecerá aquí...")
        self.prediction_result.setAlignment(Qt.AlignCenter)
        self.prediction_result.setFont(QFont("Arial", 16))
        self.prediction_result.setStyleSheet("""
            QLabel {
                background-color: #ecf0f1;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 20px;
                color: #2c3e50;
            }
        """)
        result_layout.addWidget(self.prediction_result)
        
        layout.addWidget(result_group)
        
        self.tab_widget.addTab(tab, "🔮 Predicción")
    
    def show_loading_screen(self):
        """Muestra pantalla de carga mientras se inicializa el sistema"""
        self.progress_dialog = QProgressDialog("Cargando sistema...", None, 0, 0, self)
        self.progress_dialog.setWindowTitle("Iniciando Sistema de Recomendación")
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.show()
        
        # Iniciar carga en hilo separado
        self.loading_worker = LoadingWorker()
        self.loading_worker.progress.connect(self.update_loading_progress)
        self.loading_worker.finished.connect(self.loading_finished)
        self.loading_worker.start()
    
    def update_loading_progress(self, message):
        """Actualiza el mensaje de progreso"""
        self.progress_dialog.setLabelText(message)
    
    def loading_finished(self, success, message):
        """Maneja la finalización de la carga"""
        self.progress_dialog.close()
        
        if success:
            self.recommender = self.loading_worker.recommender
            self.predictor = self.loading_worker.predictor
            self.tab_widget.setEnabled(True)
            
            # Mostrar mensaje de éxito
            QMessageBox.information(
                self, 
                "Sistema Listo", 
                "¡El sistema de recomendación está listo para usar!\n\n"
                f"Películas cargadas: {len(self.loading_worker.data_loader.df)}"
            )
        else:
            QMessageBox.critical(
                self, 
                "Error de Carga", 
                f"No se pudo cargar el sistema:\n{message}"
            )
            self.close()
    
    def search_similar_movies(self):
        """Busca películas similares por título"""
        title = self.similarity_title_input.text().strip()
        
        if not title:
            QMessageBox.warning(self, "Entrada Vacía", "Por favor, ingresa un título de película.")
            return
        
        try:
            results, error = self.recommender.buscar_peliculas_similares(title, 10)
            
            if error:
                QMessageBox.warning(self, "Error", error)
                return
            
            self.populate_results_table(self.similarity_results_table, results)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")
    
    def intelligent_search(self):
        """Realiza búsqueda inteligente"""
        title = self.intelligent_title_input.text().strip()
        actors = self.intelligent_actors_input.text().strip()
        directors = self.intelligent_directors_input.text().strip()
        
        if not any([title, actors, directors]):
            QMessageBox.warning(
                self, 
                "Entrada Vacía", 
                "Por favor, ingresa al menos un criterio de búsqueda."
            )
            return
        
        try:
            results, error = self.recommender.buscar_inteligente(
                pelicula=title,
                actores=actors, 
                directores=directors,
                top_n=10
            )
            
            if error:
                QMessageBox.warning(self, "Error", error)
                return
            
            self.populate_results_table(self.intelligent_results_table, results)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")
    
    def predict_rating(self):
        """Predice la calificación de una película"""
        try:
            budget = self.budget_input.value()
            popularity = self.popularity_input.value()
            runtime = self.runtime_input.value()
            year = self.year_input.value()
            num_genres = self.genres_input.value()
            num_cast = self.cast_input.value()
            
            # Validar rangos
            errors = self.predictor.validate_input_ranges(
                budget, popularity, runtime, year, num_genres, num_cast
            )
            
            if errors:
                QMessageBox.warning(
                    self, 
                    "Valores Inválidos", 
                    "Por favor, corrige los siguientes errores:\n\n" + "\n".join(errors)
                )
                return
            
            prediction, error = self.predictor.predict_rating(
                budget, popularity, runtime, year, num_genres, num_cast
            )
            
            if error:
                QMessageBox.warning(self, "Error", error)
                return
            
            # Mostrar resultado
            self.prediction_result.setText(
                f"🌟 Calificación Predicha: {prediction:.2f}/10.0\n\n"
                f"{'⭐' * int(prediction)} {'☆' * (10 - int(prediction))}"
            )
            
            # Cambiar color según la calificación
            if prediction >= 8:
                color = "#27ae60"  # Verde
            elif prediction >= 6:
                color = "#f39c12"  # Naranja
            else:
                color = "#e74c3c"  # Rojo
                
            self.prediction_result.setStyleSheet(f"""
                QLabel {{
                    background-color: {color};
                    border: 2px solid {color};
                    border-radius: 8px;
                    padding: 20px;
                    color: white;
                    font-weight: bold;
                }}
            """)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")
    
    def populate_results_table(self, table, results):
        """Llena la tabla con los resultados"""
        if results is None or results.empty:
            table.setRowCount(0)
            return
        
        table.setRowCount(len(results))
        
        for i, (_, row) in enumerate(results.iterrows()):
            # Título
            table.setItem(i, 0, QTableWidgetItem(str(row['title'])))
            
            # Calificación
            rating_item = QTableWidgetItem(f"{row['vote_average']:.1f}")
            rating_item.setTextAlignment(Qt.AlignCenter)
            table.setItem(i, 1, rating_item)
            
            # Fecha
            if 'release_date' in row and row['release_date']:
                date_str = str(row['release_date'])[:10]  # Solo la fecha, sin hora
            else:
                date_str = "N/A"
            table.setItem(i, 2, QTableWidgetItem(date_str))
            
            # Géneros
            if 'genres' in row and row['genres']:
                genres_str = ", ".join(row['genres'][:3])  # Primeros 3 géneros
                if len(row['genres']) > 3:
                    genres_str += "..."
            else:
                genres_str = "N/A"
            table.setItem(i, 3, QTableWidgetItem(genres_str))
        
        # Ajustar ancho de columnas
        table.resizeColumnsToContents()


def main():
    """Función principal"""
    app = QApplication(sys.argv)
    app.setApplicationName("Sistema de Recomendación de Películas")
    app.setApplicationVersion("1.0")
    
    # Configurar estilo de la aplicación
    app.setStyle('Fusion')
    
    window = MovieRecommendationApp()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
