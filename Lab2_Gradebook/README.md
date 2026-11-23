# Class Gradebook

A PyQt6 version of the CSCI 1620 Lab 2 grade calculator. Enter a class on one line, see each student's grade, and reopen the application to view the last saved class.

## Run in PyCharm

1. Extract the project and open the folder containing `main.py` in PyCharm.
2. Choose a Python 3.10 or newer interpreter for the project.
3. In the PyCharm terminal, run `python -m pip install -r requirements.txt`.
4. Right-click `main.py` and choose **Run 'main'**. From a terminal, use `python main.py`.

To edit the interface, open `grade_window.ui` in Qt Widgets Designer. The application reads the form directly at startup.

## Try the original lab example

Enter **3** for the number of students, enter **55 40 70** in the scores field, then choose **Calculate and save**.

| Student | Score | Grade |
| --- | ---: | :---: |
| 1 | 55 | B |
| 2 | 40 | C |
| 3 | 70 | A |

The best score is 70. The average is (55 + 40 + 70) / 3 = 55.00, which earns a B. As in Lab 2, the grade boundaries are the best score minus 10 for A, 20 for B, 30 for C, and 40 for D. Scores below the D boundary earn F. The average receives a letter using its unrounded value.

If there are extra scores, the class uses only the first requested scores. If there are too few, edit the line and try again. Each accepted score must be a whole number from 0 through 100.

## Data and project files

**Calculate and save** replaces the previous class in `CS1620Gradebook/latest_grades.csv` inside your home folder. The CSV holds student numbers, scores and grades. The app reloads it on startup and recalculates the summary. Invalid input leaves the last saved report visible. A storage error is displayed in the window.

| File | Purpose |
| --- | --- |
| `main.py` | Starts the application and sets the CSV location. |
| `grade_window.ui` | Editable Qt Designer form with input fields and a result table. |
| `grade_window.py` | A QMainWindow subclass that handles input, events, feedback and display. |
| `grade_report.py` | Validates keyboard input and keeps the scores private inside GradeReport. |
| `grade_storage.py` | Reads and writes the CSV file. |
| `requirements.txt` | Lists the Python dependency. |
