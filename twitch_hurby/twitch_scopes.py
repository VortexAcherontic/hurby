from utils import logger

scopes = {
    "analytics:read:extensions": False,
    "analytics:read:games": False,
    "bits:read": False,
    "channel:read:subscriptions": False,
    "clips:edit": False,
    "user:edit": False,
    "user:edit:broadcast": False,
    "user:read:broadcast": False,
    "user:read:email": False
}


class TwitchScopes:
    def __init__(self):
        self.scopes = scopes

    def get_url_scope_request(self, scope_request: list) -> str:
        scopes_string = ""
        for i in scope_request:
            scope_name = i
            if scope_name in scopes:
                scopes_string = scopes_string + scope_name + "+"
                self.scopes[scope_name] = True
                pass
            else:
                logger.log(logger.WARN, "Unsupported scope: " + scope_name)
        scopes_string = scopes_string[0:len(scopes_string)-1]
        return scopes_string

    def is_scope_requested(self, scope: str):
        if scope in self.scopes:
            return self.scopes[scope]
