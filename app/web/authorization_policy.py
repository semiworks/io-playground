
import aiohttp_security


class AuthorizationPolicy(aiohttp_security.AbstractAuthorizationPolicy):

    def __init__(self):
        super().__init__()

    async def authorized_userid(self, identity):
        """Retrieve authorized user id.
        Return the user_id of the user identified by the identity
        or 'None' if no user exists related to the identity.
        """
        if identity == "bud":
            return "bud"

        return None

    async def permits(self, identity, permission, context=None):
        """Check user permissions.
        Return True if the identity is allowed the permission in the
        current context, else return False.
        """
        if identity != "bud":
            return False

        # TODO: check permissions

        return True
