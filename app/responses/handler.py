
from typing import Type, Union, List, Optional
from sqlalchemy.orm import declarative_base, DeclarativeMeta
from pydantic import ValidationError
from responses.models import Response, MetaData
from database import Base
from exceptions.models import CustomError


def create_response(message: str,
                    result: Union[Base, List[Base], dict, List[dict], None], 
                    pydantic_model: Optional[Type[declarative_base]] = None,
                    meta_data: Optional[MetaData] = None
                    ) -> Response:
    if not result:
        return Response(message=message, data=result, meta_data=meta_data)

    result_dict = None  # Placeholder

    if isinstance(result, list):
        # Check if list contains ORM objects
        if all(isinstance(item, Base) for item in result):
            result_dict = [{key: value for key, value in item.__dict__.items() if key != '_sa_instance_state'} for item in result]
        else:
            result_dict = result  # Assume already in dictionary format
    elif isinstance(result, Base):
        result_dict = {key: value for key, value in result.__dict__.items() if key != '_sa_instance_state'}
    else:
        result_dict = result  # Assume it's a valid dict

    try:
        if isinstance(result_dict, list):
            # Convert list of dictionaries to list of Pydantic models
            result_response = [pydantic_model(**item) for item in result_dict]
        else:
            # Convert single dictionary to Pydantic model
            result_response = pydantic_model(**result_dict)
    except ValidationError as e:
        raise CustomError(message= "internal server error:ValidationError", status_code=500)
    except TypeError as e:
        raise CustomError(message= "internal server error:TypeError", status_code=500)
    return Response(message=message, data=result_response, meta_data=meta_data)


