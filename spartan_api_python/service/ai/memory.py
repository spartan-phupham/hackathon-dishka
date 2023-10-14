from abc import ABCMeta, abstractmethod

import pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain.memory import VectorStoreRetrieverMemory, ConversationBufferWindowMemory
from langchain.schema import Document
from langchain.vectorstores import Pinecone, VectorStore

from spartan_api_python.service.ai.config import PineconeConfig, OpenAIConfig


class LangchainMemory(metaclass=ABCMeta):
    @abstractmethod
    def add_documents(self, documents: list[Document]) -> None:
        pass

    @abstractmethod
    def add_texts(self, texts: list[str]) -> None:
        pass

    @abstractmethod
    def get_vector_store(self) -> VectorStore:
        pass

    @abstractmethod
    def get_memory(self) -> VectorStoreRetrieverMemory | ConversationBufferWindowMemory:
        pass


class PineconeLangchainMemory(LangchainMemory):

    def __init__(self, pinecone_config: PineconeConfig, openai_config: OpenAIConfig):
        pinecone.init(**pinecone_config.dict)
        self.dimension = 1536
        self.pinecone_index_name = pinecone_config.index_name
        self.openai_api_key = openai_config.api_key

    def add_documents(self, documents: list[Document]) -> None:
        index_name = self._get_or_create_index()
        docsearch = self.get_vector_store()
        docsearch.add_documents(
            documents,
            index_name=index_name,
        )

    def add_texts(self, texts: list[str]) -> None:
        pass

    def get_memory(self, use_vector: bool = False) -> VectorStoreRetrieverMemory | ConversationBufferWindowMemory:
        memory_key = "chat_history"
        if use_vector:
            docsearch = self.get_vector_store()
            retriever = docsearch.as_retriever(search_kwargs={"k": 1})
            return VectorStoreRetrieverMemory(
                retriever=retriever,
                memory_key=memory_key,
            )
        return ConversationBufferWindowMemory(
            memory_key=memory_key,
            return_messages=True,
            output_key="answer",
            k=5,
        )

    def get_vector_store(self) -> Pinecone:
        """
        Get the Pinecone vector store for document search.

        :return: Pinecone vector store.
        """
        index_name = self._get_or_create_index()
        return Pinecone.from_existing_index(
            index_name=index_name,
            embedding=self._get_embeddings(),
        )

    def _get_or_create_index(self) -> str:
        # Create or connect to the Pinecone index
        if self.pinecone_index_name in pinecone.list_indexes():
            return self.pinecone_index_name

        pinecone.create_index(
            name=self.pinecone_index_name,
            dimension=self.dimension,
        )
        return self.pinecone_index_name

    def _get_embeddings(self) -> OpenAIEmbeddings:
        # Get embeddings for OpenAI
        return OpenAIEmbeddings(  # type: ignore
            openai_api_key=self.openai_api_key,
        )
