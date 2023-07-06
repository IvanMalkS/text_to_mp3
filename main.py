import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QApplication, QWidget, QFileDialog, QMessageBox, QPushButton, QLabel, QVBoxLayout)
from pathlib import Path
import pdfplumber
from gtts import gTTS
from langdetect import detect
from docx import Document


class DialogApp(QWidget):

    def get_file(self):
        dir, _ = QFileDialog.getOpenFileName(self, 'Open text File', r"<Default dir>",
                                             "Text files (*.PDF *.DOC *.DOCX *.TXT)")
        if Path(dir).suffix == ".pdf":
            with pdfplumber.PDF(open(file=dir, mode='rb')) as pdf:  # extract text from pdf
                pages = [p.extract_text() for p in pdf.pages]
        elif Path(dir).suffix == ".docx" or Path(dir).suffix == ".doc":  # extract text from doc
            doc = Document(dir)
            pages = [p.text for p in doc.paragraphs]
        else:
            with open(file=dir, encoding="utf-8") as txt:  # extract text from txt
                pages = txt.readlines()
        first_page = pages[0].rstrip()
        text = ''.join(pages)
        text = text.replace('\n', '')

        language = detect(first_page)  # detect language of text

        mp3 = gTTS(text=text, lang=language, slow=False)  # text to voice

        file_name = Path(dir).stem  # save file
        mp3.save(file_name + '.mp3')

        Successful = QMessageBox()      # message that code compile successful
        Successful.setStyleSheet("QLabel{min-width: 200px;color; font: 75 14pt \"Tahoma\"}");
        Successful.setWindowTitle("Successful")
        Successful.setInformativeText("Successful")
        Successful.exec_()

    def __init__(self):
        super().__init__()
        self.resize(400, 50)  # create window
        self.setStyleSheet("background-color:#121212;")

        self.button1 = QPushButton('Upload file')  # create button
        self.button1.setGeometry(QtCore.QRect(20, 60, 360, 50))
        self.button1.setStyleSheet("background-color: #03C03C;\n"
                                   "font: 75 14pt \"Tahoma\";\n"
                                   "color: rgb(255, 255, 255)")
        self.button1.clicked.connect(self.get_file)

        self.labelImage = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.button1)
        layout.addWidget(self.labelImage)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = DialogApp()
    demo.show()

    sys.exit(app.exec_())
