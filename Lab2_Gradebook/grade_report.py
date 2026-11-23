"""Validate keyboard input and calculate the relative grades used in Lab 2."""


class GradeReport:
    """Keep one class's scores and use its best score as the grading reference."""

    def __init__(self, scores: list[int]) -> None:
        """Keep a private copy of whole-number scores in the range 0 through 100."""
        if not scores:
            raise ValueError("Enter at least one score.")
        for score in scores:
            if type(score) is not int or not 0 <= score <= 100:
                raise ValueError("Every score must be a whole number from 0 to 100.")
        self.__scores = scores.copy()
        self.__best_score = max(scores)

    def get_scores(self) -> list[int]:
        """Return a copy so callers cannot change the saved scores."""
        return self.__scores.copy()

    def best_score(self) -> int:
        """Return the highest accepted student score."""
        return self.__best_score

    def average(self) -> float:
        """Return the unrounded mean used to grade the class average."""
        return sum(self.__scores) / len(self.__scores)

    def letter_grade(self, score: float) -> str:
        """Assign a letter by comparing the score with the best in this class."""
        if score >= self.__best_score - 10:
            return "A"
        if score >= self.__best_score - 20:
            return "B"
        if score >= self.__best_score - 30:
            return "C"
        if score >= self.__best_score - 40:
            return "D"
        return "F"


def read_class_scores(count_text: str, scores_text: str) -> GradeReport:
    """Read the requested number of scores from one space-separated line."""
    count_text = count_text.strip()
    if not count_text.isdecimal():
        raise ValueError("Enter the number of students as a positive whole number.")
    try:
        count = int(count_text)
    except ValueError:
        raise ValueError("The student count is too large.") from None
    if count < 1:
        raise ValueError("Enter at least one student.")

    entries = scores_text.split()
    if len(entries) < count:
        raise ValueError(f"Enter {count} scores. You entered {len(entries)}.")

    scores = []
    for number, entry in enumerate(entries[:count], start=1):
        message = f"Score {number} must be a whole number from 0 to 100."
        if not entry.isdecimal():
            raise ValueError(message)
        try:
            score = int(entry)
        except ValueError:
            raise ValueError(message) from None
        if score > 100:
            raise ValueError(message)
        scores.append(score)
    return GradeReport(scores)
