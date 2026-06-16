from rest_framework.response import Response


def build_api_response_envelope(message, data=None):
    return {"message": message, "data": data}


# Standard api response shape.
def api_response(message, data=None, status=200):
    return Response(build_api_response_envelope(message, data), status=status)
