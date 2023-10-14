from pydantic import BaseModel


def to_camel(text: str) -> str:
    """
    Convert string to camelCase.

    :param text: text for change
    :return: camelCase convention of text
    """
    result = ""
    capitalize_next = False
    for char in text:
        if char == "_":
            capitalize_next = True
        else:
            if capitalize_next:
                result += char.upper()
                capitalize_next = False
            else:
                result += char
    return result


class CamelModel(BaseModel):
    """
    BaseModel for API with camel-case aliases and support for population by field name.

    Configurations:
        - alias_generator: Specifies the alias generator used for converting field
        - allow_population_by_field_name: Indicates whether to allow population of model

    """

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
