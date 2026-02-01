from .validator import Validator

class UsernameValidator(Validator):
    name = "username"

    def validate(self, value):
        # validate username length
        if not (6 <= len(value) <= 18): 
            return False

        # validate username only includes letter, numbers, underscore
        if not value.isalnum():
            return False
        
        return True