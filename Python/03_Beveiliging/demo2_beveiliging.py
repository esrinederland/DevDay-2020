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

        items = gis.content.search('Rotterdam', 'feature layer')
        for item in items:
            print(item)

    except:
        print("Error in main") 

    print("Demo gereed")


def GetGIS():
    ###############################
    # demo Python
    ###############################
    profileName = "arcgis_{}".format(_portalUsername)
    print(profileName)
    
    #get GIS
    gis = arcgis.GIS(_portalUrl, profile=profileName)

    #if the users.me is None, logging in through the profilename did not succeed. Then get a password and create the profile
    if gis.users.me is None:
        import getpass
        pwd = getpass.getpass("Voer een wachtwoord in: ")
        gis = arcgis.GIS(_portalUrl, username=_portalUsername, password=pwd, profile=profileName)

    print("Successfully logged into '{}' via the '{}' user".format(gis.properties.portalHostname,gis.properties.user.username)) 

    return gis

if __name__ == "__main__":
    main()