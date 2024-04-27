from rest_framework.authentication import TokenAuthentication


# by default, django token auth uses the "Token" keyword
# we need to create a new subclass to be able to use the "Bearer" keyword
class BearerAuthentication(TokenAuthentication):
    keyword = "Bearer"
