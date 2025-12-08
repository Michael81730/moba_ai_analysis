from .validator import Validator

class UsernameValidator(Validator):
    name = "username"

    def validate(value):
        # validate username

        return True