import csv
import os
import re
from datetime import date

import plotly.graph_objects as go
import questionary
from pytrends.request import TrendReq
from tabulate import tabulate

from setup import setup


class Student:
    """
    Class for Student Mode.

    Used as base class for `Teacher` Class
    """

    def __init__(self) -> None:
        self.bookPath = "data/MOCK_DATA.csv"
        self.borrowPath = "data/borrowed.csv"
        self.baseActions = [
            "Borrow A Book",
            "Return A Book",
            "See All Books",
            "Search By Author",
            "Search By Genre",
            "See Trends for a Particular Book",
            "EXIT",
        ]

    def run(self) -> None:
        """Run method for Student Class"""

        TERM = os.get_terminal_size()
        print("-" * TERM.columns)
        print("STUDENT Mode".center(TERM.columns))
        print("-" * TERM.columns)

        while True:
            action = questionary.select(
                "Choose an action:",
                choices=self.baseActions,
                default=self.baseActions[6],
            ).ask()

            if action == self.baseActions[0]:
                self.borrowBook()

            elif action == self.baseActions[1]:
                self.returnBook()

            elif action == self.baseActions[2]:
                self.seeAllBooks()

            elif action == self.baseActions[3]:
                self.searchByAuthor()

            elif action == self.baseActions[4]:
                self.searchByGenre()

            elif action == self.baseActions[5]:
                self.plotting()

            else:
                exit()

    def borrowBook(self):
        """Borrow Method.
        Provides borrowing functionality for both Student & Teacher Class."""

        with open(self.borrowPath, "r", newline="") as file_borrow_01:
            reader = csv.reader(file_borrow_01)

            data_borrow = list(reader)
            cur_ids = []
            for row in data_borrow:
                if len(row) == 4:
                    cur_ids.append(row[1])

            file_borrow_01.close()

        rollNo = questionary.text(
            "Enter your Admission No:",
            validate=lambda x: len(x) == 4 and str(x).isdigit() == True,
        ).ask()

        if rollNo in cur_ids:
            print("You have already borrowed a book.")
            print("First return that book!")
            return

        name = questionary.text(
            "Enter your name: ",
        ).ask()

        print("Name & Admin No. accepted!")

        with open(self.bookPath, "r", newline="") as fileBooks:
            data_books = []
            for row in csv.reader(fileBooks):
                if len(row) != 0:
                    data_books.append(row)

            cur_books = [row[1] for row in data_books]

            today = str(date.today())

            fileBooks.close()

        book = questionary.autocomplete(
            "Choose a book",
            choices=cur_books,
            validate=lambda b: b in cur_books,
        ).ask()

        toBeIns = [book, rollNo, name, today]
        data_borrow = [
            row
            for row in csv.reader(open(self.borrowPath, "r", newline=""))
            if len(row) != 0
        ]
        data_borrow.append(toBeIns)

        with open(self.borrowPath, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data_borrow)
            print("Book borrowed successfully!")
            file.close()

    def returnBook(self):
        """Return Method.
        Provides return functionality for both Student & Teacher Class."""
        with open(self.borrowPath, "r") as fileObject:
            reader = csv.reader(fileObject)
            data = [row for row in reader if len(row) == 4]
            fileObject.close()

        admNos = [row[1] for row in data]

        admNo = questionary.text(
            "Enter your adm No:",
            validate=lambda x: x in admNos,
        ).ask()

        dateBorrowed = date(2020, 1, 1)
        for row in data:
            if row[1] == admNo:
                dateBorrowed = row[3]
                comps = dateBorrowed.split("-")
                dateBorrowed = date(int(comps[0]), int(comps[1]), int(comps[2]))
                data.remove(row)

        today = date.today()

        daysBorrowed: int = (today - dateBorrowed).days

        if daysBorrowed <= 7:
            print("Amount to be Paid is Rs. 100")

        elif 7 < daysBorrowed < 50:
            print("-" * os.get_terminal_size().columns)
            print(
                f"Amount to Be Paid: {daysBorrowed*35}".center(
                    os.get_terminal_size().columns
                )
            )
            print("-" * os.get_terminal_size().columns)
        else:
            print("You have exceeded the number of days to return the book!")
            print("You must pay a fine of Rs. 500")

        with open(self.borrowPath, "w", newline="") as fileObject:
            writer = csv.writer(fileObject)
            writer.writerows(data)
            fileObject.close()

    def seeAllBooks(self):
        """See All Method.
        Allows either students or teachers to see All books present."""

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
        Method for plotting a graph based on
        interest in book over a period of time.
        """
        with open(self.bookPath, "r") as plottingFile:
            data = [row for row in csv.reader(plottingFile) if len(row) != 0]

            currentBooks = [row[1] for row in data if len(row) != 0]

            plottingFile.close()

        book = questionary.autocomplete(
            "Enter the name of the book:",
            choices=currentBooks,
            validate=lambda x: x in currentBooks,
        )

        bookVal = book.ask()
        timeFrames = {
            "1 Month": "today 1-m",
            "3 Months": "today 3-m",
            "12 Months": "today 12-m",
        }

        tmf = questionary.select(
            "Choose the timeframe:", choices=list(timeFrames.keys())
        ).ask()

        tmfValue = timeFrames[tmf]
        pytrend = TrendReq()
        try:
            pytrend.build_payload(kw_list=[bookVal], timeframe=tmfValue)
        except Exception as e:
            print("Error in building data for {}".format(bookVal))
            return

        else:
            print("Data successfully built!")
            df = pytrend.interest_over_time()

            df.drop(labels="isPartial", axis=1, inplace=True)

        try:
            data = go.Scatter(
                x=df.index, y=df[bookVal], name=bookVal, mode="lines+markers"
            )

        except Exception as e:
            print("Error in building figure!")
            print(e)
            return

        else:
            print("Figure built successfully!!")
            fig = go.Figure(data=data)
            fig.show()

    def searchByAuthor(self):
        data = None

        with open(self.bookPath, "r") as fileObject:
            data = list(csv.reader(fileObject))

        authors = []
        for _row in data:
            if _row[3] not in authors:
                authors.append(_row[3])

        authorChoose = questionary.autocomplete(
            "Enter the author's name:",
            choices=authors,
            validate=lambda x: x in authors,
        ).ask()

        authorData = []

        for _row in data:
            if _row[3] == authorChoose:
                authorData.append(_row)

        print(
            tabulate(
                authorData,
                headers=[
                    "ISBN",
                    "BOOK NAME",
                    "PAGES",
                    "AUTHOR NAME",
                    "GENRE",
                ],
                tablefmt="fancy_grid",
            )
        )

    def searchByGenre(self):
        data = None
        with open(self.bookPath, "r") as fileObject:
            data = list(csv.reader(fileObject))

            genres = []
            for row in data:
                if row[4] not in genres:
                    genres.append(row[4])

        genreChoose = questionary.select(
            "Choose a genre:", choices=genres, default=genres[0]
        ).ask()

        genreData = []

        for row in data:
            if row[4] == genreChoose:
                genreData.append(row)

        print("All Books with Genre {} are:".format(genreChoose))

        print(
            tabulate(
                genreData,
                headers=["ISBN", "BOOK NAME", "PAGES", "AUTHOR", "GENRE"],
                tablefmt="fancy_grid",
            )
        )


# TODO:  Search : Author/ Books Name


class Teacher(Student):
    """Class for Teacher Method.

    Parameters
    ----------
    Student : Base Class

    Teacher inherits from Student
    """

    def __init__(self) -> None:
        super().__init__()

    def verify(self):
        attempts = 3
        while True:
            attempts -= 1
            if attempts == 0:
                print("3 attemps used up!")
                exit()
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
                print("-" * os.get_terminal_size().columns)
                print("Teacher Mode".center(os.get_terminal_size().columns))
                print("-" * os.get_terminal_size().columns)
                break
            else:
                print(
                    "Wrong passsword!".center(
                        os.get_terminal_size().columns
                    ).capitalize()
                )

    def run(self) -> None:
        """Run method for Teacher Class"""
        self.verify()
        self.baseActions.extend(
            [
                "Add Book",
                "Remove Book",
            ]
        )
        actions = self.baseActions

        while True:
            action = questionary.select(
                "Choose an action:", choices=actions, default=actions[0]
            ).ask()

            if action == actions[0]:
                self.borrowBook()
            elif action == actions[1]:
                self.returnBook()
            elif action == actions[2]:
                self.seeAllBooks()
            elif action == actions[3]:
                self.searchByAuthor()
            elif action == actions[4]:
                self.searchByGenre()
            elif action == actions[5]:
                self.plotting()
            elif action == actions[7]:
                self.addBook()
            elif action == actions[8]:
                self.removeBook()
            else:
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
                "Enter the ISBN of your book\
                (It should be of the format ###-####-###): "
            ).ask()
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

        authorNew = questionary.text(
            "Enter the Author's name:",
            validate=lambda x: len(x.split(" ")) >= 2,
        ).ask()

        categoryNew = questionary.autocomplete(
            "Enter the Category: ",
            choices=cur_categ,
            validate=lambda cat: cat in cur_categ,
        ).ask()

        toBeIns = [isbn_new, bookNew, pagesNew, authorNew, categoryNew]

        data.append(toBeIns)

        try:
            with open(self.bookPath, "w", newline="") as fileObject:
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
        pattern_isbn = "^[0-9]{3}-[0-9]{4}-[0-9]{3}$"
        checker_isbn = re.compile(pattern=pattern_isbn)

        with open(self.bookPath, "r", newline="") as fileObject:
            data = [row for row in csv.reader(fileObject) if len(row) != 0]
            curISBNs = [row[0] for row in data]
            fileObject.close()

        while True:
            isbnToRemove = questionary.text(
                "Enter the ISBN of the Book that you want to remove"
            ).ask()
            if not checker_isbn.match(isbnToRemove):
                print("Wrong format.\n Try Again!")
                print("Correct format is : ###-####-###")
            elif isbnToRemove not in curISBNs:
                print("Invalid ISBN!\nTry again!")
            else:
                break

        with open(self.bookPath, "r", newline="") as file_book_02:
            data = [row for row in csv.reader(file_book_02) if len(row) == 5]
            for row in data:
                if str(row[0]).rstrip(" ").lstrip(" ") == isbnToRemove:
                    data.remove(row)
                    print(row)
            file_book_02.close()

        with open(self.bookPath, "w", newline="") as fileObject:
            writer = csv.writer(fileObject)

            writer.writerows(data)
            print("Book successfully deleted!")


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
        elif action == options[0]:
            main = Teacher()
            main.run()


if __name__ == "__main__":
    app = MainApp()
