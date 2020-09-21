import arcgis
import logging

logging.basicConfig(level=logging.DEBUG )
gis = arcgis.gis.GIS("PRO")

item = gis.content.get("e8f55ab6170f4a72af5ab0860210b435")

res = gis.content.clone_items([item])

print(res)
print("script complete")