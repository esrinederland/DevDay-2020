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

import getpass
import keyring
import keyring.errors


password = getpass.getpass()
username = "pmallo_esrinl"

name = "security"

try:
    keyring.set_password(name, username, password)
    print("wachtwoord opgeslagen")
except (RuntimeError, keyring.errors.KeyringError) as e:
    raise KeyRingError(
        "Unable to store the password for {} in the key ring: {}".format(name, str(e))
        )
