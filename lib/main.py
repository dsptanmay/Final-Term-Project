import os
import questionary as qr
import plotly.graph_objects as go
import json
import sys
import sqlite3


class Student:
    def __init__(self) -> None:
        TERM = os.get_terminal_size()
        print("-" * TERM.columns)
        print("STUDENT Mode".center(TERM.columns))
        print("-" * TERM.columns)


class Teacher(Student):
    """Class for Teacher Method.

    Parameters
    ----------
    Student : Base Class

        Teacher inherits from Student
    """

    def __init__(self) -> None:
        super().__init__()
        while True:
            username = qr.text(
                "Enter your username:", default="root", validate=lambda x: len(x) > 0
            ).ask()
            password = qr.password(
                "Enter the password:", validate=lambda x: len(x) > 0
            ).ask()

            if username == "root" and password == "password":
                break
            else:
                print("Wrong passsword!\nTry again!")
                print("-" * os.get_terminal_size().columns)


class MainApp:
    def __init__(self) -> None:
        options = ["TEACHER MODE", "STUDENT MODE"]

        action = qr.select("Choose a mode:", choices=options, default=options[1]).ask()

        run = None
        if action == options[1]:
            run = Student()
        else:
            run = Teacher()


if __name__ == "__main__":
    app = MainApp()
