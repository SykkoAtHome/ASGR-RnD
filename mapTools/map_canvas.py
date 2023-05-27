import math
import userData.userData as user
import pandas as pd
from PIL import Image
from matplotlib import pyplot as plt
import requests
from itertools import product
from io import BytesIO
from mpl_toolkits.basemap import Basemap

tile_limit = 100


def deg2num(latitude, longitude, zoom):
    C = (256/(2*math.pi)) * 2**zoom

    x = C*(math.radians(longitude)+math.pi)
    y = C*(math.pi-math.log(math.tan((math.pi/4) + math.radians(latitude)/2)))

    return x, y


def oom_deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)


def oom_num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)


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
    canvas = Image.new("RGB", canvas_size)


    # x, y = x0_tile * 256, y0_tile * 256
    # canvas = canvas.crop((
    #     int(x0 - x),  # left
    #     int(y0 - y),  # top
    #     int(x1 - x),  # right
    #     int(y1 - y)))  # bottom
    # print(canvas.size)

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
    # print(x0_tile, y0_tile)
    # print(x1_tile, y1_tile)

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



    # #Crop to fit location data
    # x, y = x0_tile * 256, y0_tile * 256
    # canvas = canvas.crop((
    #     int(x0 - x),  # left
    #     int(y0 - y),  # top
    #     int(x1 - x),  # right
    #     int(y1 - y)))  # bottom

    return canvas


def tile_corners_to_latlon(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad_nw = math.atan(math.sinh(math.pi * (1 - 2 * (ytile / n))))
    lat_deg_nw = math.degrees(lat_rad_nw)

    lat_rad_se = math.atan(math.sinh(math.pi * (1 - 2 * ((ytile + 1) / n))))
    lat_deg_se = math.degrees(lat_rad_se)

    lat_deg_nw = max(min(lat_deg_nw, 85.0511), -85.0511)
    lat_deg_se = max(min(lat_deg_se, 85.0511), -85.0511)

    top_left = (lat_deg_nw, lon_deg)
    top_right = (lat_deg_nw, lon_deg + (360.0 / n))
    bottom_right = (lat_deg_se, lon_deg + (360.0 / n))
    bottom_left = (lat_deg_se, lon_deg)

    return top_left, top_right, bottom_left, bottom_right


def plot_points(user_id, game_id, zoom):
    canvas_bg = canvas_size(user_id, game_id, zoom)  # width, height, columns, rows, aspect ratio
    columns, rows = canvas_bg[2], canvas_bg[3]
    aspect_ratio = columns/rows




    pd.set_option('display.float_format', '{:.8f}'.format)
    locationData = user.location_data(user_id, game_id)  # Dictionary


    dataframe = pd.DataFrame(data=locationData)

    top, bottom, right, left = set_bounding_box(dataframe)
    topMerc, leftMerc = oom_deg2num(top, left, zoom)
    upperLeftX, upperLeftY = topMerc, leftMerc
    bottomLeftX, bottomLeftY = upperLeftX, upperLeftY+rows-1
    upperRightA, upperRightB = upperLeftX+columns-1, bottomLeftY-rows+1


    llcrnrlat, llcrnrlon = tile_corners_to_latlon(bottomLeftX, bottomLeftY, zoom)[2]
    urcrnrlat, urcrnrlon = tile_corners_to_latlon(upperRightA, upperRightB, zoom)[1]

    llcrnrlat, urcrnrlat, llcrnrlon, urcrnrlon = \
        round(llcrnrlat, 6), round(urcrnrlat, 6), round(llcrnrlon, 6), round(urcrnrlon, 6)

    print(columns, rows)
    fig = plt.figure(figsize=(columns, rows), dpi=256)

    ax = fig.add_subplot(111)

    m = Basemap(llcrnrlat=llcrnrlat,
                urcrnrlat=urcrnrlat,
                llcrnrlon=llcrnrlon,
                urcrnrlon=urcrnrlon,
                resolution="l")

    x, y = m(locationData['lon'], locationData['lat'])
    m.scatter(x, y, c='red', marker='o', s=50, alpha=0.7)
    #ax.set_aspect(aspect_ratio)
    plt.gca().set_aspect(aspect_ratio)

    fig.tight_layout(rect=[0, 0, 1, 1])
    #plt.axis('equal')
    plt.axis('off')

    fig.savefig('points.png', transparent=True, bbox_inches='tight', pad_inches=0)



plot_points(1,1,18)
plt.show()

# mapa = map_canvas(1,1,18)
# plt.imshow(mapa)
# plt.axis('off')
# mapa.save('mapBG.png', format='PNG')
# plt.show()