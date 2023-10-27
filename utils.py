from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
import string


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
        }


class IsUpperPasswordValidator:
    """
    Validate that the password is not contain any 
    uppercase letter.
    """

    def validate(self, password, user=None):

        UPPERCASES = string.ascii_uppercase
        
        for char in password:
            if char in UPPERCASES:
                return
            
        raise ValidationError(
            "Your Password Must Contains At Least One Uppercase Letter.")


class IsPuncPasswordValidator:
    """
    Validate that the password is not contain any 
    punctuation.
    """

    def validate(self, password, user=None):

        PUNCTUATIONS = string.punctuation

        for char in password:
            if char in PUNCTUATIONS:
                return

        raise ValidationError(
            "Your Password Must Contains At Least One Punctuation.")
    