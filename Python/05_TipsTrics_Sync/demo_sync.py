from arcgis.gis import GIS
gis = GIS("home")

map1 = gis.map("Nijmegen")
map1.basemap = "gray"
map1

from ipywidgets import HBox
map1 = gis.map("Nijmegen")
map1.basemap = "gray"
map2 = gis.map("Nijmegen")
map2.basemap = "satellite"
map1.sync_navigation(map2)
HBox([map1, map2])
