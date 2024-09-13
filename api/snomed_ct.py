class SnomedCt():

    def __init__(self) -> None:
        raise NotImplementedError

    def check_observation(self, observation: str):
        raise NotImplementedError

    def get_code_from_name(self, name: str):
        raise NotImplementedError

    def get_name_from_code(self, code: str):
        raise NotImplementedError

class SnomedCtAPI(SnomedCt):

    def __init__(self) -> None:
        pass

    def check_observation(self, observation: str):
        pass

    def get_code_from_name(self, name: str):
        pass

    def get_name_from_code(self, code: str):
        pass

class SnomedCtExample(SnomedCt):

    def __init__(self) -> None:
        self.conditions_map = {
            'Diabético': '44054006',
            'Hipertenso': '38341003'
        }
        self.observations_map = {
            'Gestante': '161713000'
        }
        self.reverse_conditions_map = {v: k for k, v in self.conditions_map.items()}
        self.reverse_observations_map = {v: k for k, v in self.observations_map.items()}

    def check_observation(self, observation: str) -> bool:
        if observation in self.observations_map:
            return True
        return False

    def get_code_from_name(self, name: str) -> str:
        if name in self.conditions_map:
            return self.conditions_map[name]
        
        if name in self.observations_map:
            return self.observations_map[name]
        
        return None
    
    def get_name_from_code(self, code: str) -> str:
        if code in self.reverse_conditions_map:
            return self.reverse_conditions_map[code]
        
        if code in self.reverse_observations_map:
            return self.reverse_observations_map[code]
        
        return None