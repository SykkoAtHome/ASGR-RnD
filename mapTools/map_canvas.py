import math
import userData.userData as user
import pandas as pd


def deg2num(latitude, longitude, zoom):
    lat_rad = math.radians(latitude)
    n = 2.0 ** zoom
    xtile = int((longitude + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)


def set_bounding_box(dataframe):
    bbox_list = []
    bbox_list.append(dataframe['lat'].max())
    bbox_list.append(dataframe['lat'].min())
    bbox_list.append(dataframe['lon'].max())
    bbox_list.append(dataframe['lon'].min())
    return bbox_list




def map_canvas(user_id, game_id, zoom):
        # build dataframe from database
        dataframe = pd.DataFrame(data=user.location_data(user_id, game_id))

        # calculate min and max values for setting up the region







map_canvas(1,1,18)
