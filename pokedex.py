import pandas as pd
import sys
import urllib.request
from PyQt6.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QLabel, QGridLayout
from PyQt6.QtGui import QIcon, QImage, QPixmap
from PyQt6 import QtCore

class PokeDex(QWidget):
    def __init__(self):
        super(PokeDex, self).__init__()
        
        self.initUI()

    def initUI(self):
        '''Initial UI'''

        # Grid layout
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        # Parse JSON for DataFrame
        self.df = pd.read_json('pokemon_data.json')
        self.df = self.df.set_index(['#'])

        # Drop Down
        self.dropdown = QComboBox(self)
        self.names = self.df['Name'].values
        self.dropdown.addItems(self.names)
        self.grid.addWidget(self.dropdown, 0, 0, 1, 1)

        # Search Button
        self.btn = QPushButton('Search', self)
        self.btn.clicked.connect(self.runSearch)
        self.grid.addWidget(self.btn, 0, 1, 1, 1)

        # Image
        self.img = QLabel(self)
        self.grid.addWidget(self.img, 1, 1, 1, 1)

        # Data
        self.label = QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setText('\nName:\n\nType:\n\nHP:\n\nAttack:\n\nSp. Attack:\n\nDefense:\n\nSp. Defense:\n\nSpeed:\n\nTotal:')
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.grid.addWidget(self.label, 1, 0, 1, 1)

        # Customize Widgets
        self.resize(500,250)
        self.center()
        self.setWindowTitle('PokeDex')
        self.show()

    def runSearch(self):
        '''Event for run Button'''

        try:
            index = self.dropdown.currentIndex()
            val = self.names[index]
            cond = self.df['Name'] == val

            # Image URL
            base = 'http://img.pokemondb.net/artwork/'
            img_url = base + val.lower() + '.jpg'

            # Adding headers to simulate a real browser request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            req = urllib.request.Request(img_url, headers=headers)
            data = urllib.request.urlopen(req).read()

            # Load image
            image = QImage()
            image.loadFromData(data)
            self.img.setPixmap(QPixmap(image))

            # Set values
            name = 'Name:\t\t\t' + val + '\n\n'
            ty = 'Type:\t\t\t' + ' '.join(self.df[cond]['Type'].values[0]) + '\n\n'
            hp = 'HP:\t\t\t' + str(self.df[cond]['HP'].values[0]) + '\n\n'
            atk = 'Attack:\t\t\t' + str(self.df[cond]['Attack'].values[0]) + '\n\n'
            satk = 'Sp. Attack:\t\t' + str(self.df[cond]['Sp. Atk'].values[0]) + '\n\n'
            deff = 'Defense:\t\t\t' + str(self.df[cond]['Defense'].values[0]) + '\n\n'
            sdef = 'Sp. Defense:\t\t' + str(self.df[cond]['Sp. Def'].values[0]) + '\n\n'
            speed = 'Speed:\t\t\t' + str(self.df[cond]['Speed'].values[0]) + '\n\n'
            total = 'Total:\t\t\t' + str(self.df[cond]['Total'].values[0]) + '\n\n'

            # Add text
            final = name + ty + hp + atk + satk + deff + sdef + speed + total
            self.label.setText(final)

        except Exception as e:
            print(f"Erro ao buscar dados ou carregar imagem: {e}")
            self.label.setText("Erro ao carregar dados ou imagem.")

    def center(self):
        '''Center Widget on screen'''

        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()  # Updated for PyQt6
        qr.moveCenter(cp)
        self.move(qr.topLeft())

def main():
    '''Codes for running GUI'''

    # Create Application object to run GUI
    app = QApplication(sys.argv)

    # Run GUI
    gui = PokeDex()

    # Exit cleanly when closing GUI
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
