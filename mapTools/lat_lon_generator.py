import math
import random
from db import c, conn
from datetime import datetime

################## Fake Data Sim

userID = 1  # test user = 1
gameID = 1  # test game = 1
gameTotalTime = 60  # in minutes
latStart = 52.310386
lonStart = 20.973477
radius_meters = 100  # in meters

date = datetime.now().timestamp()  # Do not touch !
dateStart = date  # Do not touch !

#######################
fakeDateList = []

radius_degrees = radius_meters / (111000 * math.cos(math.radians(latStart)))

check = c.execute(f"SELECT EXISTS (SELECT * FROM location_events WHERE user_id = {userID});")
check = c.fetchall()

if check == 1:
    dateStart = c.execute(
        f"SELECT MAX(event_time) FROM location_events WHERE user_id = {userID} AND game_id = {gameID}")
    dateStart = c.fetchall()

    for x in dateStart:
        dateStart = x[0].timestamp()
else:
    pass

# generate dateEnd as timestamp
dateEnd = dateStart + (gameTotalTime * 60)
dateTick = dateStart

while True:
    # generate Tick

    randomTick = random.randint(2, 8)
    milliseconds = format(random.randint(100000, 999990), '06d')

    dateTick = dateTick + randomTick
    dateTickNew = str(dateTick)
    dateTickNew = float(dateTickNew[:-6] + milliseconds)

    fakeDateList.append(dateTickNew)
    time_end = dateTickNew

    if fakeDateList[len(fakeDateList) - 1] >= dateEnd:
        break


def generate_random_coords(lat, lon, radius):
    tick_count = 1
    for timestamp in fakeDateList:
        time = datetime.fromtimestamp(timestamp)

        latitude = round(random.uniform(lat - radius, lat + radius), 7)
        longitude = round(random.uniform(lon - radius, lon + radius*2), 7)

        c.execute(
            f"INSERT INTO location_events "
            f"(user_id, game_id, event_time, latitude, longitude, event_type, tick_count)"
            f" VALUES ({userID}, {gameID}, '{time}', '{latitude}', '{longitude}', 6, {tick_count});")

        tick_count += 1
    print(f"Ticks: {tick_count}\n"
          f"Time Start: {datetime.fromtimestamp(date)}\n"
          f"Time End: {datetime.fromtimestamp(time_end)}")

generate_random_coords(latStart, lonStart, radius_degrees)
conn.commit()
conn.close()
