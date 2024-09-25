from rest_framework.exceptions import ValidationError


class Validators:

    @staticmethod
    def validate_password(password):
        if password is None:
            raise ValidationError("Password is required.")

        if len(password) < 6:
            raise ValidationError("Password should be atleast 6 characters long.")
        if not any(char.isdigit() for char in password):
            raise ValidationError("Password should contain atleast one digit.")
        if not any(char in '!@#$%^&*()_+' for char in password):
            raise ValidationError("Password should contain atleast one special character.")
        return password
