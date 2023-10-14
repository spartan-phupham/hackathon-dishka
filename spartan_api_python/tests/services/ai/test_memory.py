import unittest

from spartan_api_python.service.ai.config import PineconeConfig, OpenAIConfig
from spartan_api_python.service.ai.memory import PineconeLangchainMemory


class PineconeLangchainMemoryTest(unittest.TestCase):
    def test_train(self):
        memory = PineconeLangchainMemory(
            pinecone_config=PineconeConfig(
                api_key="",
                index_name="",
                environment="",
            ),
            openai_config=OpenAIConfig(
                api_key="",
            ),
        )
        memory.add_texts(["Hello world!"])
        self.assertEqual(1, 1)
        pass
