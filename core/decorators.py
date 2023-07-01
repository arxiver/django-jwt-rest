from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

def swagger(method, operation_description, response_schema, body_schema=None, operation_summary=None):
    return swagger_auto_schema(
      method=method,
      request_body=body_schema,
      operation_description=operation_description,
      operation_summary=operation_summary,
      responses={
          200: openapi.Response(
              description='Get',
              schema=response_schema
          ),
          400: openapi.Response(
              description='Bad request',
              schema=openapi.Schema(
                  type=openapi.TYPE_OBJECT,
                  properties={
                      'error': openapi.Schema(type=openapi.TYPE_STRING)
                  }
              )
          ),
      }
  )
