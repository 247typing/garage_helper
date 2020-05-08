#this is only used for developemnt to create the proper structure of a yaml file
import yaml
conf = {"font" :
            {
            "BUTTON" : ("arial", 18),
            "DEFAULT_TOOL" : ("arial", 16),
            "TOOL_TITLE" : ("arial bold", 24)
            },
        "color":
            {
            "BACKGROUND" : "powder blue"
            }
        }

with open("config.yml", "w") as f:
    yaml.dump(conf, f, default_flow_style=False)
