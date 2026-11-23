"""Launch the Lab 2 grade calculator."""

import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from grade_window import GradeWindow


def main() -> int:
    """Start the application and keep its window open until the user exits."""
    app = QApplication(sys.argv)
    window = GradeWindow(Path.home() / "CS1620Gradebook" / "latest_grades.csv")
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
