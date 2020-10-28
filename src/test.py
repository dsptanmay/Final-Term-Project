import pandas as pd
from typing import List, Any, Dict
import questionary


class Student:
    def __init__(self):
        self.booksPath = "data/MOCK_DATA.csv"
        self.borrowPath = 'data/borrowed.csv'

    def borrowBook(self):

        dataset_borrowed = pd.read_csv(filepath_or_buffer=self.borrowPath, names=[
                                       "BOOK NAME", "ROLL NO.", "NAME", "DATE BORROWED"])

        currentRollNos = dataset_borrowed["ROLL NO."].tolist()
        print(currentRollNos)

        # rollNo = questionary.select("Enter your roll No. :").ask()

        dataset_books = pd.read_csv(filepath_or_buffer=self.booksPath,
                                    names=[
                                        "ISBN",
                                        "BOOK NAME",
                                        "PAGES",
                                        "AUTHOR NAME",
                                        "CATEGORY"])
