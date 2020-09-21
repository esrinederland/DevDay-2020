from arcgis.gis import GIS
from arcgis._impl.common._utils import _to_utf8
import arcgis

import security
import requests
import datetime

def main():

    portal = GIS("https://maps.arcgis.com", security.username, security.password)

    # Delete existing users with the 'Leerling' role
    role = "Leerling"
    print("Deleting all users with role: {}".format(role))
    roleId = "tH9rpbADx0KzPyof"

    for user in portal.users.search(role=roleId):

        userItems = user.items()

        print("Deleting user: {}".format(user.username))
        if user.delete(reassign_to=security.username):
            print("Successfull")
    
        print("Deleting all items from user")
        if portal.content.delete_items(userItems):
            print("Successfull")

    # Add new users with the 'Leerling' role
    with open("Leerlingen_S1.csv") as csvFile:
        for line in csvFile:
            student = line.split(",")
            firstname = student[0]
            lastname = student[1]
            username = "{}_{}".format(firstname, lastname)
            email = student[2].strip()
            password = security.studentPassword

            print("Creating account for student: {}".format(username))
            studentUser = portal.users.create(username=username, password=password, firstname=firstname, lastname=lastname, email=email)
            if studentUser:
                print("Successfull")

            print("Setting role to: {}".format(role))
            if studentUser.update_role(roleId):
                print("Successfull")


    # Clone lesmateriaal to new student
    folderName = "Lesmateriaal"
    print("Getting group content from folder: {}".format(folderName))
    items = portal.users.me.items(folderName)
    newItems = portal.content.clone_items(items, copy_data=True, owner=username)
    for newItem in newItems:
        print("Cloned item: {} for user: {}".format(newItem.title, username))

    # Modify organization settings
    print("Editing portal settings")
    portalUX = arcgis.gis.admin.UX(portal)
    portalUX.name = "Semester 1"
    portalUX.description = "Portaal voor semester 1"
    portalUX.set_banner("banner-3", is_built_in=True)
    portalUX.set_logo(logo_file=None)
    portalUX.set_logo(logo_file=r"Asterix.png")
    portalUX.featured_content = "ffc7db2c7a5346f4a183fe7b346ded5a"

    print("Script completed")

if __name__ == "__main__":
    main()
    