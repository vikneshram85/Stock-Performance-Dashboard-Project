import os
import yaml
import csv

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

input_folder = "data"
output_folder = "csv_by_ticker"
os.makedirs(output_folder, exist_ok=True)

written_headers = {}

for month_folder in os.listdir(input_folder):
    month_path = os.path.join(input_folder, month_folder)

    if not os.path.isdir(month_path):
        continue

    for file in os.listdir(month_path):
        if file.endswith(".yaml") or file.endswith(".yml"):
            file_path = os.path.join(month_path, file)

            with open(file_path, "r") as f:
                data = yaml.load(f, Loader=Loader)

            # Case 1: YAML file contains a list
            if isinstance(data, list):
                records = data

            # Case 2: YAML file contains a single dict
            elif isinstance(data, dict):
                records = [data]

            else:
                continue

            # Process each record inside the file
            for record in records:

                if not isinstance(record, dict):
                    continue

                ticker = (
                    record.get("Ticker") or
                    record.get("ticker") or
                    record.get("TICKER")
                )

                if not ticker:
                    continue

                ticker = ticker.upper()
                csv_file = os.path.join(output_folder, f"{ticker}.csv")

                write_header = False
                if ticker not in written_headers:
                    write_header = True
                    written_headers[ticker] = True

                with open(csv_file, "a", newline="", encoding="utf-8") as csvf:
                    writer = csv.DictWriter(csvf, fieldnames=record.keys())

                    if write_header:
                        writer.writeheader()

                    writer.writerow(record)
