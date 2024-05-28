from typing import Optional, List

from pydantic import BaseModel, ValidationError
from pydantic_jsonapi.filter import filter_none
from pydantic_jsonapi.resource_links import ResourceLinks


class ErrorSource(BaseModel):
    pointer: Optional[str] = None
    parameter: Optional[str] = None


class Error(BaseModel):
    """https://jsonapi.org/format/#error-objects"""
    id: Optional[str] = None
    links: Optional[ResourceLinks] = None
    status: Optional[str] = None
    code: Optional[str] = None
    title: Optional[str] = None
    detail: Optional[str] = None
    source: Optional[ErrorSource] = None
    meta: Optional[dict] = None


class ErrorResponse(BaseModel):
    errors: List[Error]

def transform_to_json_api_errors(validation_error: ValidationError) -> dict:
    def transform_error(error):
        return {
            'detail': error.get('msg'),
            'title': error.get('type'),
            'source': {
                'pointer': '/' + '/'.join(error['loc']),
            },
        }
    error_response = ErrorResponse(
        errors=[transform_error(error) for error in validation_error.errors()]
    )
    return filter_none(error_response.dict())
