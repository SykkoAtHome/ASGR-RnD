from db import c, conn
from datetime import datetime
import pandas as pd



def location_data(user_id, game_id):
    sql = c.execute(f"SELECT exists (SELECT * from location_events WHERE user_id = {user_id}) AS extists;")
    userCheck = c.fetchall()
    sql = c.execute(f"SELECT exists (SELECT * from location_events WHERE user_id = {game_id}) AS extists;")
    gameCheck = c.fetchall()


    user_locations = {}

    for x in userCheck:
        userExists = int(x[0])

    for y in gameCheck:
        gameExists = int(y[0])

    if userExists and gameExists:
        locationdb = c.execute("SELECT latitude, longitude, event_time from location_events WHERE user_id = 1 AND game_id = 1;")
        locationData = c.fetchall()

        lat_list, lon_list, time_list, user_list, game_list = [], [], [], [], []

        for x,y,z in locationData:
            lat_list.append(float(x))
            user_locations["lat"] = lat_list
            lon_list.append(float(y))
            user_locations["lon"] = lon_list
            time_list.append(str(z))
            user_locations["time"] = time_list
        for x in range(len(locationData)):
            user_list.append(user_id)
            user_locations["user_id"] = user_list
        for x in range(len(locationData)):
            game_list.append(game_id)
            user_locations["game_id"] = game_list

        return user_locations  # dictionary
    else:
        conn.close()
        return "Either user_id or game_id does not exist."


def location_center(user_id, game_id):
    dataframe = pd.DataFrame(data=location_data(user_id, game_id))
    min_lat = dataframe['lat'].min()
    max_lat = dataframe['lat'].max()
    min_lon = dataframe['lon'].min()
    max_lon = dataframe['lon'].max()

    center_lat = (min_lat + max_lat) / 2
    center_lon = (min_lon + max_lon) / 2

    return center_lat, center_lon


def generate_user_heatmap_data(user_id, game_id, resolution):
    dataframe = pd.DataFrame(data=location_data(user_id, game_id))

    rounded_data = dataframe.round({"lat": resolution, "lon": resolution})
    rounded_data["count"] = 1

    grouped_data = rounded_data.groupby(["lat", "lon"]).count().reset_index()

    heatmap_data = {
        "lat": [],
        "lon": [],
        "count": []
    }

    for index, row in grouped_data.iterrows():
        lat = row["lat"]
        lon = row["lon"]
        count = row["count"]

        heatmap_data["lat"].append(lat)
        heatmap_data["lon"].append(lon)
        heatmap_data["count"].append(int(count))

    return heatmap_data


def get_last_location(user_id, game_id):
    sql = f"SELECT latitude, longitude, event_time from location_events WHERE user_id = {user_id} AND game_id = {game_id} ORDER BY event_time DESC LIMIT 1;"
    c.execute(sql)
    dane = c.fetchall()
    conn.close()
    last_location = []
    for x in dane:
        last_location.append(float(x[0]))
        last_location.append(float(x[1]))
        last_location.append(str(x[2]))

    return last_location  # list


def set_location(user_id, game_id, latitude, longitude):
    time = datetime.now()
    sql = f"INSERT INTO location_events (user_id, game_id, event_time, latitude, longitude, event_type) VALUES ({user_id}, {game_id}, '{time}', {latitude}, {longitude}, 6);"
    c.execute(sql)
    conn.close()





def get_name(user_id):

    sql = f"SELECT username FROM users WHERE user_id={user_id}"
    c.execute(sql)
    dane = c.fetchall()
    conn.close()
    for tuple in dane:
        for username in tuple:

            return str(username)


def get_display_name(user_id):
    sql = f"SELECT display_name FROM users WHERE user_id={user_id}"
    c.execute(sql)
    dane = c.fetchall()
    conn.close()
    for tuple in dane:
        for displayname in tuple:

            return str(displayname)







