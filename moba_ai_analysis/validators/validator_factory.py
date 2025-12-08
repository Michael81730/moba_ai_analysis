from .username_validator import UsernameValidator

class ValidatorFactory:
    @staticmethod
    def get_validator(name):
        match name:
            case "username":
                return UsernameValidator()