import arcgis
import getpass
from datetime import date

datum = date.today().strftime("%Y%m%d")

password = getpass.getpass("Voer uw wachtwoord in: ")
gis = arcgis.GIS("http://www.arcgis.com", "pmallo_test", password)
print("Gebruiker ingelogd")

items = gis.content.search('', 'Feature layer')
print("Gevonden lagen:")
for item in items:
    print(item)

verkeersbordenLayer = items[5]

#Laten we nu deze gevonden laag exporteren en downloaden
exportName = "{}{}".format(verkeersbordenLayer.title, datum)
print('Export name: {}'.format(exportName))

fgdb = verkeersbordenLayer.export(title=exportName, export_format="File Geodatabase")

fgdb.download(r'E:\GISTech\2020\Demo\Backup')
print("script gereed")