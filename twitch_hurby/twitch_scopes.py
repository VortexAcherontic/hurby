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

    def get_url_scope_request(self, scope_request: list):
        url = ""
        for i in scope_request:
            scope_name = i
            if scope_name in scopes:
                url = url + scope_name + " "
                self.scopes[scope_name] = True
                pass
            else:
                logger.log(logger.WARN, "Unsupported scope: " + scope_name)
        return url.strip()

    def is_scope_requested(self, scope: str):
        if scope in self.scopes:
            return self.scopes[scope]
