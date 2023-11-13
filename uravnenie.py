import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox

from sympy import symbols, sympify, diff

# x = symbols('x')

# Метод хорд
def chord_method(eq_str, x1, x2, tol=1e-6, max_iter=100):
    try:
        eq = sympify(eq_str)
        x = symbols('x')
        for i in range(max_iter):
            f_x1 = eq.subs(x, x1)
            f_x2 = eq.subs(x, x2)
            x_new = x2 - (f_x2 * (x1 - x2)) / (f_x1 - f_x2)

            if abs(x_new - x2) < tol:
                return x_new

            x1, x2 = x2, x_new

        return None
    except Exception as e:
        return str(e)

# Метод касательных
def newton_method(eq_str, x0, tol=1e-6, max_iter=100):
    try:
        eq = sympify(eq_str)
        x = symbols('x')
        f_prime = diff(eq, x)
        for i in range(max_iter):
            f_x0 = eq.subs(x, x0)
            f_prime_x0 = f_prime.subs(x, x0)
            x_new = x0 - f_x0 / f_prime_x0

            if abs(x_new - x0) < tol:
                return x_new

            x0 = x_new

        return None
    except Exception as e:
        return str(e)

class EquationSolver(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Решение уравнений")
        self.setGeometry(100, 100, 400, 200)

        self.equation_label = QLabel("Введите уравнение (например, x^2-9*x+14=0):", self)
        self.equation_label.move(10, 10)

        self.equation_entry = QLineEdit(self)
        self.equation_entry.setGeometry(10, 30, 380, 20)

        self.x1_label = QLabel("Введите x1:", self) 
        self.x1_label.move(10, 60)

        self.x1_entry = QLineEdit(self)
        self.x1_entry.setGeometry(10, 80, 80, 20)

        self.x2_label = QLabel("Введите x2:", self)
        self.x2_label.move(150, 60)

        self.x2_entry = QLineEdit(self)
        self.x2_entry.setGeometry(150, 80, 80, 20)

        self.method_label = QLabel("Выберите метод:", self)
        self.method_label.move(10, 110)

        self.method_combobox = QComboBox(self)
        self.method_combobox.addItem("Хорд")
        self.method_combobox.addItem("Касательных")
        self.method_combobox.setGeometry(10, 130, 120, 20)

        self.calculate_button = QPushButton("Посчитать", self)
        self.calculate_button.setGeometry(10, 160, 80, 30)
        self.calculate_button.clicked.connect(self.calculate_solution)

        self.result_label = QLabel(self)
        self.result_label.setGeometry(120, 160, 280, 30)

    def calculate_solution(self):
        try:
            equation_str = self.equation_entry.text().replace("^", "**").replace("=", "-(") + ")"
            x1 = float(self.x1_entry.text())
            x2 = float(self.x2_entry.text())

            if self.method_combobox.currentText() == "Хорд":
                solution = chord_method(equation_str, x1, x2)
            else:
                solution = newton_method(equation_str, x1)

            if isinstance(solution, str):
                raise Exception(solution)

            if solution is not None:
                self.result_label.setText(f"Решение: x = {solution:.6f}")
            else:
                self.result_label.setText("Решение не найдено")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EquationSolver()
    ex.show()
    sys.exit(app.exec_())
