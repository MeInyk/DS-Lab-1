import xml.etree.ElementTree as ET
import csv
from typing import List, Dict


def parse_weather_xml(xml_file: str) -> List[Dict[str, any]]:
    """
    Parse weather data from an XML file.

    Args:
        xml_file (str): Path to the XML file.

    Returns:
        list of dict: A list of dictionaries with parsed weather data.

    Raises:
        FileNotFoundError: If the XML file does not exist.
        ET.ParseError: If the XML file is malformed.
    """
    with open(xml_file, "r", encoding="utf-8") as file:
        tree = ET.parse(file)

    root = tree.getroot()
    weather_data = []

    for day in root.findall("day"):
        weather_data.append({
            "date": day.findtext("date"),
            "temperature": float(day.findtext("temperature")),
            "humidity": int(day.findtext("humidity")),
            "precipitation": float(day.findtext("precipitation"))
        })

    return weather_data



def save_to_csv(data: List[Dict[str, any]], filename: str = "parsed_weather_data.csv") -> None:
    """
    Save parsed weather data to a CSV file.

    Args:
        data (list of dict): Parsed weather data.
        filename (str): Name of the CSV file.

    Raises:
        IOError: If there is an error writing to the file.
    """
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(["Date", "Temperature", "Humidity", "Precipitation"])

        for day in data:
            writer.writerow([
                day["date"],
                day["temperature"],
                day["humidity"],
                day["precipitation"]
            ])


if __name__ == "__main__":
    try:
        # Parse the XML file
        import os
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        xml_path = os.path.join(script_dir, "weather_data.xml")
        weather_data = parse_weather_xml(xml_path)

        # Save the parsed data to a CSV file
        save_to_csv(weather_data)
        print("Data has been successfully parsed and saved to parsed_weather_data.csv.")
    except Exception as e:
        print(f"An error occurred: {e}")
