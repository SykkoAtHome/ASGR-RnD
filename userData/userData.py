import os
import sys
sys.path.append("../db")
from db import c, conn



from datetime import datetime


def gather_user_locations(user_id, game_id):
    userCheck = c.execute(f"SELECT exists (SELECT * from location_events WHERE user_id = {user_id}) AS extists;")
    userCheck = c.fetchall()
    gameCheck = c.execute(f"SELECT exists (SELECT * from location_events WHERE user_id = {game_id}) AS extists;")
    gameCheck = c.fetchall()

    user_locations = {}

    for x in userCheck:
        userExists = x[0]

    for y in gameCheck:
        gameExists = y[0]

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
    else:
        conn.close()
        print("Either user_id or game_id does not exist.")

    return user_locations

def get_user_name(user_id):

    sql = f"SELECT username FROM users WHERE user_id={user_id}"
    c.execute(sql)
    dane = c.fetchall()
    for tuple in dane:
        for username in tuple:
            return str(username)


def get_display_name(user_id):

    sql = f"SELECT display_name FROM users WHERE user_id={user_id}"
    c.execute(sql)
    dane = c.fetchall()
    for tuple in dane:
        for displayname in tuple:
            return str(displayname)


def set_user_location(user_id, game_id, pos_x, pos_y):
    time = datetime.now()
    sql = f"INSERT INTO location_events (user_id, game_id, event_time, latitude, longitude, event_type) VALUES ({user_id}, {game_id}, '{time}', {pos_x}, {pos_y}, 6);"
    c.execute(sql)


#print(get_user_name(1))