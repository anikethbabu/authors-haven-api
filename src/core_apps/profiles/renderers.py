import json
from rest_framework.renderers import JSONRenderer


class ProfileJSONRenderer(JSONRenderer):
    """Renderer which serializes profile to JSON"""

    charset = "utf-8"

    def render(self, data, accepted_media_type=None, render_context=None):
        """Renders data into JSON, returning a bytestring. If an error returns JSON formatted string"""
        status_code = render_context["response"].status_code
        errors = data.get("errors", None)

        if errors is not None:
            return super(ProfileJSONRenderer, self).render(data)
        return json.dumps({"status_code": status_code, "profile": data})


class ProfilesJSONRenderer(JSONRenderer):
    """Renderer which serializes profiles JSON"""

    charset = "utf-8"

    def render(self, data, accepted_media_type=None, render_context=None):
        """Renders data into JSON, returning a bytestring. If an error, returns JSON formatted string"""
        status_code = render_context["response"].status_code
        errors = data.get("errors", None)

        if errors is not None:
            return super(ProfilesJSONRenderer, self).render(data)
        return json.dumps({"status_code": status_code, "profiles": data})
