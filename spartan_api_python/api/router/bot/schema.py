from pydantic import validator

from spartan_api_python.core.schema_api_base import CamelModel


class BotQuestionRequest(CamelModel):
    """Input model for a question."""

    question: str


class BotTrainRequest(CamelModel):
    """Input model for a question."""

    input_text: str


class BotQuestionResponse(CamelModel):
    """Output model for an answer."""

    output_text: str


class BotChatResponse(CamelModel):
    """Chat response schema."""

    sender: str
    message: str

    @classmethod
    @validator("sender")
    def sender_must_be_bot_or_you(cls, value: str) -> str:
        """
        Validate the sender value.

        This method is a validator for the "sender" field of a message. It ensures
        that the provided sender value is either "bot" or "you".

        :param value: The sender value to validate.
        :type value: str
        :return: The validated sender value.
        :rtype: str
        :raises ValueError: If the provided sender value is not "bot" or "you".

        """
        valid_senders = ["bot", "you"]
        if value not in valid_senders:
            raise ValueError("sender must be bot or you")
        return value

    type: str

    @classmethod
    @validator("type")
    def validate_message_type(cls, value: str) -> str:
        """
        Validate the message type.

        This method is a validator for the "type" field of a message. It ensures that
        the provided message type is one of the valid values: "start", "stream",
        "end", "error", or "info".

        :param value: The message type to validate.
        :type value: str
        :return: The validated message type.
        :rtype: str
        :raises ValueError: If the provided message type is not one of the valid values.

        """
        valid_senders = ["start", "stream", "end", "error", "info"]
        if value not in valid_senders:
            raise ValueError("type must be start, stream or end")
        return value
