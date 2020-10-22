import subprocess as sp
import sys
import pkg_resources


def setup():
    installed = {pkg.key for pkg in pkg_resources.working_set}
    required = {"plotly", "questionary", "tabulate", "black"}
    python = sys.executable

    missing = required - installed

    if missing:
        for module in missing:
            try:
                sp.check_call(
                [python, "-m", "pip", "install", "--upgrade", "--no-cache-dir", module],
                stdout=sp.DEVNULL,
            )
            except Exception as e:
                print("An error occurred in installing modules!")
            else:
                print(f"{module.capitalize()} was successfully installed!")