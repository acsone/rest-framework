# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from starlette.middleware.errors import ServerErrorMiddleware
from starlette.responses import JSONResponse

from fastapi import Request

# we need to monkey patch the ServerErrorMiddleware to ensure that all the
# exceptions that are not handled by the specific handlers are handled by
# the odoo handler chain
original_error_response_method = ServerErrorMiddleware.error_response


def error_response(self, request: Request, exc: Exception) -> JSONResponse:
    # let all the exceptions bubble up to the retrying mechanism and the
    # dispatcher error handler to ensure that appropriate action are taken
    # regarding the transaction, environment, and registry
    raise exc


ServerErrorMiddleware.error_response = error_response
