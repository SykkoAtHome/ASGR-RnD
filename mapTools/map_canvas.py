import math
import userData.userData as user
import pandas as pd
from PIL import Image
from matplotlib import pyplot as plt


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




def map_canvas(user_id, game_id, zoom):
    smurl = r"http://a.tile.openstreetmap.org/{0}/{1}/{2}.png"
    # build dataframe from database
    dataframe = pd.DataFrame(data=user.location_data(user_id, game_id))

    # calculate min and max values for setting up the region
    top, bottom, right, left = set_bounding_box(dataframe)

    #  create rectangle in mercator format
    x0, y0 = deg2num(top, left, zoom)
    x1, y1 = deg2num(bottom, right, zoom)

    #  calculates tiles
    x0_tile, y0_tile = int(x0 / 256), int(y0 / 256)
    x1_tile, y1_tile = math.ceil(x1 / 256), math.ceil(y1 / 256)
    numberOfTiles = (x0_tile - x1_tile) * (y0_tile - y1_tile)
    # calculate columns and rows
    columns = (x1_tile - x0_tile)
    rows = (y1_tile - y0_tile)

    # calculate canvas size (list)
    canvas_size = (columns*256, rows*256)

    # create empty canvas
    canvas = Image.new("RGB", canvas_size)

    plt.imshow(canvas)
    plt.show()




map_canvas(1,1,18)
