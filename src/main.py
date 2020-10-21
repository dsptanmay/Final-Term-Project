import os
import questionary as qr
import plotly.graph_objects as go
from tabulate import tabulate
import csv


class Student:
    """
    Class for Student Mode.

    Used as base class for `Teacher` Class
    """

    def __init__(self) -> None:
        pass

    def run(self) -> None:
        """Run method for Student Class"""
        TERM = os.get_terminal_size()
        print("-" * TERM.columns)
        print("STUDENT Mode".center(TERM.columns))
        print("-" * TERM.columns)
        actions = ["Borrow A Book", "Return A Book", "See All Books", "EXIT"]

        while True:
            action = qr.select(
                "Choose an action:", choices=actions, default=actions[3]
            ).ask()

            if action == actions[0]:
                self.borrowBook()
            elif action == actions[1]:
                self.returnBook()
            elif action == actions[2]:
                self.seeAllBooks()
            else:
                exit()

    def borrowBook(self):
        """Borrow Method. Provides borrowing functionality for both Student & Teacher Class."""
        pass

    def returnBook(self):
        """Return Method. Provides return functionality for both Student & Teacher Class."""
        pass

    def seeAllBooks(self):
        """See All Method. Allows either students or teachers to see All books present."""
        with open("data/books.csv", "r") as fileObject:
            pass


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

    def run(self) -> None:
        """Run method for Teacher Class"""
        actions = [
            "Add A Book"  # 0,
            "Remove a Book"  # 1,
            "See All Books"  # 2,
            "Borrow A Book"  # 3,
            "Return A Book"  # 4,
            "EXIT"  # 5,
        ]

        while True:
            action = qr.select(
                "Choose an action:", choices=actions, default=actions[5]
            ).ask()

            if action == actions[5]:
                print("Exiting program...")
                exit()
            elif action == actions[4]:
                self.returnBook()
            elif action == actions[3]:
                self.borrowBook()
            elif action == actions[2]:
                self.seeAllBooks()
            elif action == actions[1]:
                self.removeBook()
            elif action == actions[0]:
                self.addBook()
            else:
                print("Error in choosing action.")
                exit(0)

    def addBook(self):
        """Add Book Method. Only for Teacher Class"""
        cont = True
        while cont:
            isbn = qr.text(
                "Enter the ISBN of the book:",
                validate=lambda x: type(x) == int and len(x) > 5,
            ).ask()

            cont = qr.confirm("Do you wish to continue?", default=False).ask()

    def removeBook(self):
        """Remove Book Method. Only for Teacher Class"""
        cont = True
        while cont:
            isbn = qr.text(
                "Enter the ISBN of the Book:",
                validate=lambda x: type(x) == int and len(x) > 5,
            ).ask()

            cont = qr.confirm("Do you wish to continue?", default=False).ask()


class MainApp:
    def __init__(self) -> None:
        options = ["TEACHER MODE", "STUDENT MODE"]

        action = qr.select("Choose a mode:", choices=options, default=options[1]).ask()

        main = None
        if action == options[1]:
            main = Student()
            main.run()
        else:
            main = Teacher()
            main.run()


if __name__ == "__main__":
    app = MainApp()
