import json 

CONFIG_FILE = "config.json"

class Configuration:
    def __init__(self, api_key: str, source_groups: list[str], destination_groups: list[str]): 
        self.api_key = api_key 
        self.source_groups = source_groups
        self.destination_groups = destination_groups 

    def __str__(self): 
        return f"Configuration(api_key='{self.api_key}', source_groups={self.source_groups}, destination_groups={self.destination_groups})"
    
def get_config_file() -> Configuration: 
    '''
    This function reads the configuration file `config.json`

    `config.json` is expected to be in the following format: 

    { 
        "api_key": "API-KEY-FROM-BOT-FATHER-GOES-HERE", 
        "source_groups": [
            "source group ids 1",
            "source group ids 2"
        ], 
        "destination_groups": [ 
            "destination group ids 3"
        ]
    }

    '''
    with open(CONFIG_FILE, 'r') as f: 
        data = f.read() 
        config = json.loads(data)
        config = Configuration(
            api_key=config['api_key'], 
            source_groups=config['source_groups'], 
            destination_groups=config['destination_groups']
        )
        # print(config, type(config)) 
    return config 



if __name__ == '__main__': 
    print(get_config_file())   