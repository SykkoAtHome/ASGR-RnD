from db import c, conn

def gather_locations(user_id, game_id):
    userCheck = c.execute(f"SELECT exists (SELECT * from location_events WHERE user_id = {user_id}) AS extists;")
    userCheck = c.fetchall()
    gameCheck = c.execute(f"SELECT exists (SELECT * from location_events WHERE user_id = {game_id}) AS extists;")
    gameCheck = c.fetchall()

    location = {}

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
            location["lat"] = lat_list
            lon_list.append(float(y))
            location["lon"] = lon_list
            time_list.append(str(z))
            location["time"] = time_list
        for x in range(len(locationData)):
            user_list.append(user_id)
            location["user_id"] = user_list
        for x in range(len(locationData)):
            game_list.append(game_id)
            location["game_id"] = game_list
    else:
        conn.close()
        print("Either user_id or game_id does not exist.")

    return location