"""Connect the Qt Designer form to the grading and storage modules."""

import csv
from pathlib import Path

from PyQt6 import uic
from PyQt6.QtWidgets import QHeaderView, QMainWindow, QTableWidgetItem

from grade_report import GradeReport, read_class_scores
from grade_storage import load_report, save_report


class GradeWindow(QMainWindow):
    """Display class scores and keep the most recent successful calculation."""

    def __init__(self, data_file: Path) -> None:
        """Load the Designer form, connect its controls, and restore saved data."""
        super().__init__()
        uic.loadUi(Path(__file__).with_name("grade_window.ui").as_posix(), self)
        self.__data_file = data_file
        self.resultsTable.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.calculateButton.clicked.connect(self.calculate)
        self.scoresInput.returnPressed.connect(self.calculate)
        self.countInput.returnPressed.connect(self.scoresInput.setFocus)
        self.restore()
        self.countInput.setFocus()

    def restore(self) -> None:
        """Fill the form with the last saved class when its CSV is readable."""
        try:
            report = load_report(self.__data_file)
        except FileNotFoundError:
            return
        except (OSError, ValueError, csv.Error) as error:
            self.statusLabel.setText(f"Could not read the saved class. {error}")
            return
        scores = report.get_scores()
        self.countInput.setText(str(len(scores)))
        self.scoresInput.setText(" ".join(str(score) for score in scores))
        self.display_report(report)
        self.statusLabel.setText("Loaded the last saved class.")

    def calculate(self) -> None:
        """Validate entries, save the new class, and show its grades."""
        try:
            report = read_class_scores(self.countInput.text(), self.scoresInput.text())
        except ValueError as error:
            self.statusLabel.setText(str(error))
            return
        try:
            save_report(self.__data_file, report)
        except (OSError, csv.Error) as error:
            self.statusLabel.setText(f"Could not save this class. {error}")
            return
        self.display_report(report)
        count = len(report.get_scores())
        message = "Class saved."
        if len(self.scoresInput.text().split()) > count:
            message += f" Used only the first {count} scores."
        self.statusLabel.setText(message)

    def display_report(self, report: GradeReport) -> None:
        """Show the saved class in entry order and format its average."""
        scores = report.get_scores()
        self.resultsTable.setRowCount(len(scores))
        for row, score in enumerate(scores):
            values = [str(row + 1), str(score), report.letter_grade(score)]
            for column, value in enumerate(values):
                self.resultsTable.setItem(row, column, QTableWidgetItem(value))
        average = report.average()
        self.summaryLabel.setText(
            f"Best score: {report.best_score()}     "
            f"Class average: {average:.2f} ({report.letter_grade(average)})"
        )
