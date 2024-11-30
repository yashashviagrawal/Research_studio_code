import pandas as pd
import json
import re

def clean_float64_notation(material_str):
    """
    Cleans the `np.float64(...)` notation from the materials strings.
    Args:
        material_str (str): The raw string from the materials column.
    Returns:
        str: Cleaned string with valid numeric values.
    """
    # Replace `np.float64(value)` with the numeric `value`
    return re.sub(r'np\.float64\(([\d\.]+)\)', r'\1', material_str)

def convert_csv_to_json(input_csv, output_json):
    """
    Converts a CSV file into a JSON file following a specified structure.
    Args:
        input_csv (str): Path to the input CSV file.
        output_json (str): Path to save the output JSON file.
    """
    # Load the CSV file
    data = pd.read_csv(input_csv)


    # Clean the 'materials' column to fix JSON formatting issues
    data['materials'] = data['materials'].str.replace("'", '"').str.replace("None", "null")
    data['materials'] = data['materials'].apply(clean_float64_notation)

    # Parse the materials column into proper JSON objects
    try:
        data['materials'] = data['materials'].apply(json.loads)
    except json.JSONDecodeError as e:
        print(f"Error parsing materials column: {e}")
        return

    # Convert the entire DataFrame into a list of dictionaries (JSON structure)
    json_structure = data.to_dict(orient='records')

    # Save the JSON to a file
    with open(output_json, 'w') as json_file:
        json.dump(json_structure, json_file, indent=4)

    print(f"Conversion successful! JSON saved to {output_json}")

# Example usage
if __name__ == "__main__":
    input_csv_path = "datasets/wall_population.csv"
    output_json_path = "datasets/outputted.json"

    convert_csv_to_json(input_csv_path, output_json_path)
