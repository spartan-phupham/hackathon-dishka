from langchain import OpenAI, PromptTemplate
from langchain.callbacks.manager import AsyncCallbackManager
from langchain.chains.chat_vector_db.prompts import QA_PROMPT
from langchain.chains.conversational_retrieval.base import BaseConversationalRetrievalChain, ConversationalRetrievalChain
from langchain.chains.question_answering import load_qa_chain
from langchain.schema import Document
from starlette.websockets import WebSocket

from spartan_api_python.service.ai.callback import QuestionGenCallbackHandler, StreamingLLMCallbackHandler
from spartan_api_python.service.ai.config import OpenAIConfig
from spartan_api_python.service.ai.memory import LangchainMemory


class LangchainManager:

    def __init__(self, config: OpenAIConfig, memory: LangchainMemory):
        self.openai_api_key = config.api_key
        self.memory = memory

    def conversation(self, websocket: WebSocket) -> BaseConversationalRetrievalChain:
        question_handler = QuestionGenCallbackHandler(websocket)
        stream_handler = StreamingLLMCallbackHandler(websocket)
        """
        Create a ChatVectorDBChain for question/answering.

        :param question_handler: Handler class of question after search output.
        :param stream_handler: Handler class of stream after receive output.
        :return: A ConversationalRetrievalChain object
        """
        manager = AsyncCallbackManager([])
        question_manager = AsyncCallbackManager([question_handler])
        stream_manager = AsyncCallbackManager([stream_handler])

        question_gen_llm = ChatOpenAI(  # type: ignore
            openai_api_key=self.openai_api_key,
            temperature=0,
            verbose=True,
            callback_manager=question_manager,
        )
        streaming_llm = ChatOpenAI(  # type: ignore
            openai_api_key=self.openai_api_key,
            streaming=True,
            callback_manager=stream_manager,
            verbose=True,
            temperature=0,
        )

        return ConversationalRetrievalChain.from_llm(
            llm=streaming_llm,
            verbose=True,
            condense_question_llm=question_gen_llm,
            retriever=self.memory.get_vector_store().as_retriever(),
            memory=self.memory.get_memory(),
            callback_manager=manager,
            combine_docs_chain_kwargs={
                "prompt": QA_PROMPT,
            },
        )

    async def ask(self, query: str, num_results: int = 5) -> str:
        """
        Search for similar documents in the Pinecone index.

        :param query: Query string for similarity search.
        :param num_results: Number of results to retrieve (default: 5).
        :return: Dictionary containing the generated text for each document.
        """
        docsearch = self.memory.get_vector_store()
        docs = docsearch.similarity_search(query, k=num_results)
        return await self._generate_text(docs, query)

    async def _generate_text(self, docs: list[Document], query: str) -> str:
        # Generate text using OpenAI's API
        prompt = self.prompt_template()
        chain = load_qa_chain(
            OpenAI(
                temperature=0,
                openai_api_key=self.openai_api_key,
                model_name="text-davinci-003",  # type: ignore
            ),
            chain_type="stuff",
            prompt=prompt,
        )
        return await chain.arun(question=query, input_documents=docs)

    @staticmethod
    def prompt_template(is_chat: bool = False) -> PromptTemplate:
        if is_chat:
            prompt_template = """The following is a friendly conversation between a
            human and an AI. The AI is talkative and provides lots of specific
            details from its context. If the AI does not know the answer to a
            question, it truthfully says it does not know.

            Relevant pieces of previous conversation:
            {history}

            (You do not need to use these pieces of information if not relevant)

            Current conversation:
            Human: {input}
            AI:"""
            input_variables = ["history", "input"]
        else:
            prompt_template = """Use the following pieces of context to answer the
            question at the end. If you don't know the answer, just say that you don't
            know, don't try to make up an answer.

                {context}

                Question: {question}
                Answer in English:
            """
            input_variables = ["context", "question"]
        return PromptTemplate(
            template=prompt_template,
            input_variables=input_variables,
        )
