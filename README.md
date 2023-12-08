# GVE DevNet Network Visualization
This repository contains the source code for a script that will connect to all devices in a network specified in the YAML testbed file and then parse through the response of some CLI commands involving the interfaces, the memory processes, the CPU processes, and the OSPF neighbors and writes them to an Excel file.

## Contacts
* Danielle Stacy

## Solution Components
* Python 3.11
* pyATS and Genie
* Pandas
* Excel
* Catalyst Switches
* Nexus Switches

## Prerequisites
Configure network_testbed.yml for your network devices
```
devices:
  [ device-name ]:
    os: [ ios | iosxe | nxos ]
    type: [ switch | router ]
    connections:
      defaults:
        class: unicon.Unicon
      cli:
        protocol: ssh
        ip: [ x.x.x.x ]
        username: [ xxxx ]
        password: [ xxxx ]
```
Replace the strings in the brackets [] with the appropriate values for your network, deleting the brackets as you do. If you have more than one device, copy the lines from the device name to the password and paste them directly under the last line. Make sure that the new lines are indented at the same level as the lines above them. To learn more about the testbed file for pyATS and Genie, read [here](https://pubhub.devnetcloud.com/media/pyats-getting-started/docs/quickstart/manageconnections.html#creating-testbed-yaml-file).

## Installation/Configuration
1. Clone this repository with the command: `git clone https://github.com/gve-sw/gve_devnet_network_visualization_dashboard.git`.
2. Set up a Python virtual environment. Make sure Python 3 is installed in your environment, and if not, you may download Python [here](https://www.python.org/downloads/). Once Python 3 is installed in your environment, you can activate the virtual environment with the instructions found [here](https://docs.python.org/3/tutorial/venv.html).
3. Install the requirements with `pip3 install -r requirements.txt`.

## Usage
To run the script, enter the following command:
```
$ python network_analytics.py
```

The code will output information if one of the commands could not be run, including which command failed and the reason why it failed. Once the code is complete, it will have created a spreadsheet entitled network_analysis.xlsx in the same directory as the code. This will contain the information parsed from the CLI commands.

# Screenshots

![/IMAGES/0image.png](/IMAGES/0image.png)

![/IMAGES/nxos_intf.png](/IMAGES/nxos_intf.png)

![/IMAGES/nxos_memory.png](/IMAGES/nxos_memory.png)

![/IMAGES/nxos_cpu.png](/IMAGES/nxos_cpu.png)

![/IMAGES/ios_intf.png](/IMAGES/ios_intf.png)

![/IMAGES/ios_memory.png](/IMAGES/ios_memory.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.