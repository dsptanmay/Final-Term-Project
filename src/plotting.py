# IMPORTS
import plotly.graph_objects as go
import questionary as qr
from plotly.subplots import make_subplots
from pytrends.request import TrendReq
from typing import Any, List, Dict


class App:
    opts: List[str] = [
        "Compare the different topics' interests",
        "Show Data of different topics individually",
    ]
    tmfs: Dict[Any, Any] = {
        "1 Month": "today 1-m",
        "3 Months": "today 3-m",
        "12 Months": "today 12-m",
    }

    def __init__(self):
        self.pytrend = TrendReq()
        self.topics = []
        ind: int = 1
        while True:
            topic: str = (
                str(input(f"Enter topic {ind} (Enter for break)\n⚡ "))
                .rstrip(" ")
                .lstrip(" ")
            )
            if not topic:
                if len(self.topics) >= 1:
                    break
                else:
                    print("At least 1 topic should be added!")
            else:
                ind += 1
                self.topics.append(topic)
        self.tmf: str = qr.select(
            "Choose the timeframe for the data:",
            list(App.tmfs.keys()),
            default="3 Months",
        ).ask()
        self.timeframe: str = App.tmfs[self.tmf]
        resp: str = qr.select(
            "Choose the output format:", App.opts, default=App.opts[0]
        ).ask()
        if resp == App.opts[1]:
            self.showSimple()
        else:
            self.showCompare()

    def showSimple(self):
        t = []
        for name in self.topics:
            i = f"Searches for {name}"
            t.append(i)
        titles = tuple(t)
        fig = make_subplots(
            rows=len(self.topics),
            cols=1,
            subplot_titles=titles,
            x_title="Dates",
            y_title="Interest (in points out of 100)",
        )
        subRow = 1
        subCol = 1

        for name in self.topics:
            df = None
            try:
                self.pytrend.build_payload(kw_list=[name], timeframe=self.timeframe)
            except:
                print("[  ❌   ] Error in building data!")
            else:
                df = self.pytrend.interest_over_time()
                print(f"[  ✔️   ] Data successfully built for {name}")
            toBeIns = go.Scatter(
                x=df.index, y=df[name].tolist(), name=name, mode="lines+markers"
            )
            try:
                fig.append_trace(toBeIns, row=subRow, col=subCol)
            except:
                print("[  ❌   ] Error in Adding Figure!")
            else:
                print(f"[  ✔️   ] Figure successfully added for {name} ❕")
            finally:
                print("-" * 100)
            subRow += 1
        fig.update_layout(title=f"Time Period: {self.tmf}")
        try:
            fig.show()
        except:
            print("[  ❌   ] Error in Plotting Figure !")
        else:
            print("[  ✔️   ] Plotting Figures Now...")
        finally:
            print("-" * 100)

    def showCompare(self):
        fig = go.Figure()
        try:
            self.pytrend.build_payload(kw_list=self.topics, timeframe=self.timeframe)
        except:
            print("[  ❌   ] Error in building data!")
            exit()
        else:
            print("[  ✔️   ] Data successfully built!")
            df = self.pytrend.interest_over_time()
        finally:
            print("-" * 100)
        xVal = df.index
        title = "Comparison of "
        for name in self.topics:
            if self.topics.index(name) != len(self.topics) - 1:
                title += f"{name}, "
            else:
                title += f"{name} over a period of {self.tmf}."
            toBeIns = go.Scatter(
                x=xVal, y=df[name].tolist(), mode="lines+markers", name=name
            )
            try:
                fig.add_trace(toBeIns)
            except:
                print("[  ❌   ] Error in Adding figure!")
            else:
                print(f"[  ✔️   ] Figure for {name} added ")
            finally:
                print("-" * 100)
        fig.update_layout(
            title=title, xaxis_title="Dates", yaxis_title="Interest(in points)"
        )
        try:
            fig.show()
        except:
            print("[  ❌   ] Error in plotting figures!")
        else:
            print("[  ✔️   ] Plotting figures now...")
            print("-" * 100)


if __name__ == "__main__":
    App()
