from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from ..token import L2RefreshToken


class L2TokenRefreshSerializer(TokenRefreshSerializer):
    """
    A wrapper of `TokenRefreshSerializer` that replace that
    implements added security
    """

    token_class = L2RefreshToken
