import pandas as pd
import questionary as qr


class Person:
    def __init__(self):
        self.bookPath = "data/MOCK_DATA.csv"
        self.borrowedPath = "data/borrowed.csv"

    def run(self):
        choices = [
            "Borrow A Book",
            "Return A Book",
            "Search by Author",
            "Search by Category",
            "EXIT",
        ]

        action = qr.select(
            "Choose an action: ", choices=choices, default=choices[4]
        ).ask()

        if action == choices[0]:
            self.borrowBook()

        elif action == choices[1]:
            pass

        elif action == choices[2]:
            pass

        elif action == choices[3]:
            pass

        elif action == choices[4]:
            print("Exiting the program now...")
            exit(0)

    def borrowBook(self):
        dataset_books = pd.read_csv(
            filepath_or_buffer=self.bookPath,
            names=[
                "ISBN",
                "BOOK NAME",
                "PAGES",
                "AUTHOR NAME",
                "CATEGORY",
            ],
        )

        dataset_borrowed = pd.read_csv(self.borrowedPath,names=["BOOK NAME","ADMISSION NO.","NAME","DATE BORROWED"])

        print(dataset_books.head())

        books = dataset_books["BOOK NAME"].tolist()

        book = qr.autocomplete(
            "Choose a book: ",
            choices=books,
            validate=lambda x: x in books,
        ).ask()

        


if __name__ == "__main__":
    app = Person()
    app.run()
