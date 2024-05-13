from fastapi import HTTPException

NOT_FOUND = HTTPException(404, "Item not found")
KEY_EXISTS = HTTPException(422, "Key already exists")
