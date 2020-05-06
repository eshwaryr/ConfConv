import config_parse
import config_convert

# Parse input configuration files

config_parse

# Wait for user input whether to start the conversion code
print("Press Enter to start configuration conversion)
input()

# Create configuration file for new device (only if, yaml output from config_parse and jinja template are both ready)

config_convert
