from jinja2 import Environment, FileSystemLoader
import yaml

def main():
    #Load data from YAML file into Python dictionary
    config = yaml.load(open('./yamlout.yml'))

    #Load Jinja2 template
    env = Environment(loader = FileSystemLoader('./'), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('template.txt')

    #Render template using data and print the output
    Target_Config = template.render(config)

    print(type(Target_Config))

    file1 = open("Target.conf", "w") 
    file1.write(Target_Config)
    file1.close() 
    return
