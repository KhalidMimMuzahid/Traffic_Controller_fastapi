import enum

def model_to_dict(model):
    """Convert a SQLAlchemy model instance to a dictionary."""
    if model is None:
        return None

    model_dict = {**model.__dict__}
    model_dict.pop("_sa_instance_state", None)  # Remove SQLAlchemy internal attribute

    # Convert Enum fields to their values
    for key, value in model_dict.items():
        if isinstance(value, enum.Enum):
            model_dict[key] = value.value  # Convert Enum to string

    return model_dict
