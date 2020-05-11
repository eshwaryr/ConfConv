#remove unwanted imports
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
import parse_features
 
 def main():
  # the result dictionary
    result = {
        "features": [],
        "interfaces": {}
    }
    parse = CiscoConfParse("./sample.conf")
				result = parse_features.parse_interfaces(parse,result)
				
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
				return

if __name__ == "__main__":
    main()
