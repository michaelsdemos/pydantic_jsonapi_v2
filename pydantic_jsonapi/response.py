from typing import Generic, TypeVar, Optional, List, Any, Type, get_type_hints
from typing_extensions import Literal

from pydantic_jsonapi.filter import filter_none
from pydantic_jsonapi.relationships import ResponseRelationshipsType
from pydantic_jsonapi.resource_links import ResourceLinks
from pydantic import BaseModel, ConfigDict


TypeT = TypeVar("TypeT", bound=str)
AttributesT = TypeVar("AttributesT")


class ResponseDataModel(BaseModel, Generic[TypeT, AttributesT]):
    """ """

    id: str
    type: TypeT
    attributes: AttributesT = {}
    relationships: Optional[ResponseRelationshipsType] = None
    links: Optional[ResourceLinks] = None
    model_config = ConfigDict(validate_default=True)


DataT = TypeVar("DataT", bound=ResponseDataModel)


class ResponseModel(BaseModel, Generic[DataT]):
    """ """

    data: DataT
    included: Optional[list] = None
    meta: Optional[dict] = None
    links: Optional[ResourceLinks] = None

    def dict(self, *, serlialize_none: bool = False, **kwargs):
        response = super().dict(**kwargs)
        if serlialize_none:
            return response
        return filter_none(response)

    @classmethod
    def resource_object(
        cls,
        *,
        id: str,
        attributes: Optional[dict] = None,
        relationships: Optional[dict] = None,
        links: Optional[dict] = None,
    ) -> ResponseDataModel:
        data_type = get_type_hints(cls)["data"]
        if getattr(data_type, "__origin__", None) is list:
            data_type = data_type.__args__[0]
        typename = get_type_hints(data_type)["type"].__args__[0]
        return data_type(
            id=id,
            type=typename,
            attributes=attributes or {},
            relationships=relationships,
            links=links,
        )


def JsonApiResponse(
    type_string: str, attributes_model: Any, *, use_list: bool = False
) -> Type[ResponseModel]:
    response_data_model = ResponseDataModel[
        Literal[type_string],
        attributes_model,
    ]
    if use_list:
        response_data_model = List[response_data_model]
        response_data_model.__name__ = f"ListResponseData[{type_string}]"
        response_model = ResponseModel[response_data_model]
        response_model.__name__ = f"ListResponse[{type_string}]"
    else:
        response_data_model.__name__ = f"ResponseData[{type_string}]"
        response_model = ResponseModel[response_data_model]
        response_model.__name__ = f"Response[{type_string}]"
    return response_model
