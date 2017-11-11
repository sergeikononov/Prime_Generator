import sys
import random
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot





class App(QWidget):
    def nlz(a):
        n = 0
        if ((a >> 16) == 0):
            n += 16
            a <<= 16
        if ((a >> 24) == 0):
            n += 8
            a <<= 8
        if ((a >> 28) == 0):
            n += 4
            a <<= 4
        if ((a >> 30) == 0):
            n += 2
            a <<= 2
        if ((a >> 31) == 0):
            n += 1
            a <<= 1
        return n

    def generateNumber(k):
        value = random.getrandbits(k)
        while (value % 2 == 0):
            value = random.getrandbits(k)
        value = value | 1
        value = value | 1 << (k - 1)
        value = value << (32 - k)
        value = value >> (32 - k)
        return value

    def jacobi(a, n):
        s = 1
        while True:
            if n < 1: raise ValueError("Too small module for Jacobi symbol: " + str(n))
            if n & 1 == 0: return a
            if n == 1: return s
            a = a % n
            if a == 0: return 0
            if a == 1: return s

            if a & 1 == 0:
                if n % 8 in (3, 5):
                    s = -s
                a >>= 1
                continue

            if a % 4 == 3 and n % 4 == 3:
                s = -s

            a, n = n, a
        return

    def randint_bits(size):
        low = 1 << (size - 1)
        hi = (1 << size) - 1
        return random.randint(low, hi)

    def testSolovey(n, t):
        for index in range(t):
            randomNumber = 2 + random.randint(1, 32767) % (n - 3)
            r = pow(int(randomNumber), int(((n - 1) / 2)), int(n))
            symbolJ = App.jacobi(randomNumber, n)
            if (r != 1 and r != (n - 1)):
                return 0
            if (symbolJ == -1):
                if ((symbolJ + n) != r):
                    return 0
                else:
                    return 1
            return 1

    def generatePrime(bits, timess):
        res = 0
        value = 0
        while res == 0:
            value = App.generateNumber(bits)
            res = App.testSolovey(value, timess)
        return value


    def __init__(self):
        super().__init__()
        self.title = 'Prime Generator'
        self.left = 10
        self.top = 10
        self.width = 500
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.textbox = QLineEdit(self)
        self.textbox.move(180, 20)
        self.textbox.resize(120, 20)

        self.textbox1 = QLineEdit(self)
        self.textbox1.move(180, 50)
        self.textbox1.resize(120, 20)

        button = QPushButton('Generate', self)
        button.setToolTip('')
        button.move(190, 70)
        button.clicked.connect(self.on_click)

        self.show()

    @pyqtSlot()


    def on_click(self):
        textvalue = int(self.textbox.text())
        iteration = int(self.textbox1.text())
        textvalue = App.generatePrime(textvalue, iteration)
        QMessageBox.question(self, 'Prime generator', "You number: " + str(textvalue), QMessageBox.Ok,
                             QMessageBox.Ok)
        self.textbox.setText("")





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())