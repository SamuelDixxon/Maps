import requests
import csv
from dotenv import dotenv_values
from io import open as iopen

# defining a function, it takes four parameters:
# the path to a csv file containing lat/lon coordinates
# your API key
# the zoom level you would your images to be downloaded as
# the size, in pixels of your images, the maximum is 640


def satellite_squares(csvforimport, APIkey, zoom, size):
    API_KEY = APIkey
    base = "https://maps.googleapis.com/maps/api/staticmap?scale=2&size="
    locations = []
    # this section reads the csv file
    with open(csvforimport, 'rt') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)
            ind, lat, lng = str(row[0]), float(row[1]), float(row[2])
            location = (ind, lat, lng)
            locations.append(location)
    # here we format a url to pass to the API for each row in the csv file
    for location in locations:
        ind, lat, lng = location
        latlng = "center={},{}".format(lat, lng)
        view = "zoom={}&maptype=satellite".format(zoom)
        keys = "key={}".format(API_KEY)
        url = "{}{}x{}&{}&{}&{}".format(base, size, size, latlng, view, keys)
        # defining the name for the image files that will be downloaded
        filename = "{}_{}.png".format(ind, zoom)
        res = requests.get(url)
        if res.status_code == requests.codes.ok:
            with iopen(filename, 'wb') as file:
                file.write(res.content)
            print(filename)
        # here we tell the function to show us an error message if it is unable to download an image
        else:
            print(res.status_code)
            print(url)
            return False


satellite_squares("data.csv", dotenv_values(".env")['pass2'], 13, 640)
