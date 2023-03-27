from drf_spectacular.openapi import OpenApiAuthenticationExtension
from drf_spectacular.plumbing import build_bearer_security_scheme_object


class AuthenticationScheme(OpenApiAuthenticationExtension):
    """Change representation of authentication in Redoc/Swagger."""

    target_class = "dj_rest_auth.jwt_auth.JWTCookieAuthentication"
    name = "jwtAuth"
    priority = 2

    def get_security_definition(self, auto_schema):
        return build_bearer_security_scheme_object(
            header_name="Authorization",
            token_prefix="Bearer",
            bearer_format="JWT",
        )
