from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken


class L2RefreshToken(RefreshToken):
    """
    A wrapper of `RefreshToken` and implements additional
    revocation policies
    """

    def check_blacklist(self) -> None:

        """
        Checks if this token is present in the token blacklist.
        if present, add all outstanding token associated with the
        user to the blacklist and Raise `TokenError`. -- attempting
        to use a blacklisted token is flagged as suspicious activity
        """
        try:
            super().check_blacklist()
        except TokenError:
            user_jwts = OutstandingToken.objects.filter(user_id=self.payload[api_settings.USER_ID_CLAIM])
            BlacklistedToken.objects.bulk_create(
                [BlacklistedToken(token=token) for token in user_jwts], ignore_conflicts=True
            )
            print(f'{len(user_jwts)} sessions of user <id:{self.payload[api_settings.USER_ID_CLAIM]}> '
                  f' automatically terminated by system,')
            raise TokenError(f'Token blacklisted; {len(user_jwts)} sessions canceled for suspicious activity.'
)


