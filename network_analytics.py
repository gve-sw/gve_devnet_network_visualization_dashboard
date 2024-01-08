""" Copyright (c) 2023 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

# Import Section
import json
import os
import sys
from genie import testbed
import pandas as pd


def parse_interfaces(interfaces, device):
    """
    Create a list of dictionaries with the information from each interface.
    This information includes the device name, ip address, interface name, 
    whether the interface is enabled, the operating status, admin state, 
    auto negotiate status, bandwidth, mtu, port mode, output rate, and input 
    rate.
    :return: list of dictionaries 
    """
    interface_list = []
    for interface in interfaces:
        interface_info = {}
        interface_info["device"] = device["name"]
        interface_info["ip"] = device["ip"]
        interface_info["interface"] = interface
        interface_info["enabled"] = interfaces[interface]["enabled"]
        interface_info["oper_status"] = interfaces[interface]["oper_status"]
        if "admin_state" in interfaces[interface].keys():
            interface_info["admin_state"] = interfaces[interface]["admin_state"]
        else:
            interface_info["admin_state"] = "n/a"
        if "auto_negotiate" in interfaces[interface].keys():
            interface_info["auto_negotiate"] = interfaces[interface]["auto_negotiate"]
        else:
            interface_info["auto_negotiate"] = "n/a"
        if "bandwidth" in interfaces[interface].keys():
            interface_info["bandwidth"] = interfaces[interface]["bandwidth"]
        else:
            interface_info["bandwidth"] = "n/a"
        if "mtu" in interfaces[interface].keys():
            interface_info["mtu"] = interfaces[interface]["mtu"]
        else:
            interface_info["mtu"] = "n/a"
        if "port_mode" in interfaces[interface].keys():
            interface_info["port_mode"] = interfaces[interface]["port_mode"]
        else:
            interface_info["port_mode"] = "n/a"
        if "counters" in interfaces[interface].keys() and "rate" in interfaces[interface]["counters"].keys() and "out_rate_pkts" in interfaces[interface]["counters"]["rate"].keys():
            interface_info["out_rate"] = interfaces[interface]["counters"]["rate"]["out_rate_pkts"]
        else:
            interface_info["out_rate"] = "n/a"
        if "counters" in interfaces[interface].keys() and "rate" in interfaces[interface]["counters"].keys() and "in_rate_pkts" in interfaces[interface]["counters"]["rate"].keys():
            interface_info["in_rate"] = interfaces[interface]["counters"]["rate"]["in_rate_pkts"]
        else:
            interface_info["in_rate"] = "n/a"

        interface_list.append(interface_info)

    return interface_list

def parse_cpu_process(cpu_processes, device):
    """
    Create a list of dictionaries with the information from the cpu 
    processes. This information includes the device name, ip address, 
    the process id, process name, whether the process is invoked, the 
    runtime, and usecs.
    :return: list of dictionaries
    """
    cpu_process_list = []
    for key in cpu_processes:
            cpu_process_info = {}
            cpu_process_info["device"] = device["name"]
            cpu_process_info["ip"] = device["ip"]
            cpu_process_info["invoked"] = cpu_processes[key]["invoked"]
            cpu_process_info["p_id"] = cpu_processes[key]["pid"]
            cpu_process_info["process"] = cpu_processes[key]["process"]
            if "runtime_ms" in cpu_processes[key].keys():
                cpu_process_info["runtime"] = cpu_processes[key]["runtime_ms"]
            elif "runtime" in cpu_processes[key].keys():
                cpu_process_info["runtime"] = cpu_processes[key]["runtime"]
            cpu_process_info["usecs"] = cpu_processes[key]["usecs"]

            cpu_process_list.append(cpu_process_info)

    return cpu_process_list

def parse_memory_process(memory_processes, device):
    """
    Create a list of dictionaries with the information from the memory 
    processes of the IOS devices. This information includes the device name, 
    ip address, process id, process name, tty, the amount of memory allocated, 
    the amount of memory freed, how much is holding, the getbufs, and retbufs.
    :return: list of dictionaries
    """
    memory_process_list = []
    for key in memory_processes:
        for index in memory_processes[key]["index"]:
            memory_process_info = {}
            memory_process_info["device"] = device["name"]
            memory_process_info["ip"] = device["ip"]
            memory_process_info["p_id"] = memory_processes[key]["index"][index]["pid"]
            memory_process_info["process"] = memory_processes[key]["index"][index]["process"]
            memory_process_info["tty"] = memory_processes[key]["index"][index]["tty"]
            memory_process_info["allocated"] = memory_processes[key]["index"][index]["allocated"]
            memory_process_info["freed"] = memory_processes[key]["index"][index]["freed"]
            memory_process_info["holding"] = memory_processes[key]["index"][index]["holding"]
            memory_process_info["getbufs"] = memory_processes[key]["index"][index]["getbufs"]
            memory_process_info["retbufs"] = memory_processes[key]["index"][index]["retbufs"]
            memory_process_list.append(memory_process_info)

    return memory_process_list

def parse_nx_memory_process(memory_processes, device):
    """
    Create as list of dictionaries with the information from the memory 
    processes of the Nexus devices. This information includes the device 
    name, ip address, process id, process, the amount of memory allocated, 
    and the amount of memory used.
    :return: list of dictionaries
    """
    memory_process_list = []
    for key in memory_processes:
            for index in memory_processes[key]["index"]:
                    memory_process_info = {}
                    memory_process_info["device"] = device["name"]
                    memory_process_info["ip"] = device["ip"]
                    memory_process_info["p_id"] = memory_processes[key]["index"][index]["pid"]
                    memory_process_info["process"] = memory_processes[key]["index"][index]["process"]
                    memory_process_info["allocated"] = memory_processes[key]["index"][index]["mem_alloc"]
                    memory_process_info["used"] = memory_processes[key]["index"][index]["mem_used"]
                    memory_process_list.append(memory_process_info)

    return memory_process_list

def parse_ospf_neighbor(ospf_neighbors, device):
    """
    Create a list of dictionaries with the OSPF neighbor information of 
    each interface. This information includes the device name, ip address, 
    vrf, process id, area, interface, neighbor, router id, neighbor ip 
    address, neighbor state, neighbor priority, designated router ip 
    address, backup designated router ip address, and dead time.
    :return: list of dictionaries
    """
    ospf_neighbor_list = []
    for vrf in ospf_neighbors:
        for process in ospf_neighbors[vrf]["address_family"]["ipv4"]["instance"]:
            for area in ospf_neighbors[vrf]["address_family"]["ipv4"]["instance"][process]["area"]:
                for interface in ospf_neighbors[vrf]["address_family"]["ipv4"]["instance"][process]["area"][area]["interfaces"]:
                    for neighbor in ospf_neighbors[vrf]["address_family"]["ipv4"]["instance"][process]["area"][area]["interfaces"][interface]["neighbors"]:
                        ospf_neighbor_info = {}
                        ospf_neighbor_info["device"] = device["name"]
                        ospf_neighbor_info["ip"] = device["ip"]
                        ospf_neighbor_info["vrf"] = vrf
                        ospf_neighbor_info["process_id"] = process
                        ospf_neighbor_info["area"] = area
                        ospf_neighbor_info["interface"] = interface
                        ospf_neighbor_info["neighbor"] = neighbor
                        ospf_neighbor_info["router_id"] = ospf_neighbors[vrf]["address_family"]["ipv4"]["instance"][process]["areas"][area]["interfaces"][interface]["neighbors"][neighbor]["neighbor_router_id"]
                        ospf_neighbor_info["address"] = ospf_neighbors[vrf]["address_family"]["ipv4"]["instance"][process]["areas"][area]["interfaces"][interface]["neighbors"][neighbor]["address"]
                        if "state" in ospf_neighbors[vrf]["address_family"]["ipv4"]["instance"][process]["areas"][area]["interfaces"][interface]["neighbors"][neighbor].keys():
                            ospf_neighbor_info["state"] = ospf_neighbors[vrf]["address_family"]["ipv4"]["instance"][process]["areas"][area]["interfaces"][interface]["neighbors"][neighbor]["state"]
                        else:
                            ospf_neighbor_info["state"] = "n/a"
                        if "priority" in ospf_neighbors[vrf]["address_family"]["ipv4"]["instance"][process]["areas"][area]["interfaces"][interface]["neighbors"][neighbor].keys():
                            ospf_neighbor_info["priority"] = ospf_neighbors[vrf]["address_family"]["ipv4"]["instance"][process]["areas"][area]["interfaces"][interface]["neighbors"][neighbor]["priority"]
                        else:
                            ospf_neighbor_info["priority"] = "n/a"
                        if "dr_ip_addr" in ospf_neighbors[vrf]["address_family"]["ipv4"]["instance"][process]["areas"][area]["interfaces"][interface]["neighbors"][neighbor].keys():
                            ospf_neighbor_info["dr_ip"] = ospf_neighbors[vrf]["address_family"]["ipv4"]["instance"][process]["area"][area]["interfaces"][interface]["neighbors"][neighbor]["dr_ip_addr"]
                        else:
                            ospf_neighbor_info["dr_ip"] = "n/a"
                        if "bdr_ip_addr" in ospf_neighbors[vrf]["address_family"]["ipv4"]["instance"][process]["area"][area]["interfaces"][interface]["neighbors"][neighbor].keys():
                            ospf_neighbor_info["bdr_ip"] = ospf_neighbors[vrf]["address_family"]["ipv4"]["instance"][process]["areas"][area]["interfaces"][interface]["neighbors"][neighbor]["bdr_ip_addr"]
                        else:
                            ospf_neighbor_info["bdr_ip"] = "n/a"
                        if "dead_time" in ospf_neighbors[vrf]["address_family"]["ipv4"]["instance"][process]["areas"][area]["interfaces"][interface]["neighbors"][neighbor].keys():
                            ospf_neighbor_info["dead_time"] = ospf_neighbors[interface]["neighbors"][neighbor]["dead_time"]
                        else:
                            ospf_neighbor_info["dead_time"] = "n/a"
                        ospf_neighbor_list.append(ospf_neighbor_info)

    return ospf_neighbor_list

def run_nxos_commands(nxos_devices):
    """
    Connect to Nexus devices and run the commands show interface, 
    show ip ospf neighbors detail, show processes memory, and show 
    processes cpu. Add the results of running the commands to a 
    dictionary.
    :return: dictionary containing lists with the parsed results of 
    running the commands on each device
    """
    nxos_info = {
        "interfaces": [],
        "cpu_processes": [],
        "memory_processes": [],
        "ospf_neighbors": []
    }
    for device in nxos_devices:
        node = nxos_devices[device]
        ip_addr = node.connections["cli"]["ip"]
        device_info = {"name": device, "ip": ip_addr}
        node.connect(init_exec_commands=[], init_config_commands=[],
                       log_stdout=False, learn_hostname=True)
        try:
            show_interface = node.parse("show interface")
        except Exception as e:
            print(f"There was an issue getting the interfaces for {device}")
            print(e)
            show_interface = {}
        try:
            show_ospf_neighbor = node.parse("show ip ospf neighbors detail")
        except Exception as e:
            print(f"There was an issue getting the ospf neighbor information for {device}")
            print(e)
            show_ospf_neighbor = {}
        try:
            show_memory = node.parse("show processes memory")
        except Exception as e:
            print(f"There was an issue getting the memory information for {device}")
            print(e)
            show_memory = {}
        try:
            show_cpu = node.parse("show processes cpu")
        except Exception as e:
            print(f"There was an issue getting the cpu processes for {device}")
            print(e)
            show_cpu = {}
        node.disconnect()

        if show_cpu:
            cpu_processes = show_cpu["index"]
        else:
            cpu_processes = {}
        if show_memory:
            memory_processes = show_memory["pid"]
        else:
            memory_processes = {}
        if show_ospf_neighbor:
            ospf_neighbors = show_ospf_neighbor["vrf"]
        else:
            ospf_neighbors = {}

        if show_interface:
            nxos_info["interfaces"].extend(parse_interfaces(show_interface, device_info))
        if cpu_processes:
            nxos_info["cpu_processes"].extend(parse_cpu_process(cpu_processes, device_info))
        if memory_processes:
            nxos_info["memory_processes"].extend(parse_nx_memory_process(memory_processes, device_info))
        if ospf_neighbors:
            nxos_info["ospf_neighbors"].extend(parse_ospf_neighbor(ospf_neighbors, device_info))

    return nxos_info

def run_ios_commands(ios_devices):
    """
    Connect to IOS devices and run the commands show interfaces, 
    show ip ospf neighbor, show processes memory, and show 
    processes cpu. Add the results of running the commands to a 
    dictionary.
    :return: dictionary containing lists with the parsed results of 
    running the commands on each device
    """
    ios_info = {
        "interfaces": [],
        "cpu_processes": [],
        "memory_processes": [],
        "ospf_neighbors": []
    }
    for device in ios_devices:
        node = ios_devices[device]
        ip_addr = node.connections["cli"]["ip"]
        device_info = {"name": device, "ip": ip_addr}
        node.connect(init_exec_commands=[], init_config_commands=[],
                       log_stdout=False, learn_hostname=True)
        try:
            show_interface = node.parse("show interfaces")
        except Exception as e:
            print(f"There was an issue getting the interfaces for {device}")
            print(e)
            show_interface = {}
        try:
            show_ospf_neighbor = node.parse("show ip ospf neighbor")
        except Exception as e:
            print(f"There was an issue getting the ospf neighbor information for {device}")
            print(e)
            show_ospf_neighbor = {}
        try:
            show_memory = node.parse("show processes memory")
        except Exception as e:
            print(f"There was an issue getting the memory information for {device}")
            print(e)
            show_memory = {}
        try:
            show_cpu = node.parse("show processes cpu")
        except Exception as e:
            print(f"There was an issue getting the cpu processes for {device}")
            print(e)
            show_cpu = {}
        node.disconnect()

        if show_cpu:
            cpu_processes = show_cpu["index"]
        else:
            cpu_processes = {}
        if show_memory:
            memory_processes = show_memory["pid"]
        else:
            memory_processes = {}
        if show_ospf_neighbor:
            ospf_neighbors = show_ospf_neighbor["vrf"]
        else:
            ospf_neighbors = {}

        if show_interface:
            ios_info["interfaces"].extend(parse_interfaces(show_interface, device_info))
        if cpu_processes:
            ios_info["cpu_processes"].extend(parse_cpu_process(cpu_processes, device_info))
        if memory_processes:
            ios_info["memory_processes"].extend(parse_memory_process(memory_processes, device_info))
        if ospf_neighbors:
            ios_info["ospf_neighbors"].extend(parse_ospf_neighbor(ospf_neighbors, device_info))

    return ios_info

def main(argv):
    # retrieve the devices we will connect to from the network testbed YAML file
    testbed_list = testbed.load(f"./network_testbed.yml")
    devices = testbed_list.devices

    nxos_devices = {}
    ios_devices = {}

    # separate the IOS devices from the Nexus devices
    for device in devices:
        node = devices[device]
        if node.os == "nxos":
            nxos_devices[device] = node
        elif node.os == "ios" or node.os == "iosxe":
            ios_devices[device] = node

    # run and parse the results of the commands on the devices
    if nxos_devices != {}:
        # the Nexus commands are slightly different from the IOS devices
        nxos_info = run_nxos_commands(nxos_devices)
    else:
        nxos_info = {}

    if ios_devices != {}:
        ios_info = run_ios_commands(ios_devices)
    else:
        ios_info = {}

    # create an Excel file with sheets for each of the IOS and Nexus commands
    # highlight the cells of the interfaces sheets that represent shutdown interfaces in red
    with pd.ExcelWriter("network_analytics.xlsx") as writer:
        workbook = writer.book
        if nxos_info:
            nxos_interface_df = pd.DataFrame.from_dict(nxos_info["interfaces"])
            nxos_cpu_df = pd.DataFrame.from_dict(nxos_info["cpu_processes"])
            nxos_memory_df = pd.DataFrame.from_dict(nxos_info["memory_processes"])
            nxos_ospf_df = pd.DataFrame.from_dict(nxos_info["ospf_neighbors"])

            nxos_interface_df.to_excel(writer, sheet_name="NXOS Interfaces")
            nxos_cpu_df.to_excel(writer, sheet_name="NXOS CPU Processes")
            nxos_memory_df.to_excel(writer, sheet_name="NXOS Memory Processes")
            nxos_ospf_df.to_excel(writer, sheet_name="NXOS OSPF Neighbors")

            nxos_interfaces_sheet = workbook.get_worksheet_by_name("NXOS Interfaces")
            error_format = workbook.add_format({"bg_color": "red"})
            interface_len = len(nxos_info["interfaces"])
            cell_range = "E1:E" + str(interface_len)
            nxos_interfaces_sheet.conditional_format(cell_range,
                                                     {"type": "text",
                                                      "criteria": "containing",
                                                      "value": "FALSE",
                                                      "format": error_format})



        if ios_info:
            ios_interface_df = pd.DataFrame.from_dict(ios_info["interfaces"])
            ios_cpu_df = pd.DataFrame.from_dict(ios_info["cpu_processes"])
            ios_memory_df = pd.DataFrame.from_dict(ios_info["memory_processes"])
            ios_ospf_df = pd.DataFrame.from_dict(ios_info["ospf_neighbors"])

            ios_interface_df.to_excel(writer, sheet_name="IOS Interfaces")
            ios_cpu_df.to_excel(writer, sheet_name="IOS CPU Processes")
            ios_memory_df.to_excel(writer, sheet_name="IOS Memory Processes")
            ios_ospf_df.to_excel(writer, sheet_name="IOS OSPF Neighbors")

            ios_interfaces_sheet = workbook.get_worksheet_by_name("IOS Interfaces")
            error_format = workbook.add_format({"bg_color": "red"})
            interface_len = len(ios_info["interfaces"])
            cell_range = "E1:E" + str(interface_len)
            ios_interfaces_sheet.conditional_format(cell_range,
                                                     {"type": "text",
                                                      "criteria": "containing",
                                                      "value": "FALSE",
                                                      "format": error_format})



if __name__ == "__main__":
    sys.exit(main(sys.argv))