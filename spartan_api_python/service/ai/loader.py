from langchain.document_loaders import DirectoryLoader
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter


class DataLoader:
    @staticmethod
    def load_documents(
        path: str,
        file_type: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> list[Document]:
        """
        Load and split documents from a directory.

        :param chunk_size: The maximum size of your chunks
        :param chunk_overlap: The maximum overlap between chunks
        :param path: Directory path.
        :param file_type: File type to filter documents.
        :return: List of Document objects.
        """
        loader = DirectoryLoader(path, glob=f"**/*.{file_type}")
        documents = loader.load()

        text_splitter = CharacterTextSplitter().from_tiktoken_encoder(
            encoding_name="cl100k_base",
            model_name="text-embedding-ada-002",
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        return text_splitter.split_documents(documents)

    @staticmethod
    def load_texts(
        texts: str,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> list[str]:
        """
        Load and split documents from a directory.

        :param texts: The text for train
        :param chunk_size: The maximum size of your chunks
        :param chunk_overlap: The maximum overlap between chunks
        :return: List of Document objects.
        """
        text_splitter = CharacterTextSplitter().from_tiktoken_encoder(
            encoding_name="cl100k_base",
            model_name="text-embedding-ada-002",
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        return text_splitter.split_text(texts)
