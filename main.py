import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTextBrowser, QFileDialog, QMessageBox, QComboBox, QGridLayout, QGroupBox
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
#import pyqtdarktheme
from data import carica_pesi, carica_allenamenti, Peso, Allenamento, Nuoto, Corsa, Ciclismo, salva_pesi, salva_allenamenti
from dialogs import PesoDialog, AllenamentoDialog, StoricoDialog
from export import export_to_pdf
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import pandas as pd

# Stile CSS per un look moderno e scuro
STYLESHEET = """
QWidget {
    font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', sans-serif;
    font-size: 14px;
    color: #e0e0e0; /* Testo chiaro per contrasto */
}
QMainWindow {
    background-color: #2c2c2c; /* Sfondo principale scuro */
}
QDialog {
    background-color: #383838; /* Sfondo dialoghi leggermente più chiaro */
}
QLabel {
    color: #e0e0e0;
}
QLabel#title {
    font-size: 28px;
    font-weight: bold;
    color: #ffffff;
}
QLabel#subtitle {
    font-size: 16px;
    color: #cccccc;
    padding-bottom: 10px;
}
QPushButton {
    background-color: #2a8a2a; /* Verde */
    color: white;
    border: none;
    padding: 10px 15px;
    border-radius: 15px; /* Bordi più stondati */
    font-weight: bold;
}
QPushButton:hover {
    background-color: #3a9a3a; /* Verde più chiaro al passaggio */
}
QPushButton:pressed {
    background-color: #1a7a1a; /* Verde più scuro alla pressione */
}
QComboBox, QSpinBox, QDoubleSpinBox, QLineEdit, QDateEdit {
    padding: 8px;
    border: 1px solid #555;
    border-radius: 4px;
    background-color: #424242;
    color: #e0e0e0;
}
QTextBrowser, QListWidget {
    border: 1px solid #555;
    border-radius: 4px;
    background-color: #424242;
}
QGroupBox {
    font-weight: bold;
    border: 1px solid #555;
    border-radius: 5px;
    margin-top: 10px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top center; /* Centered title */
    padding: 0 10px;
    color: #e0e0e0;
}
"""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fitness Tracker Pro")
        self.setMinimumSize(1024, 768)
        self.setWindowIcon(QIcon.fromTheme("applications-fitness")) # Icona generica
        self.pesi = carica_pesi()
        self.allenamenti = carica_allenamenti()
        self.init_ui()

    def init_ui(self):
        # Layout principale
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header_layout = QVBoxLayout()
        title = QLabel("<h1>Fitness Tracker Pro</h1>")
        # title.setObjectName("title") # Non funziona come atteso con i tag h1
        subtitle = QLabel("Traccia i tuoi progressi e raggiungi i tuoi obiettivi")
        # subtitle.setObjectName("subtitle")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addLayout(header_layout)

        # Actions Toolbar
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)
        
        icon_size = QSize(24, 24)
        
        btn_peso = QPushButton(" Aggiungi Peso")
        btn_peso.setIcon(QIcon.fromTheme("list-add"))
        btn_peso.setIconSize(icon_size)
        
        btn_allen = QPushButton(" Aggiungi Allenamento")
        btn_allen.setIcon(QIcon.fromTheme("document-new"))
        btn_allen.setIconSize(icon_size)

        btn_storico = QPushButton(" Vedi Storico")
        btn_storico.setIcon(QIcon.fromTheme("view-history"))
        btn_storico.setIconSize(icon_size)
        
        btn_export = QPushButton(" Esporta PDF")
        btn_export.setIcon(QIcon.fromTheme("document-export"))
        btn_export.setIconSize(icon_size)

        btn_peso.clicked.connect(self.aggiungi_peso)
        btn_allen.clicked.connect(self.aggiungi_allenamento)
        btn_storico.clicked.connect(self.vedi_storico)
        btn_export.clicked.connect(self.esporta_pdf)
        
        actions_layout.addWidget(btn_peso)
        actions_layout.addWidget(btn_allen)
        actions_layout.addWidget(btn_storico)
        actions_layout.addWidget(btn_export)
        actions_layout.addStretch()
        
        # Filtro
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Tutti gli Sport", "Judo", "Nuoto", "Corsa", "Ciclismo"])
        self.filter_combo.currentTextChanged.connect(self.aggiorna_dashboard)
        actions_layout.addWidget(QLabel("Filtra per sport:"))
        actions_layout.addWidget(self.filter_combo)
        
        main_layout.addLayout(actions_layout)

        # Dashboard Grid
        dashboard_grid = QGridLayout()
        dashboard_grid.setSpacing(15)
        
        self.grafico_peso = FigureCanvas(plt.Figure(figsize=(6, 4)))
        self.grafico_torta = FigureCanvas(plt.Figure(figsize=(5, 4)))
        self.grafico_barre = FigureCanvas(plt.Figure(figsize=(5, 4)))
        
        dashboard_grid.addWidget(self.grafico_peso, 0, 0, 1, 2) # Span 2 colonne
        dashboard_grid.addWidget(self.grafico_torta, 1, 0)
        dashboard_grid.addWidget(self.grafico_barre, 1, 1)

        # Consigli
        self.consigli = QTextBrowser()
        self.consigli.setMinimumHeight(120)
        
        consigli_groupbox = QGroupBox("Consigli Personalizzati")
        consigli_layout = QVBoxLayout(consigli_groupbox)
        consigli_layout.addWidget(self.consigli)

        dashboard_grid.addWidget(consigli_groupbox, 2, 0, 1, 2) # Span 2 colonne
        
        main_layout.addLayout(dashboard_grid)
        
        self.setCentralWidget(main_widget)
        self.aggiorna_dashboard()

    def vedi_storico(self):
        dlg = StoricoDialog(self.allenamenti, self)
        dlg.exec()
        # Dopo la chiusura del dialogo, salva i dati e aggiorna il cruscotto
        salva_allenamenti(self.allenamenti)
        self.aggiorna_dashboard()

    def esporta_pdf(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Salva PDF", "", "PDF Files (*.pdf)")
        if filename:
            try:
                export_to_pdf(filename, self.pesi, self.allenamenti)
                QMessageBox.information(self, "Successo", "Dati esportati correttamente!")
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Errore durante l'esportazione: {e}")

    def aggiungi_peso(self):
        dlg = PesoDialog(self)
        if dlg.exec():
            data, valore = dlg.get_data()
            self.pesi.append(Peso(data, valore))
            salva_pesi(self.pesi)
            self.aggiorna_dashboard()

    def aggiungi_allenamento(self):
        dlg = AllenamentoDialog(self)
        if dlg.exec():
            d = dlg.get_data()
            if d['sport'] == 'Nuoto':
                self.allenamenti.append(Nuoto(
                    d['data'], d['durata'], d['calorie'],
                    d['stile'], d['vasche'], d['passo_medio'], d['passo_minimo'],
                    d['bracciata_media'], d['bracciata_massima'], d['note']
                ))
            elif d['sport'] == 'Corsa':
                self.allenamenti.append(Corsa(
                    d['data'], d['durata'], d['calorie'], d['battito'], d['distanza'],
                    d['passo_medio'], d['dislivello'], d['note']
                ))
            elif d['sport'] == 'Ciclismo':
                self.allenamenti.append(Ciclismo(
                    d['data'], d['durata'], d['calorie'], d['battito'], d['distanza'],
                    d['velocita_media'], d['velocita_massima'], d['dislivello'], d['note']
                ))
            else:
                self.allenamenti.append(Allenamento(d['data'], d['sport'], d['durata'], d['calorie'], d['battito'], d['note']))
            salva_allenamenti(self.allenamenti)
            self.aggiorna_dashboard()

    def aggiorna_dashboard(self):
        # Applica filtro
        sport_filter = self.filter_combo.currentText()
        allenamenti_filtrati = self.allenamenti
        if sport_filter != "Tutti gli Sport":
            allenamenti_filtrati = [a for a in self.allenamenti if a.sport == sport_filter]

        # Grafico peso
        self.grafico_peso.figure.clear()
        self.grafico_peso.figure.patch.set_facecolor('#2c2c2c')
        ax = self.grafico_peso.figure.add_subplot(111)
        ax.set_facecolor('#424242')
        if self.pesi:
            df_pesi = pd.DataFrame([vars(p) for p in self.pesi])
            # Converte la colonna 'data' in oggetti datetime per ordinamento e visualizzazione corretti
            df_pesi['data'] = pd.to_datetime(df_pesi['data'], dayfirst=True, errors='coerce')
            df_pesi.dropna(subset=['data'], inplace=True) # Rimuove date non valide
            df_pesi.sort_values(by='data', inplace=True)

            ax.plot(df_pesi['data'], df_pesi['valore'], marker='o', color='#82b1ff')
            ax.set_title('Peso nel tempo', color='white')
            ax.set_ylabel('Kg', color='white')
            ax.grid(True, alpha=0.3)
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white') 
            ax.spines['right'].set_color('white')
            ax.spines['left'].set_color('white')
        else:
            ax.text(0.5, 0.5, 'Nessun dato peso', ha='center', va='center', color='white')
        self.grafico_peso.draw()
        
        # Grafico torta tempo per sport
        self.grafico_torta.figure.clear()
        self.grafico_torta.figure.patch.set_facecolor('#2c2c2c')
        ax2 = self.grafico_torta.figure.add_subplot(111)
        if allenamenti_filtrati:
            df = pd.DataFrame([vars(a) for a in allenamenti_filtrati])
            sport_time = df.groupby('sport')['durata'].sum()
            wedges, texts, autotexts = ax2.pie(sport_time, autopct='%1.0f%%', startangle=90, textprops=dict(color="w"))
            ax2.legend(wedges, sport_time.index, title="Sport", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            ax2.set_title('Tempo per sport', color='white')
        else:
            ax2.text(0.5, 0.5, 'Nessun allenamento', ha='center', va='center', color='white')
        self.grafico_torta.draw()
        
        # Grafico barre calorie per sport
        self.grafico_barre.figure.clear()
        self.grafico_barre.figure.patch.set_facecolor('#2c2c2c')
        ax3 = self.grafico_barre.figure.add_subplot(111)
        ax3.set_facecolor('#424242')
        if allenamenti_filtrati:
            df = pd.DataFrame([vars(a) for a in allenamenti_filtrati])
            sport_cal = df.groupby('sport')['calorie'].sum()
            sport_cal.plot(kind='bar', ax=ax3, color=['#ff8a65','#4dd0e1','#f06292', '#7986cb'])
            ax3.set_title('Calorie per sport', color='white')
            ax3.set_ylabel('Kcal', color='white')
            ax3.tick_params(axis='x', colors='white', rotation=0)
            ax3.tick_params(axis='y', colors='white')
            ax3.spines['bottom'].set_color('white')
            ax3.spines['top'].set_color('white') 
            ax3.spines['right'].set_color('white')
            ax3.spines['left'].set_color('white')
        else:
            ax3.text(0.5, 0.5, 'Nessun allenamento', ha='center', va='center', color='white')
        self.grafico_barre.draw()
        # Consigli
        self.consigli.setText(self.genera_consigli(allenamenti_filtrati))

    def genera_consigli(self, allenamenti_filtrati):
        consigli = []
        if self.pesi:
            # Crea un DataFrame per ordinare correttamente per data
            df_pesi = pd.DataFrame([vars(p) for p in self.pesi])
            # Converte la colonna 'data' in oggetti datetime, gestendo formati diversi
            df_pesi['data'] = pd.to_datetime(df_pesi['data'], dayfirst=True, errors='coerce')
            df_pesi.dropna(subset=['data'], inplace=True) # Rimuove date non valide
            df_pesi.sort_values(by='data', inplace=True)
            
            if not df_pesi.empty:
                pesi_recenti = df_pesi['valore'].tail(7).tolist()
                if len(pesi_recenti) > 1 and pesi_recenti[-1] > pesi_recenti[0]:
                    consigli.append("Il tuo peso è in aumento. Valuta di aumentare l'attività aerobica.")
                elif len(pesi_recenti) > 1 and pesi_recenti[-1] < pesi_recenti[0]:
                    consigli.append("Ottimo! Il tuo peso è in calo.")

        if allenamenti_filtrati:
            df = pd.DataFrame([vars(a) for a in allenamenti_filtrati])
            if (df['battito'] > 170).any():
                consigli.append("Attenzione: battito elevato in alcuni allenamenti. Valuta più recupero.")
            if (df['durata'] < 20).all():
                consigli.append("Prova ad aumentare la durata degli allenamenti per maggior beneficio.")
            if 'Nuoto' in df['sport'].values:
                nuoto_df = df[df['sport']=='Nuoto'].copy()
                if 'passo_minimo' in nuoto_df.columns and (nuoto_df['passo_minimo'] < 1.5).any():
                    consigli.append("Ottimo passo minimo nel nuoto! Continua così.")
                if 'bracciata_massima' in nuoto_df.columns and (nuoto_df['bracciata_massima'] > 40).any():
                    consigli.append("Frequenza di bracciata massima eccellente!")
                elif 'bracciata_media' in nuoto_df.columns and (nuoto_df['bracciata_media'] < 25).any():
                    consigli.append("Puoi provare ad aumentare la frequenza delle bracciate nel nuoto.")
            if 'Ciclismo' in df['sport'].values:
                ciclismo_df = df[df['sport']=='Ciclismo'].copy()
                if 'velocita_media' in ciclismo_df.columns and (ciclismo_df['velocita_media'] > 25).any():
                    consigli.append("Velocità media eccezionale nel ciclismo! Grande performance.")
                if 'dislivello' in ciclismo_df.columns and ciclismo_df['dislivello'].sum() > 1000:
                    consigli.append("Hai superato i 1000m di dislivello totale nel ciclismo questa settimana, ottimo lavoro in salita!")
        if not consigli:
            return "Continua così!"
        return '\n'.join(consigli)

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    #pyqtdarktheme.setup_theme("dark")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 