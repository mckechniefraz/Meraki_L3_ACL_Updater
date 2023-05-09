"""
This script will backup your existing l3 ACL for all networks within a single Meraki Organision to the backup folder. 

To run this script you will need:
1. A Read Only or Read Write API Key
2. To know your unique Meraki Organisation ID
"""

import os
import random
import meraki
import sys
import json


def merakiError(e):
    """
    Function to print the error generated by Meraki's SDK during any API call made to via the SDK with a try logic attached.
    Args:
            e (String): Error message generated and formatted by the Meraki SDK.
    """
    print(f"Meraki API error: {e}")


def pythonError(e):
    """
    Function to print the error generated by Python during any API calls made with a try logic attached.
    Args:
            e (String): Python Error message.
    """
    print(f"Python API error: {e}")


def setupScript():
    """
    Function to setup the script,  including input of required variables and creating the backup folder structure. 

    In an attempt to not overwrite existing backups if the folder alredy exists, it will add a two digit number to the end of the path.

    Returns:
        apiKey(String): API Key to authenticate against the Meraki API (RW or RO).
        orgId(String): Unique Org Id of the Meraki organisation that this script should run against.
        backupFolderpath(String): Folder path of where to save backup files.
    """
    apiKey = input("Please enter your Meraki API Key: ")
    orgId = input("Please enter your Meraki OrgId: ")
    backupFolderName = input(
        "Please enter the of the folder to save backups to: ")

    if os.path.exists(f"backup/{backupFolderName}") != True:
        os.mkdir(f"backup/{backupFolderName}")
        print(f"Creating folder: backup/{backupFolderName}")
        backupFolderpath = f"backup/{backupFolderName}"
    else:
        backupFolderNameRandom = f"{backupFolderName}_{random.randint(1, 99)}"
        os.mkdir(f"backup/{backupFolderNameRandom}")
        print(
            f"Path backup/{backupFolderName} already exists, creating path as backup/{backupFolderNameRandom}")
        backupFolderpath = f"backup/{backupFolderNameRandom}"

    return apiKey, orgId, backupFolderpath


def getMerakiNetworkList(orgId):
    """
    Function to query the Meraki API and provide a list of Meraki Networks which have appliance in their product type list. 

    Args:
        orgId (String): Unique Org Id of the Meraki organisation that this script should run against.

    Returns:
        networkListFiltered (List): Filtered X of all Meraki Networks within the Organisation which have an appliance in their product type list.
    """

    networkList = []

    try:
        networkList = dashboard.organizations.getOrganizationNetworks(
            organizationId=orgId, total_pages="all")
    except meraki.APIError as e:
        merakiError(e)
        sys.exit(1)

    except Exception as e:
        pythonError(e)
        sys.exit(1)

    networkListFiltered = []

    for network in networkList:
        if "appliance" in network["productTypes"]:
            networkListFiltered.append(network)
            print(network["name"])

    return networkListFiltered


def backupL3Acl(networkInfo, backupPath):
    """
    Function to pull the current L3 ACL and creates a JSON file based on the network name at the provided folder path. 

    Args:
        networkInfo (Dict): Dict of the network's configuration provided by the Meraki dashboard including Name and unique Network ID.
        backupPath (String): Path where the backup of the network should be stored. 
    """

    networkL3Acl = []
    networkName = networkInfo["name"]
    try:
        networkL3Acl = dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules(
            networkId=networkInfo["id"])
    except meraki.APIError as e:
        merakiError(e)
        sys.exit(1)

    except Exception as e:
        pythonError(e)
        sys.exit(1)

    with open(f"{backupPath}/{networkName}.json", "w") as outputfile:

        json.dump(networkL3Acl, outputfile, indent=4)

    print(f"Backing up of {networkName} complated")


if "__main__" == __name__:

    """
    This is what is run when the file is run directly, this will setup the script, get a list of Meraki networks and back each up.
    """

    apiKey, orgId, backupFolderPath = setupScript()

    dashboard = meraki.DashboardAPI(api_key=apiKey,
                                    print_console=False,
                                    log_path="logs",
                                    retry_4xx_error=True)

    merakiNetworkList = getMerakiNetworkList(orgId=orgId)

    for network in merakiNetworkList:
        backupL3Acl(networkInfo=network, backupPath=backupFolderPath)
