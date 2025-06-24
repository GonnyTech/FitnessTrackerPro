from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QDateEdit, QSpinBox, QTextEdit, QWidget, QFormLayout, QDoubleSpinBox, QListWidget, QListWidgetItem, QMessageBox
from PySide6.QtCore import QDate, Qt
from data import Allenamento, Nuoto, Corsa, Ciclismo
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class PesoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Aggiungi Peso")
        layout = QVBoxLayout()
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.valore_edit = QLineEdit()
        self.valore_edit.setPlaceholderText("Peso in kg")
        btns = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Annulla")
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        btns.addWidget(ok_btn)
        btns.addWidget(cancel_btn)
        layout.addWidget(QLabel("Data:"))
        layout.addWidget(self.date_edit)
        layout.addWidget(QLabel("Peso (kg):"))
        layout.addWidget(self.valore_edit)
        layout.addLayout(btns)
        self.setLayout(layout)
    def get_data(self):
        return self.date_edit.date().toString("yyyy-MM-dd"), float(self.valore_edit.text())

class AllenamentoDialog(QDialog):
    def __init__(self, parent=None, allenamento=None):
        super().__init__(parent)
        self.setWindowTitle("Dettagli Allenamento")
        self.allenamento = allenamento
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout()
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.sport_combo = QComboBox()
        self.sport_combo.addItems(["Judo", "Nuoto", "Corsa", "Ciclismo"])
        self.sport_combo.currentTextChanged.connect(self.update_specific_widgets)
        self.durata_edit = QSpinBox()
        self.durata_edit.setRange(1, 600)
        self.durata_edit.setSuffix(" min")
        self.calorie_edit = QSpinBox()
        self.calorie_edit.setRange(0, 5000)
        self.calorie_edit.setSuffix(" kcal")
        self.battito_edit = QSpinBox()
        self.battito_edit.setRange(30, 250)
        self.battito_edit.setSuffix(" bpm")
        self.battito_label = QLabel("Battito medio:")
        self.note_edit = QTextEdit()

        # Nuoto specifico
        self.nuoto_widget = QWidget()
        nuoto_layout = QFormLayout()
        self.stile_combo = QComboBox()
        self.stile_combo.addItems(["Libero", "Dorso", "Rana", "Farfalla", "Misti"])
        self.vasche_edit = QSpinBox()
        self.vasche_edit.setRange(0, 500)
        self.passo_medio_edit = QDoubleSpinBox()
        self.passo_medio_edit.setRange(0, 10)
        self.passo_medio_edit.setSuffix(" min/100m")
        self.passo_medio_edit.setSingleStep(0.1)
        self.passo_minimo_edit = QDoubleSpinBox()
        self.passo_minimo_edit.setRange(0, 10)
        self.passo_minimo_edit.setSuffix(" min/100m")
        self.passo_minimo_edit.setSingleStep(0.1)
        self.bracciata_media_edit = QSpinBox()
        self.bracciata_media_edit.setRange(0, 100)
        self.bracciata_media_edit.setSuffix(" br/min")
        self.bracciata_massima_edit = QSpinBox()
        self.bracciata_massima_edit.setRange(0, 100)
        self.bracciata_massima_edit.setSuffix(" br/min")
        
        nuoto_layout.addRow(QLabel("Stile:"), self.stile_combo)
        nuoto_layout.addRow(QLabel("Vasche:"), self.vasche_edit)
        nuoto_layout.addRow(QLabel("Passo medio:"), self.passo_medio_edit)
        nuoto_layout.addRow(QLabel("Passo minimo:"), self.passo_minimo_edit)
        nuoto_layout.addRow(QLabel("Bracciata media:"), self.bracciata_media_edit)
        nuoto_layout.addRow(QLabel("Bracciata massima:"), self.bracciata_massima_edit)

        self.nuoto_widget.setLayout(nuoto_layout)

        # Corsa specifico
        self.corsa_widget = QWidget()
        corsa_layout = QFormLayout()
        self.distanza_edit = QDoubleSpinBox()
        self.distanza_edit.setRange(0, 200)
        self.distanza_edit.setSuffix(" km")
        self.distanza_edit.setSingleStep(0.1)
        self.passo_medio_corsa_edit = QDoubleSpinBox()
        self.passo_medio_corsa_edit.setRange(0, 20)
        self.passo_medio_corsa_edit.setSuffix(" min/km")
        self.passo_medio_corsa_edit.setSingleStep(0.1)
        self.dislivello_edit = QSpinBox()
        self.dislivello_edit.setRange(0, 10000)
        self.dislivello_edit.setSuffix(" m")
        corsa_layout.addRow(QLabel("Distanza:"), self.distanza_edit)
        corsa_layout.addRow(QLabel("Passo medio:"), self.passo_medio_corsa_edit)
        corsa_layout.addRow(QLabel("Dislivello:"), self.dislivello_edit)
        self.corsa_widget.setLayout(corsa_layout)

        # Ciclismo specifico
        self.ciclismo_widget = QWidget()
        ciclismo_layout = QFormLayout()
        self.distanza_ciclismo_edit = QDoubleSpinBox()
        self.distanza_ciclismo_edit.setRange(0, 500)
        self.distanza_ciclismo_edit.setSuffix(" km")
        self.velocita_media_edit = QDoubleSpinBox()
        self.velocita_media_edit.setRange(0, 100)
        self.velocita_media_edit.setSuffix(" km/h")
        self.velocita_massima_edit = QDoubleSpinBox()
        self.velocita_massima_edit.setRange(0, 150)
        self.velocita_massima_edit.setSuffix(" km/h")
        self.dislivello_ciclismo_edit = QSpinBox()
        self.dislivello_ciclismo_edit.setRange(0, 10000)
        self.dislivello_ciclismo_edit.setSuffix(" m")
        ciclismo_layout.addRow(QLabel("Distanza:"), self.distanza_ciclismo_edit)
        ciclismo_layout.addRow(QLabel("Velocità media:"), self.velocita_media_edit)
        ciclismo_layout.addRow(QLabel("Velocità massima:"), self.velocita_massima_edit)
        ciclismo_layout.addRow(QLabel("Dislivello:"), self.dislivello_ciclismo_edit)
        self.ciclismo_widget.setLayout(ciclismo_layout)

        # Pulsanti
        btns = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Annulla")
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        btns.addWidget(ok_btn)
        btns.addWidget(cancel_btn)
        # Layout
        layout.addWidget(QLabel("Data:"))
        layout.addWidget(self.date_edit)
        layout.addWidget(QLabel("Sport:"))
        layout.addWidget(self.sport_combo)
        layout.addWidget(QLabel("Durata:"))
        layout.addWidget(self.durata_edit)
        layout.addWidget(QLabel("Calorie:"))
        layout.addWidget(self.calorie_edit)
        layout.addWidget(self.battito_label)
        layout.addWidget(self.battito_edit)
        layout.addWidget(QLabel("Note:"))
        layout.addWidget(self.note_edit)
        layout.addWidget(self.nuoto_widget)
        layout.addWidget(self.corsa_widget)
        layout.addWidget(self.ciclismo_widget)
        layout.addLayout(btns)
        self.setLayout(layout)
        self.update_specific_widgets(self.sport_combo.currentText())

        if self.allenamento:
            self.populate_form()

    def populate_form(self):
        self.date_edit.setDate(QDate.fromString(self.allenamento.data, "yyyy-MM-dd"))
        self.sport_combo.setCurrentText(self.allenamento.sport)
        self.durata_edit.setValue(self.allenamento.durata)
        self.calorie_edit.setValue(self.allenamento.calorie)
        self.note_edit.setText(str(self.allenamento.note) if pd.notna(self.allenamento.note) else "")

        if isinstance(self.allenamento, Nuoto):
            self.battito_edit.setValue(0) # Non usato per Nuoto
            self.stile_combo.setCurrentText(self.allenamento.stile)
            self.vasche_edit.setValue(self.allenamento.vasche)
            self.passo_medio_edit.setValue(self.allenamento.passo_medio)
            self.passo_minimo_edit.setValue(self.allenamento.passo_minimo)
            self.bracciata_media_edit.setValue(self.allenamento.bracciata_media)
            self.bracciata_massima_edit.setValue(self.allenamento.bracciata_massima)
        elif isinstance(self.allenamento, Corsa):
            self.battito_edit.setValue(self.allenamento.battito)
            self.distanza_edit.setValue(self.allenamento.distanza)
            self.passo_medio_corsa_edit.setValue(self.allenamento.passo_medio)
            self.dislivello_edit.setValue(self.allenamento.dislivello)
        elif isinstance(self.allenamento, Ciclismo):
            self.battito_edit.setValue(self.allenamento.battito)
            self.distanza_ciclismo_edit.setValue(self.allenamento.distanza)
            self.velocita_media_edit.setValue(self.allenamento.velocita_media)
            self.velocita_massima_edit.setValue(self.allenamento.velocita_massima)
            self.dislivello_ciclismo_edit.setValue(self.allenamento.dislivello)
        else: # Allenamento generico
            self.battito_edit.setValue(self.allenamento.battito)

    def update_specific_widgets(self, sport):
        is_nuoto = sport == "Nuoto"
        is_corsa = sport == "Corsa"
        is_ciclismo = sport == "Ciclismo"

        self.nuoto_widget.setVisible(is_nuoto)
        self.corsa_widget.setVisible(is_corsa)
        self.ciclismo_widget.setVisible(is_ciclismo)

        self.battito_label.setVisible(not is_nuoto)
        self.battito_edit.setVisible(not is_nuoto)

    def get_data(self):
        sport = self.sport_combo.currentText()
        data = self.date_edit.date().toString("yyyy-MM-dd")
        durata = self.durata_edit.value()
        calorie = self.calorie_edit.value()
        battito = self.battito_edit.value()
        note = self.note_edit.toPlainText()
        if sport == "Nuoto":
            return dict(data=data, sport=sport, durata=durata, calorie=calorie, battito=0, note=note, 
                        stile=self.stile_combo.currentText(),
                        vasche=self.vasche_edit.value(),
                        passo_medio=self.passo_medio_edit.value(),
                        passo_minimo=self.passo_minimo_edit.value(),
                        bracciata_media=self.bracciata_media_edit.value(),
                        bracciata_massima=self.bracciata_massima_edit.value())
        elif sport == "Corsa":
            return dict(data=data, sport=sport, durata=durata, calorie=calorie, battito=battito, note=note,
                        distanza=self.distanza_edit.value(),
                        passo_medio=self.passo_medio_corsa_edit.value(),
                        dislivello=self.dislivello_edit.value())
        elif sport == "Ciclismo":
            return dict(data=data, sport=sport, durata=durata, calorie=calorie, battito=battito, note=note,
                        distanza=self.distanza_ciclismo_edit.value(),
                        velocita_media=self.velocita_media_edit.value(),
                        velocita_massima=self.velocita_massima_edit.value(),
                        dislivello=self.dislivello_ciclismo_edit.value())
        else:
            return dict(data=data, sport=sport, durata=durata, calorie=calorie, battito=battito, note=note)

class StoricoDialog(QDialog):
    def __init__(self, allenamenti, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Storico Allenamenti")
        self.allenamenti = allenamenti
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout()
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.SingleSelection)
        self.populate_list()

        btn_layout = QHBoxLayout()
        view_btn = QPushButton("Vedi Dettagli")
        edit_btn = QPushButton("Modifica Selezionato")
        delete_btn = QPushButton("Elimina Selezionato")
        close_btn = QPushButton("Chiudi")

        btn_layout.addStretch()
        btn_layout.addWidget(view_btn)
        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(close_btn)

        layout.addWidget(QLabel("Storico degli allenamenti (doppio click per modificare):"))
        layout.addWidget(self.list_widget)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        view_btn.clicked.connect(self.view_details)
        edit_btn.clicked.connect(self.edit_selected)
        self.list_widget.itemDoubleClicked.connect(self.edit_selected)
        delete_btn.clicked.connect(self.delete_selected)
        close_btn.clicked.connect(self.accept)

    def populate_list(self):
        self.list_widget.clear()
        # Sort by date, newest first
        allenamenti_ordinati = sorted(self.allenamenti, key=lambda x: x.data, reverse=True)
        for allenamento in allenamenti_ordinati:
            if hasattr(allenamento, 'stile'):  # Nuoto
                text = f"{allenamento.data} - {allenamento.sport} ({allenamento.stile}) - {allenamento.durata} min, {allenamento.vasche} vasche"
            elif hasattr(allenamento, 'velocita_media'): # Ciclismo
                text = f"{allenamento.data} - {allenamento.sport} - {allenamento.distanza} km, {allenamento.velocita_media} km/h"
            elif hasattr(allenamento, 'distanza'): # Corsa
                text = f"{allenamento.data} - {allenamento.sport} - {allenamento.distanza} km, {allenamento.passo_medio} min/km"
            else:
                text = f"{allenamento.data} - {allenamento.sport} - {allenamento.durata} min, {allenamento.calorie} kcal"
            
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, allenamento)
            self.list_widget.addItem(item)

    def view_details(self):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Attenzione", "Nessun allenamento selezionato.")
            return

        allenamento_selezionato = selected_items[0].data(Qt.UserRole)
        # Filtra per ottenere solo gli allenamenti dello stesso sport
        allenamenti_tipo_simile = [a for a in self.allenamenti if a.sport == allenamento_selezionato.sport]
        
        dlg = DettaglioAllenamentoDialog(allenamento_selezionato, allenamenti_tipo_simile, self)
        dlg.exec()

    def edit_selected(self):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Attenzione", "Nessun allenamento selezionato.")
            return

        allenamento_to_edit = selected_items[0].data(Qt.UserRole)
        dlg = AllenamentoDialog(parent=self, allenamento=allenamento_to_edit)
        
        if dlg.exec():
            new_data = dlg.get_data()
            try:
                # Find the original object in the list
                idx = self.allenamenti.index(allenamento_to_edit)
                # Create a new object based on the possibly changed sport
                if new_data['sport'] == 'Nuoto':
                    new_allenamento = Nuoto(
                        data=new_data['data'], durata=new_data['durata'], calorie=new_data['calorie'],
                        stile=new_data['stile'], vasche=new_data['vasche'], passo_medio=new_data['passo_medio'],
                        passo_minimo=new_data['passo_minimo'], bracciata_media=new_data['bracciata_media'],
                        bracciata_massima=new_data['bracciata_massima'], note=new_data['note']
                    )
                elif new_data['sport'] == 'Corsa':
                    new_allenamento = Corsa(
                        data=new_data['data'], durata=new_data['durata'], calorie=new_data['calorie'],
                        battito=new_data['battito'], distanza=new_data['distanza'],
                        passo_medio=new_data['passo_medio'], dislivello=new_data['dislivello'], note=new_data['note']
                    )
                elif new_data['sport'] == 'Ciclismo':
                    new_allenamento = Ciclismo(
                        data=new_data['data'], durata=new_data['durata'], calorie=new_data['calorie'],
                        battito=new_data['battito'], distanza=new_data['distanza'],
                        velocita_media=new_data['velocita_media'], velocita_massima=new_data['velocita_massima'],
                        dislivello=new_data['dislivello'], note=new_data['note']
                    )
                else:
                    new_allenamento = Allenamento(
                        data=new_data['data'], sport=new_data['sport'], durata=new_data['durata'],
                        calorie=new_data['calorie'], battito=new_data['battito'], note=new_data['note']
                    )
                # Replace the old object with the new one
                self.allenamenti[idx] = new_allenamento
                self.populate_list()
            except ValueError:
                QMessageBox.critical(self, "Errore", "Errore interno, impossibile trovare l'allenamento da modificare.")

    def delete_selected(self):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Attenzione", "Nessun allenamento selezionato.")
            return

        reply = QMessageBox.question(self, "Conferma Eliminazione",
                                     f"Sei sicuro di voler eliminare i {len(selected_items)} allenamenti selezionati?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            for item in selected_items:
                allenamento_to_delete = item.data(Qt.UserRole)
                try:
                    self.allenamenti.remove(allenamento_to_delete)
                except ValueError:
                    # Could happen if the list is manipulated elsewhere, but unlikely.
                    pass
            self.populate_list()

class DettaglioAllenamentoDialog(QDialog):
    def __init__(self, allenamento, allenamenti_simili, parent=None):
        super().__init__(parent)
        self.allenamento = allenamento
        self.allenamenti_simili = allenamenti_simili
        self.setWindowTitle(f"Dettaglio Allenamento - {allenamento.sport}")
        self.setMinimumSize(500, 600)

        layout = QVBoxLayout()
        
        # Summary
        summary_text = self.get_summary_text()
        layout.addWidget(QLabel(summary_text))
        
        # Grafico
        self.grafico = FigureCanvas(plt.Figure(figsize=(5,4)))
        self.create_comparison_chart()
        layout.addWidget(self.grafico)

        # Close button
        close_btn = QPushButton("Chiudi")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)

    def get_summary_text(self):
        text = f"<b>Data:</b> {self.allenamento.data}<br>"
        text += f"<b>Durata:</b> {self.allenamento.durata} min<br>"
        text += f"<b>Calorie:</b> {self.allenamento.calorie} kcal<br>"
        
        if isinstance(self.allenamento, Nuoto):
            text += f"<b>Stile:</b> {self.allenamento.stile}<br>"
            text += f"<b>Vasche:</b> {self.allenamento.vasche}<br>"
            text += f"<b>Passo Medio:</b> {self.allenamento.passo_medio:.2f} min/100m<br>"
        elif isinstance(self.allenamento, Corsa):
            text += f"<b>Distanza:</b> {self.allenamento.distanza} km<br>"
            text += f"<b>Passo Medio:</b> {self.allenamento.passo_medio:.2f} min/km<br>"
            text += f"<b>Dislivello:</b> {self.allenamento.dislivello} m<br>"
        elif isinstance(self.allenamento, Ciclismo):
            text += f"<b>Distanza:</b> {self.allenamento.distanza} km<br>"
            text += f"<b>Velocità Media:</b> {self.allenamento.velocita_media:.1f} km/h<br>"
            text += f"<b>Velocità Massima:</b> {self.allenamento.velocita_massima:.1f} km/h<br>"
            text += f"<b>Dislivello:</b> {self.allenamento.dislivello} m<br>"
        
        if self.allenamento.note:
             text += f"<b>Note:</b> {self.allenamento.note}<br>"
             
        return text

    def create_comparison_chart(self):
        df = pd.DataFrame([vars(a) for a in self.allenamenti_simili])
        self.grafico.figure.patch.set_facecolor('#383838')
        ax = self.grafico.figure.add_subplot(111)
        ax.set_facecolor('#424242')

        metrics_to_compare = ['durata', 'calorie']
        if isinstance(self.allenamento, Corsa) or isinstance(self.allenamento, Ciclismo):
            metrics_to_compare.append('distanza')

        avg_values = df[metrics_to_compare].mean()
        current_values = pd.Series(vars(self.allenamento))[metrics_to_compare]
        
        chart_df = pd.DataFrame({'Questo Allenamento': current_values, 'Media Sport': avg_values})
        chart_df.plot(kind='bar', ax=ax, colormap='viridis')
        
        ax.set_title('Confronto con la Media', color='white')
        ax.set_ylabel('Valori', color='white')
        ax.tick_params(axis='x', rotation=0, colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white') 
        ax.spines['right'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.legend(labelcolor='white')
        self.grafico.draw() 