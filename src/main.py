import os
import questionary
from tabulate import tabulate
from setup import setup
import csv
from datetime import date
import re
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pytrends.request import TrendReq


class Student:
    """
    Class for Student Mode.

    Used as base class for `Teacher` Class
    """

    def __init__(self) -> None:
        self.bookPath = "data/MOCK_DATA.csv"
        self.borrowPath = "data/borrowed.csv"

    def run(self) -> None:
        """Run method for Student Class"""

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
            action = questionary.select(
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

        with open(self.borrowPath, "r") as file:
            reader = csv.reader(file)

            data = list(reader)
            cur_ids = []
            for row in data:
                if len(row) == 4:
                    cur_ids.append(row[1])

            file.close()

        rollNo = questionary.text("Enter your roll No:", default="4501").ask()

        if rollNo in cur_ids:
            print("You have already borrowed a book!")
            return

        else:
            name = questionary.text("Enter your name: ",).ask()

            print("Name & Roll No. accepted!")

        with open(self.bookPath, "r") as fileObj:

            data = list(csv.reader(fileObj))

            cur_books = [row[1] for row in data]

            today = str(date.today())

            fileObj.close()

        book = questionary.autocomplete(
            "Choose a book", choices=cur_books, validate=lambda b: b in cur_books).ask()

        toBeIns = [book, rollNo, name, today]

        with open(self.borrowPath, "r") as fileObject:
            data = list(csv.reader(fileObject))

            data.append(toBeIns)

            fileObject.close()

        with open(self.borrowPath, "w") as file:
            writer = csv.writer(file)
            writer.writerows(data)
            print("Book borrowed successfully!")
            file.close()
            return

    def returnBook(self):
        """Return Method. Provides return functionality for both Student & Teacher Class."""
        with open("data/borrowed.csv", "r") as fileObject:
            reader = csv.reader(fileObject)
            cur_ids = []
            for row in reader:
                cur_ids.append(row[0])

        person = questionary.autocomplete(
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
                if len(row) == 5:
                    books.append(list(row))

            print(
                tabulate(
                    books,
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

    def plotting(self):
        """
        Method for plotting a graph based on interest in book over a period of time.
        """
        timeFrames = {
            "1 Month": "today 1-m",
            "3 Months": "today 3-m",
            "12 Months": "today 12-m"
        }


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
            username = questionary.text(
                "Enter your username:",
                default="root",
                validate=lambda x: len(x) > 0,
            ).ask()
            password = questionary.password(
                "Enter the password:",
                validate=lambda x: len(x) > 0,
            ).ask()

            if username == "root" and password == "password":
                print("Username and password validated successfully!")
                print("-"*os.get_terminal_size().columns)
                print("Teacher Mode".center(os.get_terminal_size().columns))
                print("-"*os.get_terminal_size().columns)
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
            action = questionary.select(
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
        with open(self.bookPath, "r") as fileObject:
            data = list(csv.reader(fileObject))

            cur_isbn = []
            cur_categ = []
            for row in data:
                if len(row) == 5:
                    cur_isbn.append(row[0])
                    if row[4] not in cur_categ:
                        cur_categ.append(row[4])

            fileObject.close()

        pattern_isbn = "^[0-9]{3}-[0-9]{4}-[0-9]{3}$"
        checker_isbn = re.compile(pattern=pattern_isbn)

        while True:
            isbn_new = questionary.text(
                "Enter the ISBN of your book(It should be of the format ###-####-###): ").ask()
            if isbn_new in cur_isbn:
                print("ISBN is already in use!")
                print("Try Again!")
            elif not checker_isbn.match(isbn_new):
                print("Incorrect Format!\n\tTry Again!")
            else:
                break

        bookNew = questionary.text("Enter the Book Name:").ask()

        while True:
            pagesNew = int(input("Enter the No. of Pages: "))

            if pagesNew <= 1:
                print("Incorrect Value!\n")
            else:
                break

        authorNew = questionary.text("Enter the Author's name:").ask()

        categoryNew = questionary.autocomplete(
            "Enter the Category: ",
            choices=cur_categ,
            validate=lambda cat: cat in cur_categ).ask()

        toBeIns = [isbn_new, bookNew, pagesNew, authorNew, categoryNew]

        data.append(toBeIns)

        try:
            with open(self.bookPath, "w") as fileObject:
                writer = csv.writer(fileObject)
                writer.writerows(data)
                fileObject.close()
        except Exception as e:
            print(e)
            print("Unable to add book")
            return
        else:
            print("Book added successfully!")
            return

    def removeBook(self):
        """Remove Book Method. Only for Teacher Class"""
        isbn = questionary.text(
            "Enter the ISBN of the Book:",
            validate=lambda x: type(x) == int and len(x) > 5,
        ).ask()


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
        action = questionary.select(
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
