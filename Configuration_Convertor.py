import config_parse
import convert_config

start_message = """         Configuration Converter v0.1
-------------------------------------------------
The script can parse the IOS configs and convert it into an YAML file 
before producing the final output. The YAML file can be edited to 
add/modify values read from the source config. The edited YAML file 
will be used to generate the final output using the jinja template.
-------------------------------------------------
"""

choice = """Choose from following option
1 : To parse the config and generate an YAML file
2 : To produce target device configurations
0 : To exit
"""

print(start_message)
user_entry = ""
while (1):
    print("\n" + choice + "\n")
    user_entry = input()
    if user_entry == 1:
        # Parse input configuration files
        config_parse.main()
    elif user_entry == 2:
        # Create configuration file for new device (only if, yaml output from config_parse and jinja template are both ready)
        convert_config.main()
    elif user_entry == 0:
        break
    else:
        print("Invalid input")
