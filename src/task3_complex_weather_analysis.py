from typing import Dict, List, Any

try:
    from .utils import load_json
except ImportError:
    from utils import load_json


def analyze_daily_weather(day: Dict[str, Any], temp_threshold: float = 30, 
                          wind_threshold: float = 15, humidity_threshold: float = 70) -> Dict[str, Any]:
    """
    Analyze weather data for a single day.

    Args:
        day (dict): The weather data for the day.
        temp_threshold (float): The temperature threshold to determine a hot day.
        wind_threshold (float): The wind speed threshold to determine a windy day.
        humidity_threshold (float): The humidity threshold to determine uncomfortable weather.

    Returns:
        dict: A dictionary with analysis results for the day.
    """
    max_temp = day["max_temperature"]
    min_temp = day["min_temperature"]
    wind_speed = day["wind_speed"]
    humidity = day["humidity"]
    precipitation = day["precipitation"]

    temperature_swing = max_temp - min_temp

    if precipitation == 0:
        rain_severity = "No rain"
    elif precipitation < 5:
        rain_severity = "Light rain"
    elif precipitation < 10:
        rain_severity = "Moderate rain"
    else:
        rain_severity = "Heavy rain"

    return {
        **day,
        "temperature_swing": temperature_swing,
        "is_hot_day": max_temp > temp_threshold,
        "significant_swing": temperature_swing > 10,
        "is_windy_day": wind_speed > wind_threshold,
        "is_uncomfortable_day": humidity > humidity_threshold,
        "is_rainy_day": precipitation > 0,
        "rain_severity": rain_severity
    }


def generate_daily_report(analysis: Dict[str, Any]) -> str:
    """
    Generate a detailed report based on the analysis results for a single day.

    Args:
        analysis (dict): The analysis results for the day.

    Returns:
        str: A detailed report as a string.
    """
    report = [
        f"Date: {analysis['date']}",
        f"Weather: {analysis['weather_description']}",
        (
            f"Temperature: Max {analysis['max_temperature']:.1f}°C, "
            f"Min {analysis['min_temperature']:.1f}°C "
            f"(Swing: {analysis['temperature_swing']:.1f}°C)"
        )
    ]

    if analysis["is_hot_day"]:
        report.append("It was a hot day.")

    if analysis.get("significant_swing", False):
        report.append("There was a significant temperature swing.")

    if analysis["is_windy_day"]:
        report.append("It was a windy day.")

    if analysis["is_uncomfortable_day"]:
        report.append("The humidity made the day uncomfortable.")

    if analysis["is_rainy_day"]:
        rain_severity = analysis.get("rain_severity", "Rain")
        report.append(f"It was a rainy day. Rain severity: {rain_severity}.")
    else:
        report.append("There was no precipitation.")

    return "\n".join(report) + "\n"


def summarize_weather_analysis(analyses: List[Dict[str, Any]]) -> str:
    """
    Summarize the weather analysis over multiple days.

    Args:
        analyses (list of dict): A list of daily analysis results.

    Returns:
        str: A summary report as a string.
    """
    if not analyses:
        return "No weather data available."

    hottest = max(analyses, key=lambda day: day["max_temperature"])
    windiest = max(analyses, key=lambda day: day["wind_speed"])
    most_humid = max(analyses, key=lambda day: day["humidity"])
    rainiest = max(analyses, key=lambda day: day["precipitation"])

    summary = [
        "Weather Summary:",
        (
            f"Hottest day: {hottest['date']} with a maximum "
            f"temperature of {hottest['max_temperature']:.1f}°C"
        ),
        (
            f"Windiest day: {windiest['date']} with wind speeds "
            f"of {windiest['wind_speed']:.1f} km/h"
        ),
        (
            f"Most humid day: {most_humid['date']} with a "
            f"humidity level of {most_humid['humidity']}%"
        ),
        (
            f"Rainiest day: {rainiest['date']} with "
            f"{rainiest['precipitation']:.1f} mm of precipitation"
        )
    ]

    return "\n".join(summary)


if __name__ == "__main__":
    try:
        # Load the JSON data
        import os
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "tokyo_weather_complex.json")
        weather_data = load_json(json_path)

        # Analyze the weather data for each day
        analyses = [analyze_daily_weather(day) for day in weather_data['daily']]

        # Generate and print daily reports
        for analysis in analyses:
            report = generate_daily_report(analysis)
            print(report)

        # Generate and print a summary report
        summary_report = summarize_weather_analysis(analyses)
        print(summary_report)
    except Exception as e:
        print(f"An error occurred: {e}")
