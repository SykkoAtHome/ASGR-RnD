from multiprocessing import Queue
import geoplotlib
from geoplotlib.utils import read_csv

data = read_csv("sample_data.csv")
geoplotlib.dot(data,point_size=3)
geoplotlib.show()