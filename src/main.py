import os
import questionary as qr
import plotly.graph_objects as go
from tabulate import tabulate
from setup import setup
import csv


class Student:
    """
    Class for Student Mode.

    Used as base class for `Teacher` Class
    """

    def run(self) -> None:
        """Run method for Student Class"""

        self.bookPath = "data/MOCK_DATA.csv"
        TERM = os.get_terminal_size()
        print("-" * TERM.columns)
        print("STUDENT Mode".center(TERM.columns))
        print("-" * TERM.columns)
        actions = [
            "Borrow A Book",
            "Return A Book",
            "See All Books",
            "EXIT",
        ]

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
        with open("data/borrowed.csv", "r") as fileObject:
            reader = csv.reader(fileObject)
            cur_ids = []
            for row in reader:
                cur_ids.append(row[0])

        person = qr.autocomplete(
            "Enter the name of the Person who borrowed a book:",
            choices=cur_ids,
            validate=lambda x: x in cur_ids,
        ).ask()

    def seeAllBooks(self):
        """See All Method. Allows either students or teachers to see All books present."""

        with open(self.bookPath, "r") as fileObject:
            reader = csv.reader(fileObject)
            books = list()
            for row in reader:
                books.append(list(row))

            num_to_disp = qr.text(
                "Enter the number of rows to display:",
                validate=lambda x: x < len(books) and type(x) == int,
            ).ask()

            to_be_disp = books[0:num_to_disp]
            print(
                tabulate(
                    to_be_disp,
                    headers=[
                        "ISBN",
                        "Book Name",
                        "No. of Pages",
                        "Author",
                        "Category",
                    ],
                    tablefmt="fancy_grid",
                )
            )


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
                "Enter your username:",
                default="root",
                validate=lambda x: len(x) > 0,
            ).ask()
            password = qr.password(
                "Enter the password:",
                validate=lambda x: len(x) > 0,
            ).ask()

            if username == "root" and password == "password":
                break
            else:
                print("-" * os.get_terminal_size().columns)
                print(
                    "Wrong passsword!\nTry again!".center(
                        os.get_terminal_size().columns
                    ).capitalize()
                )
                print("-" * os.get_terminal_size().columns)

    def run(self) -> None:
        """Run method for Teacher Class"""
        actions = [
            "Add A Book",  # 0,
            "Remove a Book",  # 1,
            "See All Books",  # 2,
            "Borrow A Book",  # 3,
            "Return A Book",  # 4,
            "EXIT",  # 5,
        ]

        while True:
            action = qr.select(
                "Choose an action:",
                choices=actions,
                default=actions[5],
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

            cont = qr.confirm(
                "Do you wish to continue?",
                default=False,
            ).ask()

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
        try:
            setup()
        except Exception:
            print("An error occurred!")
            exit()
        else:
            print("All necessary modules installed successfully!")

        options = ["TEACHER MODE", "STUDENT MODE"]
        action = qr.select(
            "Choose a mode:",
            choices=options,
            default=options[1],
        ).ask()
        main = None
        if action == options[1]:
            main = Student()
            main.run()
        else:
            main = Teacher()
            main.run()


if __name__ == "__main__":
    app = MainApp()
