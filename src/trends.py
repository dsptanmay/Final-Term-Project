from pytrends.request import TrendReq
import csv


class Plotting:
    def __init__(self) -> None:
        with open("data/trends.csv", "w") as fileObject:
            pass