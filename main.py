from flask import Flask
from flask import request
import openai
import requests
from dotenv import dotenv_values

app = Flask(__name__)

@app.route("/")
def index():
    coords = request.args.get("coords", "")
    if coords:
        fahrenheit = fahrenheit_from(coords)
    else:
        fahrenheit = ""
    return (
        """<center><form action="" method="get">
                Latitude and Longitude Coordinates separated by space: <input type="text" name="coords">
                <input type="submit" value="Enter lat / long coords separated by space">
            </form><center>"""
        + "<center>Fahrenheit: "
        + fahrenheit + "<center>"
    )


def fahrenheit_from(coords):
    """Convert Celsius to Fahrenheit degrees."""
    try:
        list_lat_long = coords.split(" ")
        lat = list_lat_long[0]
        long = list_lat_long[1]

        openai.api_key = dotenv_values(".env")['pass']
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt="Create a csv with ",
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        # accessing the part of the response we want
        sentence = response["choices"][0]["text"]
        # getting the value of the coordinates in array form
        print(sentence)
        return sentence
    except ValueError:
        return "invalid input"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
