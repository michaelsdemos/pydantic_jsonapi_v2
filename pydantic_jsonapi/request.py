from typing import Generic, TypeVar, Optional, Any, Type
from typing_extensions import Literal

from pydantic import BaseModel, UUID4

from pydantic_jsonapi.relationships import RequestRelationshipsType


TypeT = TypeVar("TypeT")
AttributesT = TypeVar("AttributesT")


class RequestDataModel(BaseModel, Generic[TypeT, AttributesT]):
    """ """

    type: TypeT
    attributes: AttributesT
    id: Optional[str] = None
    relationships: Optional[RequestRelationshipsType] = None


DataT = TypeVar("DataT", bound=RequestDataModel)


class RequestModel(BaseModel, Generic[DataT]):
    """ """

    data: DataT

    def attributes(self):
        return self.data.attributes


def JsonApiRequest(type_string: str, attributes_model: Any) -> Type[RequestModel]:
    request_data_model = RequestDataModel[
        Literal[type_string],
        attributes_model,
    ]
    request_data_model.__name__ = f"RequestData[{type_string}]"
    request_model = RequestModel[request_data_model]
    request_model.__name__ = f"Request[{type_string}]"
    return request_model
