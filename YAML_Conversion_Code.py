import os
import yaml
import pandas as pd

# Main data folder
input_folder = "data"

# Output folder for CSV
output_folder = "csv_output"
os.makedirs(output_folder, exist_ok=True)

# Walk through all month subfolders
for month_folder in os.listdir(input_folder):
    month_path = os.path.join(input_folder, month_folder)

    # Skip if not a folder
    if not os.path.isdir(month_path):
        continue

    # Loop YAML files inside the month folder
    for file in os.listdir(month_path):
        if file.endswith(".yaml") or file.endswith(".yml"):
            
            yaml_path = os.path.join(month_path, file)

            # CSV filename (same name but .csv)
            csv_filename = file.replace(".yaml", ".csv").replace(".yml", ".csv")
            csv_path = os.path.join(output_folder, csv_filename)

            # Load YAML file
            with open(yaml_path, "r") as f:
                data = yaml.safe_load(f)

            # Convert YAML → Flat table
            df = pd.json_normalize(data, sep="_")

            # Save CSV
            df.to_csv(csv_path, index=False)

            print(f"Converted: {yaml_path} → {csv_path}")

print("\n✔️ All YAML files from all subfolders converted successfully!")