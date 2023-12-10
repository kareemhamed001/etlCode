from app.compiler import parser
from app.Controller import ui

from datetime import datetime
import time
from tabulate import tabulate


def compile():
    try:
        query = str(ui.inputbox.text())
        query = query.lower()
        result = parser.parse(query)
        ui.outputbox.setText(str(result))
    except Exception as e:
        print("Compilation Error.", e)


def execute():
    try:
        current_time = time.time()
        ui.results.setText(
            f"Execution started at: {current_time}\n"
        )
        ui.results.setText(
            ui.results.toPlainText()+  "Running"
        )
        code = str(ui.outputbox.toPlainText())
        
        locals_dict = {}
        exec(str(code),globals(), locals_dict)
        
        
        ui.results.setText(
            ui.results.toPlainText()+  f"Execution Result: {locals_dict}\n"
        )


        # from app.etl.DataSoruces.DataSource import DataSource
        # total = time.time() - start_time
        # mins = int(total / 60)
        # secs = float(total % 60)
        # ui.results.setText(
        #     ui.results.toPlainText() + f"\nExcecution process on {DataSource.results} rows.\n \tTook: {mins} Minutes, {secs:.2f} Seconds.\n"
        # )

        # if isinstance(DataSource.results, str):
        #     ui.results.setText(
        #         ui.results.toPlainText() + f"\n{DataSource.results}\n"
        #     )
        # else:
            # table = tabulate(DataSource.results, headers=DataSource.results.keys())
            # ui.results.setText(
            #     ui.results.toPlainText() + f"\n{table}\n"
            # )

    except Exception as e:
        ui.results.setText(
                ui.results.toPlainText() + e
            )
        print("Execution Error.", e)
