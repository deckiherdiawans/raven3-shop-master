import json

class Config(object):
    
    @staticmethod
    def get():
        FILENAME = 'config.rvt'
        config = None

        with open(FILENAME, 'r') as f:
            config = json.load(f)

        return config
        

        