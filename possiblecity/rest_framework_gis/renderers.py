# rest_framework_gis/renderers.py

from rest_framework.renderers import BaseRenderer

class GeoJSONRenderer(BaseRenderer):
    """
    Renderer which serializes to json.
    """

    media_type = 'application/geo-json'
    format = 'json'
    encoder_class = encoders.JSONEncoder

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `obj` into json.
        """
        if data is None:
            return ''

        # If 'indent' is provided in the context, then pretty print the result.
        # E.g. If we're being called by the BrowseableAPIRenderer.
        renderer_context = renderer_context or {}
        indent = renderer_context.get('indent', None)

        if accepted_media_type:
            # If the media type looks like 'application/json; indent=4',
            # then pretty print the result.
            base_media_type, params = parse_header(accepted_media_type)
            indent = params.get('indent', indent)
            try:
                indent = max(min(int(indent), 8), 0)
            except (ValueError, TypeError):
                indent = None

        return json.dumps(data, cls=self.encoder_class, indent=indent)