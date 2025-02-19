
from typing import Type
from sqlalchemy.orm import declarative_base
from pydantic import ValidationError
from responses.models import Response

def create_response(result, pydantic_model: Type[declarative_base], message: str) -> Response:


    # Convert ORM model to dictionary and exclude internal state
    result_dict = {key: value for key, value in result.__dict__.items() if key != '_sa_instance_state'}
    
    try:
        # Convert dictionary to Pydantic model (using the passed pydantic_model)
        result_response = pydantic_model(**result_dict)
    except ValidationError as e:
        # Print the detailed validation errors
        raise e  # Reraise to catch error at a higher level

    # Return the formatted Response object
    return Response(message=message, data=result_response)