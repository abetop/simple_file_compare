#-------------------------------------------------------------------------------
# Name:        main
# Purpose:
#
# Author:      abetop
#
# Created:     26/11/2023
# Copyright:   (c) abetop 2023
# Licence:     GNU General Public License v3.0
#-------------------------------------------------------------------------------

import filecmp
import difflib
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog
from PyQt5.QtCore import Qt, QSettings

class FileComparator(QWidget):
    def __init__(self):
        super(FileComparator, self).__init__()

        # Configuración de la aplicación
        self.settings = QSettings("MiEmpresa", "ComparadorDeArchivos")

        self.init_ui()

    def init_ui(self):
        # Widgets
        self.file1_label = QLabel('Nombre del primer archivo:')
        self.file1_edit = QLineEdit(self)
        self.file1_button = QPushButton('Seleccionar archivo', self)

        self.file2_label = QLabel('Nombre del segundo archivo:')
        self.file2_edit = QLineEdit(self)
        self.file2_button = QPushButton('Seleccionar archivo', self)

        self.file3_label = QLabel('Nombre del tercer archivo:')
        self.file3_edit = QLineEdit(self)
        self.file3_button = QPushButton('Seleccionar archivo', self)

        self.compare_button = QPushButton('Comparar archivos', self)
        self.clear_button = QPushButton('Limpiar', self)
        self.exit_button = QPushButton('Salir', self)

        self.console_output = QTextEdit(self)
        self.console_output.setReadOnly(True)

        # Layout
        vbox = QVBoxLayout()

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.file1_label)
        hbox1.addWidget(self.file1_edit)
        hbox1.addWidget(self.file1_button)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.file2_label)
        hbox2.addWidget(self.file2_edit)
        hbox2.addWidget(self.file2_button)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.file3_label)
        hbox3.addWidget(self.file3_edit)
        hbox3.addWidget(self.file3_button)

        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addWidget(self.compare_button)
        vbox.addWidget(self.clear_button)
        vbox.addWidget(self.exit_button)
        vbox.addWidget(self.console_output)

        self.setLayout(vbox)

        # Signals
        self.file1_button.clicked.connect(self.select_file1)
        self.file2_button.clicked.connect(self.select_file2)
        self.file3_button.clicked.connect(self.select_file3)
        self.compare_button.clicked.connect(self.compare_files)
        self.clear_button.clicked.connect(self.clear_output)
        self.exit_button.clicked.connect(self.close_application)

        # Inicialización de rutas desde la última sesión
        self.file1_edit.setText(self.settings.value("last_file1", ""))
        self.file2_edit.setText(self.settings.value("last_file2", ""))
        self.file3_edit.setText(self.settings.value("last_file3", ""))

        # Window settings
        self.setGeometry(300, 300, 500, 300)
        self.setWindowTitle('Comparador de Archivos')
        self.show()

    def select_file1(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Seleccionar primer archivo', self.file1_edit.text())
        if filename:
            self.file1_edit.setText(filename)
            self.settings.setValue("last_file1", filename)

    def select_file2(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Seleccionar segundo archivo', self.file2_edit.text())
        if filename:
            self.file2_edit.setText(filename)
            self.settings.setValue("last_file2", filename)

    def select_file3(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Seleccionar o crear tercer archivo', self.file3_edit.text())
        if filename:
            self.file3_edit.setText(filename)
            self.settings.setValue("last_file3", filename)


    def compare_files(self):
        file1 = self.file1_edit.text()
        file2 = self.file2_edit.text()
        file3 = self.file3_edit.text()

        if not file1 or not file2 or not file3:
            self.console_output.setPlainText('Por favor, complete todas las rutas de archivo.')
            return

        try:
            with open(file1, 'r') as f1, open(file2, 'r') as f2:
                lines1 = f1.readlines()
                lines2 = f2.readlines()

            d = difflib.Differ()
            diff = list(d.compare(lines1, lines2))

            with open(file3, 'w') as output:
                output.write('\n'.join(diff))

            result = "Resumen de diferencias:\n"
            for i, line in enumerate(diff, start=1):
                if line.startswith('- ') or line.startswith('+ '):
                    result += f"Línea {i}: {line.strip()}\n"

            self.console_output.setPlainText(result)

        except Exception as e:
            self.console_output.setPlainText(f'Error al comparar archivos: {str(e)}')

    def clear_output(self):
        self.console_output.clear()

    def close_application(self):
        sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileComparator()
    sys.exit(app.exec_())
