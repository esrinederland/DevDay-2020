#-------------------------------------------------------------------------------
# Name:        Security demo
# Purpose:     GISTech/GISConverentie 2020
#
# Author:      EsriNL DevTeam (PM)
#
# Created:     20200819
# Copyright:   (c) Esri Nederland 2020
# Licence:     MIT License
#-------------------------------------------------------------------------------
# package requirements
# pip install arcgis
#-------------------------------------------------------------------------------

import arcgis 

#ArcGIS Online username the script uses
_portalUsername = "pmallo_esrinl"

#Portal url
_portalUrl = "https://www.arcgis.com"

def main():    
    try:
        print ("ArcGIS Version: " + arcgis.__version__)
        gis = GetGIS()

        items = gis.content.search('Zwolle', 'feature layer')
        for item in items:
            print(item)

    except:
        print("Error in main") 

    print("Demo gereed")


def GetGIS():
    ###############################
    # demo keyring
    ###############################
    import keyring

    password = keyring.get_password("security", _portalUsername)
    gis = arcgis.GIS(_portalUrl, _portalUsername, password)

    print("Successfully logged into '{}' via the '{}' user".format(gis.properties.portalHostname,gis.properties.user.username)) 

    return gis


if __name__ == "__main__":
    main()