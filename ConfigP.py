"""
example script how to extract parameters from a Cisco IOS configuration using ciscoconfparse
"""
import json
from ciscoconfparse import CiscoConfParse
from ciscoconfparse.ccp_util import IPv4Obj
import sys, os
import collections
import json, pyaml
import yaml
import xlrd
import string
import fileinput
from jinja2 import Environment, FileSystemLoader
import yaml
 
if __name__ == "__main__":
    # the result dictionary
    result = {
        "features": [],
        "interfaces": {}
    }
 
    parse = CiscoConfParse("./sample.conf")
 
    interface_cmds = parse.find_objects(r"^interface ")
 
    # iterate over the resulting IOSCfgLine objects
    for interface_cmd in interface_cmds:
        # get the interface name (remove the interface command from the configuration line)
        intf_name = interface_cmd.text[len("interface "):]
        #print(intf_name)
        result["interfaces"][intf_name] = {}
        #print(result)
 
        # search for the description command, if not set use "not set" as value
        result["interfaces"][intf_name]["description"] = "not set"
        for cmd in interface_cmd.re_search_children(r"^ description "):
            result["interfaces"][intf_name]["description"] = cmd.text.strip()[len("description "):]
 
        result["interfaces"][intf_name]["qos-profile"] = "n/a"
        for cmd in interface_cmd.re_search_children(r"^ qos-profile "):
            result["interfaces"][intf_name]["qos-profile"] = cmd.text.strip()[len("qos-profile"):]
        result["interfaces"][intf_name]["vlan-type"] = "n/a"
        for cmd in interface_cmd.re_search_children(r"^ vlan-type "):
            result["interfaces"][intf_name]["vlan-type"]  = cmd.text.strip()[len("vlan-type"):]
 
        IPv4_REGEX = r"ip\saddress\s(\S+\s+\S+)"
 
        for cmd in interface_cmd.re_search_children(IPv4_REGEX):
            # ciscoconfparse provides a helper function for this task
            ipv4_addr = interface_cmd.re_match_iter_typed(IPv4_REGEX, result_type=IPv4Obj)
 
            result["interfaces"][intf_name].update({
                  "address": ipv4_addr.ip.exploded,
                  "netmask": ipv4_addr.netmask.exploded,
                  "network": ipv4_addr.network.exploded
            })
 
    #print("\nEXTRACTED PARAMETERS\n")
    #print(json.dumps(result, indent=4))
    json_data = json.dumps(result, indent=4)
    
    print(json_data)
#single call api 
#creating yaml file for Jinja
    yaml_data = yaml.dump(yaml.load(json_data))

    print(yaml_data)


    f = open("yamlout.yml", "w")
    f.write(yaml_data)
    f.close()
#updating port mapping in yaml
d = {}
wb = xlrd.open_workbook('port_mapping.xlsx')
sh = wb.sheet_by_index(0)  
for i in range(3):
    cell_value_class = sh.cell(i,0).value
    cell_value_id = sh.cell(i,1).value
    d[cell_value_class] = cell_value_id




text = "yamlout.yml"


for line in fileinput.input(text, inplace=True):
    line = line.rstrip()
    if not line:
        continue
    for f_key, f_value in d.items():
        if f_key in line:
            line = line.replace(f_key, f_value)
    print(line)


#Converting config


 
