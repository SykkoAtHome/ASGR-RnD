import math
import userData.userData as user
import pandas as pd
from PIL import Image
from matplotlib import pyplot as plt
import requests
from itertools import product
from io import BytesIO

tile_limit = 100

def deg2num(latitude, longitude, zoom):
    C = (256/(2*math.pi)) * 2**zoom

    x = C*(math.radians(longitude)+math.pi)
    y = C*(math.pi-math.log(math.tan((math.pi/4) + math.radians(latitude)/2)))

    return x, y


def set_bounding_box(dataframe):
    bbox_list = []
    bbox_list.append(dataframe['lat'].max())
    bbox_list.append(dataframe['lat'].min())
    bbox_list.append(dataframe['lon'].max())
    bbox_list.append(dataframe['lon'].min())
    return bbox_list

def canvas_size(user_id, game_id, zoom):
    dataframe = pd.DataFrame(data=user.location_data(user_id, game_id))
    # calculate min and max values for setting up the region
    top, bottom, right, left = set_bounding_box(dataframe)
    #  create rectangle in mercator format
    x0, y0 = deg2num(top, left, zoom)
    x1, y1 = deg2num(bottom, right, zoom)
    #  calculates tiles
    x0_tile, y0_tile = math.floor(x0 / 256), math.floor(y0 / 256)
    x1_tile, y1_tile = math.ceil(x1 / 256), math.ceil(y1 / 256)
    numberOfTiles = (x0_tile - x1_tile) * (y0_tile - y1_tile)
    # calculate columns and rows
    columns = (x1_tile - x0_tile)
    rows = (y1_tile - y0_tile)
    canvas_size = (columns * 256, rows * 256)
    aspect_ratio = canvas_size[0]/canvas_size[1]

    return columns * 256, rows * 256, columns, rows, aspect_ratio, numberOfTiles




def map_canvas(user_id, game_id, zoom):
    payload = {}
    headers = {
        'Host': 'tile.openstreetmap.org',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
    }

    URL = "https://tile.openstreetmap.org/{z}/{x}/{y}.png".format

    # build dataframe from database
    dataframe = pd.DataFrame(data=user.location_data(user_id, game_id))

    # calculate min and max values for setting up the region
    top, bottom, right, left = set_bounding_box(dataframe)

    #  create rectangle in mercator format
    x0, y0 = deg2num(top, left, zoom)
    x1, y1 = deg2num(bottom, right, zoom)

    #  calculates tiles
    x0_tile, y0_tile = math.floor(x0 / 256), math.floor(y0 / 256)
    x1_tile, y1_tile = math.ceil(x1 / 256), math.ceil(y1 / 256)
    numberOfTiles = (x0_tile - x1_tile) * (y0_tile - y1_tile)
    # calculate columns and rows
    columns = (x1_tile - x0_tile)
    rows = (y1_tile - y0_tile)
    assert numberOfTiles < tile_limit, f"Your CANVAS requires {numberOfTiles} tiles. Limit is {tile_limit}. Change ZOOM level!"

    # calculate canvas size (list)
    canvas_size = (columns*256, rows*256)

    # create empty canvas
    canvas = Image.new("RGB", canvas_size)
    for x_tile, y_tile in product(range(x0_tile, x1_tile), range(y0_tile, y1_tile)):
        with requests.get(URL(x=x_tile, y=y_tile, z=zoom), headers=headers, data=payload) as resp:
            resp.raise_for_status()  # just in case
            tile_img = Image.open(BytesIO(resp.content))

        # add each tile to the full size image
        canvas.paste(im=tile_img, box=((x_tile - x0_tile) * 256, (y_tile - y0_tile) * 256))



    # Crop to fit location data
    # x, y = x0_tile * 256, y0_tile * 256
    # canvas = canvas.crop((
    #     int(x0 - x),  # left
    #     int(y0 - y),  # top
    #     int(x1 - x),  # right
    #     int(y1 - y)))  # bottom

    return canvas


def plot_points(user_id, game_id, zoom):
    canvas_bg = canvas_size(user_id,game_id,zoom)  # width, height, columns, rows, aspect ratio
    #dataframe = pd.DataFrame(data=user.location_data(user_id, game_id))
    #top, bottom, right, left = set_bounding_box(dataframe)
    locationData = user.location_data(user_id, game_id)  # Dictionary
    latitudeData = []
    longitudeData = []
    conversionData = []
    mercatorData = []
    mercatorX = []
    mercatorY = []
    list_of_lists = [i for i in locationData.values()]
    for latitude in list_of_lists[0]:
        latitudeData.append(latitude)
    for longitude in list_of_lists[1]:
        longitudeData.append(longitude)
    for lat, lon in zip(latitudeData, longitudeData):
        pair = [lat,lon]
        conversionData.append(pair)

    for lat,lon in conversionData:
        mercatorData.append(deg2num(lat,lon,zoom))
    for mx, my in mercatorData:
        mercatorX.append(mx)
        mercatorY.append(my)
    locationData["mx"] = mercatorX
    locationData["my"] = mercatorY

    dataframe = pd.DataFrame(data=locationData)

plot_points(1,1,18)

# mapa = map_canvas(1,1,18)
# plt.imshow(mapa)
# plt.axis('off')
# plt.show()