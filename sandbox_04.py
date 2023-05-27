import pandas as pd
import userData.userData as user


heatmap = user.generate_user_heatmap_data(1,1,3)
map_center = user.location_center(1,1)
print(map_center)

import plotly.graph_objects as go
fig = go.Figure(go.Densitymapbox(lat=heatmap["lat"], lon=heatmap["lon"], z=heatmap["count"], radius=50))
fig.update_layout(mapbox_style="open-street-map", mapbox_center_lat=map_center[0], mapbox_center_lon=map_center[1])
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()