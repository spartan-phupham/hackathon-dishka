from fastapi.routing import APIRouter

from spartan_api_python.api.router.bot import BotRouter
from spartan_api_python.api.router.echo import EchoRouter
from spartan_api_python.api.router.health import HealthRouter
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

api_router = APIRouter()
echo_router = EchoRouter(APIRouter())
health_router = HealthRouter(APIRouter())

bot_router = BotRouter(APIRouter(), langchain_memory, langchain_manager)
api_router.include_router(health_router.router, prefix="/health", tags=["health"])
api_router.include_router(echo_router.router, prefix="/echo", tags=["echo"])
api_router.include_router(bot_router.router, prefix="/bot", tags=["bot"])
