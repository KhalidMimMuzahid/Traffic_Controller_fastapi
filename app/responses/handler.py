
from typing import Type
from sqlalchemy.orm import declarative_base, DeclarativeMeta
from pydantic import ValidationError
from responses.models import Response
from database import Base

def create_response(result, pydantic_model: Type[declarative_base], message: str) -> Response:

    result_dict= {}
    # print("type___________________________________________________  _____________\n", type( result))
    # # Convert ORM model to dictionary and exclude internal state
    # result_dict = {key: value for key, value in result.__dict__.items() if key != '_sa_instance_state'}
    if isinstance(result, Base):
         # Convert ORM model to dictionary and exclude internal state
        # print("inside converting________________________________________________________________")
        result_dict = {key: value for key, value in result.__dict__.items() if key != '_sa_instance_state'}
    else:
        result_dict= result
    
    try:
        # Convert dictionary to Pydantic model (using the passed pydantic_model)
        result_response = pydantic_model(**result_dict)
    except ValidationError as e:
        # Print the detailed validation errors
        raise e  # Reraise to catch error at a higher level

    # Return the formatted Response object
    return Response(message=message, data=result_response)