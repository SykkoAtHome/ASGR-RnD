import userData.userData as user
import plotly.express as px

points = user.location_data(1,1)

fig = px.scatter_mapbox(points, lat="lat", lon="lon",
                        color_discrete_sequence=["red"], zoom=16)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_traces(marker={'size': 10})
fig.show()