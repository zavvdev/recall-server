# Python's standard logging module.
import logging

from rest_framework import status

# DRF's built-in exception classes. These are what DRF raises internally.
from rest_framework.exceptions import NotAuthenticated, NotFound, PermissionDenied, ValidationError
from rest_framework.response import Response

# DRF's default exception handler. We're not replacing it outright — we call it first,
# then reshape what it produces. This is the function DRF normally points EXCEPTION_HANDLER to.
from rest_framework.views import exception_handler as drf_exception_handler

from shared.messages import Messages
from shared.responses import build_api_response_envelope

# A logger scoped to this module's path (shared.exception_handler).
# Lets us trace where logged errors originated and configure logging per-module.
# It creates a logger scoped to the current module's name — here, shared.exception_handler
# so when something logs logger.exception(...), the output shows where it came from:
# ERROR shared.exception_handler Unhandled exception
# Traceback (most recent call last): ...
# __name__ is a built-in Python variable — every module has it, automatically set to
# that module's dotted path (shared.exception_handler). Passing it to getLogger() is
# the standard Python convention so each module gets its own named logger instead
# of everyone sharing one anonymous logger.
logger = logging.getLogger(__name__)

# A lookup table mapping DRF's internal error codes (the .code attribute on each ErrorDetail,
# to our own generic Messages keys. Leading underscore marks it as module-private — not meant
# to be imported elsewhere.
_CODE_TO_MESSAGE = {
    "required": Messages.REQUIRED,
    "blank": Messages.REQUIRED,
    "null": Messages.REQUIRED,
    "max_length": Messages.TOO_LONG,
    "min_length": Messages.TOO_SHORT,
    "invalid": Messages.INVALID,
}


# The function we registered in settings.py under REST_FRAMEWORK["EXCEPTION_HANDLER"].
# DRF calls this automatically whenever a view raises an exception — we never call it ourselves.
# exc is the exception instance; context is a dict with
# {"view": ..., "args": ..., "kwargs": ..., "request": ...},
# giving us access to the view/request if needed.
def custom_exception_handler(exc, context):
    # Delegates to DRF's default handler first. It knows how to convert recognized exceptions
    # (ValidationError, NotFound, etc) into a Response with the right status code and DRF's
    # default .data shape (e.g. {"detail": "..."} or field errors dict). For exceptions it
    # doesn't recognize (a raw KeyError, TypeError, anything not a DRF/Django exception),
    # it returns None.
    response = drf_exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, ValidationError):
            response.data = build_api_response_envelope(
                data=_normalize_validation_err(exc.detail),
                message=Messages.VALIDATION_ERROR,
            )
            return response

        response.data = build_api_response_envelope(message=_map_known_err_message(exc))
        return response

    # Reached only if drf_exception_handler returned None — meaning this is an exception
    # DRF has no idea how to handle (a bug, a DB error, anything unexpected).
    # logger.exception logs at ERROR level and automatically includes the traceback
    # (that's what distinguishes it from logger.error), so we can debug it later.
    # This would otherwise have propagated up and become Django's HTML 500 page.
    logger.exception("unhandled_exception", exc_info=exc)

    # Fallback error.
    return Response(
        build_api_response_envelope(message=Messages.UNEXPECTED_ERROR),
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


# exc.detail for a flat serializer is a dict of {field_name: [ErrorDetail, ...]}.
# This recurses into each field's value — written generically (recursing into dicts)
# so it also handles nested serializers, where a field's value could itself be a dict
# of sub-fields rather than a list of errors.
def _normalize_validation_err(detail):
    if isinstance(detail, dict):
        return {key: _normalize_validation_err(value) for key, value in detail.items()}
    if isinstance(detail, list):
        # For each field, DRF gives a list of ErrorDetail objects (a field can fail
        # multiple validators at once). We only want the first one, so index [0] and map
        # just that single error.
        return _map_error_code(detail[0])
    return _map_error_code(detail)


def _map_error_code(err):
    code = getattr(err, "code", None)
    return _CODE_TO_MESSAGE.get(code, Messages.INVALID)


def _map_known_err_message(exc):
    if isinstance(exc, NotAuthenticated):
        return Messages.NOT_AUTHENTICATED
    if isinstance(exc, PermissionDenied):
        return Messages.PERMISSION_DENIED
    if isinstance(exc, NotFound):
        return Messages.NOT_FOUND
    return Messages.UNEXPECTED_ERROR
