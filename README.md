# Meraki L3 ACL Updater

Backup and Update scripts for L3 ACL rules across all networks within a single Meraki organisation.

## Description

This project aims to provide the scripts needed to automate the interaction with maintaining L3 ACL rules across multiple networks in a single Meraki organisation. 

Currently the project will provide script to carry out the following tasks:

1. Back up the existing configuration for each Network in a single Meraki organisation to a dedicated JSON file.

2. Append new rules onto the end of the existing L3 ACL for each network in a single Meraki organisation while maintaining a Deny Any Any at the end.

You will need to ensure you have the following information from the Meraki dashboard prior to using this project:
1. Meraki API Key with either RO (Backup only) or RW.
2. Meraki Organisation ID.

## Getting Started

### Installing

The easiest way to download the project is to clone the repository via Git.
```
git clone git@github.com:mckechniefraz/Meraki_L3_ACL_Updater.git
```


### Dependencies

All required dependencies can be found in the requirements.txt file.

To install the dependencies run the following command, its suggested to do so within a Python Virtual Environment. 

```
pip3 install -r requirements.txt
```

### Executing program

Before running the script please ensure you have
* Meraki API Key.
* Meraki Organisation ID.
* If running a virtual environment, ensure this is activated.
* Installed the required packages from requirements.txt.
* If running the update script, ensure the newrules.json is updated.

Run backup script

```
python3 meraki_acl_backup.py
```

Run update script

```
python3 meraki_acl_update.py
```


## Help

[Meraki API Getting Started](https://developer.cisco.com/meraki/api-latest/#!getting-started)

[Obtaining your Meraki API key](https://developer.cisco.com/meraki/api-latest/#!authorization/obtaining-your-meraki-api-key)


## License

This project is licensed under the MIT License - see the LICENSE file for details