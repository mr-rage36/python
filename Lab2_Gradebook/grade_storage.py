"""Save and restore the last class report in a human-readable CSV file."""

import csv
from pathlib import Path
from tempfile import NamedTemporaryFile

from grade_report import GradeReport


def save_report(path: Path, report: GradeReport) -> None:
    """Replace the previous CSV only after the new report has been written."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None
    try:
        with NamedTemporaryFile(mode="w", dir=path.parent, delete=False,
                                encoding="utf-8", newline="") as output:
            temporary_path = Path(output.name)
            writer = csv.writer(output)
            writer.writerow(["Student", "Score", "Grade"])
            for number, score in enumerate(report.get_scores(), start=1):
                writer.writerow([number, score, report.letter_grade(score)])
        temporary_path.replace(path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def load_report(path: Path) -> GradeReport:
    """Read the saved scores and check the student numbers and letter grades."""
    with path.open(encoding="utf-8", newline="") as source:
        reader = csv.reader(source, strict=True)
        if next(reader, None) != ["Student", "Score", "Grade"]:
            raise ValueError("The CSV needs the header Student,Score,Grade.")
        scores = []
        grades = []
        for number, row in enumerate(reader, start=1):
            if len(row) != 3 or row[0] != str(number) or not row[1].isdecimal():
                raise ValueError(f"Invalid student record on row {number + 1}.")
            scores.append(int(row[1]))
            grades.append(row[2])
    report = GradeReport(scores)
    for score, grade in zip(scores, grades):
        if report.letter_grade(score) != grade:
            raise ValueError("A saved grade does not match the class scores.")
    return report
