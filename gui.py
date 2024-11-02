import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QComboBox, QLabel, QVBoxLayout, QDialog, QPushButton, QDateEdit
from PyQt5.QtCore import QDate
from db_manager import see_team_game, see_tournament, see_top_teams, team_statistics,create_view_cards, see_cards
from main import start_scraper


class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        create_view_cards()
        self.setWindowTitle('Consulta de Jogos de Futebol')
        self.setGeometry(100, 100, 800, 600)

        layout = QtWidgets.QVBoxLayout()

        self.input = QtWidgets.QLineEdit(self)
        layout.addWidget(self.input)

        self.button = QtWidgets.QPushButton('Buscar Jogos', self)
        layout.addWidget(self.button)

        self.button.clicked.connect(self.on_search)

        self.table = QtWidgets.QTableWidget(self)
        layout.addWidget(self.table)

        self.search_type = QComboBox(self)
        self.search_type.addItems(["Jogos do time",
                                   "Estatisticas do time (Escolher tipo abaixo)",
                                   "Cartões do time",
                                   "Times com mais gols", "Time no torneio"])
        layout.addWidget(self.search_type)

        self.statistic_type = QComboBox(self)
        self.statistic_type.addItems(["Attack", "Shots", "Duels", "Passes",
                                      "Defending", "Goalkeeping"])

        layout.addWidget(self.statistic_type)

        bottom_layout = QtWidgets.QHBoxLayout()

        bottom_layout.addStretch(1)

        self.reset_data = QtWidgets.QPushButton('Resetar Dados', self)
        bottom_layout.addWidget(self.reset_data)

        self.reset_data.clicked.connect(self.reset_data_window)

        layout.addLayout(bottom_layout)

        self.setLayout(layout)

    def on_search(self):
        text = self.input.text()
        selected_option = self.search_type.currentText()
        statistic = self.statistic_type.currentText()
        print(f"TEXTO PESQUISADO: {text}")
        print(f"Statistic choosen:{statistic}")
        print(f'Opção selecionada: {selected_option}')

        if selected_option == "Jogos do time":
            results, colnames = see_team_game(text)
        elif selected_option == "Estatisticas do time (Escolher tipo abaixo)":
            print("BUSCANDO ESTATISTICAS")
            results, colnames = team_statistics(text, statistic)
        elif selected_option == "Cartões do time":
            results, colnames = see_cards(text)
        elif selected_option == "Times com mais gols":
            results, colnames = see_top_teams(text)
        elif selected_option == "Time no torneio":
            results, colnames = see_tournament(text)
        else:
            results, colnames = [], []

        self.update_table(results, colnames)

    def update_table(self, results, colnames):
        self.table.setRowCount(len(results))
        self.table.setColumnCount(len(results[0]))
        self.table.setHorizontalHeaderLabels(colnames)

        for i, row in enumerate(results):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))

    def reset_data_window(self):
        self.popup = Reset_Window()
        self.popup.exec_()


class Reset_Window(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('RESETAR OS DADOS?')
        self.setGeometry(150, 150, 300, 200)

        warning = "RESETAR DADOS PODE SER UM PROCESSO LENTO, TEM CERTEZA QUE DESEJA PROSSEGUIR?"
        layout = QVBoxLayout()
        layout.addWidget(QLabel(warning))

        instructions = "Se sim, insira a data da qual você deseja que começe a coleta de dados"
        instructions += "\nOs dados novos serão coletados a partir dessa data, até o dia de ontem"
        instructions += "\nApós clicar em Confirmar Data, espere até que apareça o aviso 'Dados resetados para fechar e abrir a aplicação'"
        layout.addWidget(QLabel(instructions))

        self.setLayout(layout)

        self.date_edit = QDateEdit(self)
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        layout.addWidget(self.date_edit)

        confirm_button = QPushButton("Confirmar Data", self)
        confirm_button.clicked.connect(self.confirm_date)
        layout.addWidget(confirm_button)

        self.setLayout(layout)

    def confirm_date(self):
        selected_date = self.date_edit.date().toString("yyyy-MM-dd")
        print(f"Data selecionada: {selected_date}")
        start_scraper(selected_date)
        self.accept()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
