import csv
import re
from typing import List, Dict


def clean_text(line: str) -> str:
    """
    Clean the text line by removing non-ASCII characters and fixing known issues.

    Args:
        line (str): The line of text to clean.

    Returns:
        str: The cleaned line of text.
    """
    # Replace non-breaking spaces and other non-ASCII characters
    line = line.replace("\u00a0", " ")
    line = line.replace("°", "")
    line = line.replace("−", "-")
    line = line.replace("–", "-")

    return line.encode("ascii", errors="ignore").decode("ascii")


def extract_weather_data(text_file: str) -> List[Dict[str, any]]:
    """
    Extract weather data from a text file using regular expressions.

    Args:
        text_file (str): Path to the text file.

    Returns:
        list of dict: A list of dictionaries with extracted weather data.

    Raises:
        FileNotFoundError: If the text file does not exist.
    """
    weather_data = []

    pattern = (
        r"Date:\s*(\d{4}-\d{2}-\d{2}),\s*"
        r"Max Temp:\s*(-?\d+(?:\.\d+)?)C,\s*"
        r"Min Temp:\s*(-?\d+(?:\.\d+)?)C,\s*"
        r"Humidity:\s*(\d+)%,\s*"
        r"Precipitation:\s*(\d+(?:\.\d+)?)mm"
    )

    with open(text_file, "r", encoding="utf-8") as file:
        for line in file:
            cleaned_line = clean_text(line)
            match = re.search(pattern, cleaned_line)

            if match:
                weather_data.append({
                    "date": match.group(1),
                    "max_temperature": float(match.group(2)),
                    "min_temperature": float(match.group(3)),
                    "humidity": int(match.group(4)),
                    "precipitation": float(match.group(5))
                })

    return weather_data


def save_to_csv(data: List[Dict[str, any]], filename: str = "extracted_weather_data.csv") -> None:
    """
    Save extracted weather data to a CSV file.

    Args:
        data (list of dict): Extracted weather data.
        filename (str): Name of the CSV file.

    Raises:
        IOError: If there is an error writing to the file.
    """
    headers = ["Date", "Max Temperature", "Min Temperature", "Humidity", "Precipitation"]

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        for day in data:
            writer.writerow([
                day["date"],
                day["max_temperature"],
                day["min_temperature"],
                day["humidity"],
                day["precipitation"]
            ])


if __name__ == "__main__":
    try:
        # Extract data from the text file
        import os
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        txt_path = os.path.join(script_dir, "weather_report.txt")
        weather_data = extract_weather_data(txt_path)

        # Save the extracted data to a CSV file
        save_to_csv(weather_data)
        print("Data has been successfully extracted and saved to extracted_weather_data.csv.")
    except Exception as e:
        print(f"An error occurred: {e}")
