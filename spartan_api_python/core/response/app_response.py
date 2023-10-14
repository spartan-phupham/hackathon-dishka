from typing import Any, List, Union

from starlette.responses import JSONResponse

from spartan_api_python.core.schema_api_base import CamelModel


class AppResponseModel(CamelModel):
    """
    Model representing the structure of the application response.

    Attributes:
        result: The result of the response, can be a list, a single object or None.
        messages: Optional list of messages associated with the response.
        success: Boolean indicating the success status of the response.
    """

    result: Union[List[CamelModel], CamelModel, None] = None
    messages: Union[List[str], None] = None
    success: bool = True

    class Config(CamelModel.Config):
        smart_union = True


class AppResponse(JSONResponse):
    """
    Custom JSON response class for the application.

    Attributes:
        media_type: The media type of the response.
    """

    media_type = "application/json"

    def __init__(
        self,
        content: Union[AppResponseModel, Any] = None,
        status_code: int = 200,
        success: bool = True,
    ) -> None:
        """
        Initialize the AppResponse object.

        :param content: The content of the response.
        :param status_code: The HTTP status code of the response.
        :param success: Boolean indicating the success status of the response.
        """
        if isinstance(content, AppResponseModel):
            super().__init__(content.dict(exclude_none=True), status_code)
        else:
            content_resp = AppResponseModel()
            content_resp.success = success
            if success is False:
                if isinstance(content, str):
                    content_resp.messages = [content]
                else:
                    content_resp.messages = content
            else:
                content_resp.result = content
                content_resp.messages = ["Successfully"]
            super().__init__(content_resp.dict(by_alias=True), status_code)
