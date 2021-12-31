import yaml

class confParser:
    def parseConfig(self):
        try:
            with open('conf.yml', 'r') as configFile:
                config = yaml.safe_load(configFile)
        except:
            return {'ok': False, 'reason': 'Failed to parse config'}

        if ('user_id' in config) and ('bearer_token' in config):
            return {'ok': True, 'config': config}
        else:
            return {'ok': False, 'reason': 'Failed to find required args in config'}
        
