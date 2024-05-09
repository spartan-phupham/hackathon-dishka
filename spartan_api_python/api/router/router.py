from fastapi.routing import APIRouter
from sqlalchemy import create_engine

from spartan_api_python.api.router.bot import BotRouter
from spartan_api_python.api.router.echo import EchoRouter
from spartan_api_python.api.router.health import HealthRouter
from spartan_api_python.api.router.user import UserRouter
from spartan_api_python.db.user.repository import UserRepository
from spartan_api_python.service.ai.config import PipelineConfig
from spartan_api_python.service.ai.langchain import LangchainManager
from spartan_api_python.service.ai.memory import PineconeLangchainMemory

config = PipelineConfig()

langchain_memory = PineconeLangchainMemory(
    pinecone_config=config.pinecone,
    openai_config=config.open_ai
)

langchain_manager = LangchainManager(
    config=config.open_ai,
    memory=langchain_memory
)

engine = create_engine("postgresql://local:local@localhost:5432/local")
user_repository = UserRepository(engine)
api_router = APIRouter()
echo_router = EchoRouter(APIRouter())
health_router = HealthRouter(APIRouter())
user_router = UserRouter(APIRouter(), user_repository)
bot_router = BotRouter(APIRouter(), langchain_memory, langchain_manager)

print("server started...\n")

# register all routers
api_router.include_router(health_router.router, prefix="/health", tags=["health"])
api_router.include_router(echo_router.router, prefix="/echo", tags=["echo"])
api_router.include_router(bot_router.router, prefix="/bot", tags=["bot"])
api_router.include_router(user_router.router, prefix="/user", tags=["user"])
