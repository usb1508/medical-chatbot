
from dotenv import load_dotenv
import os
from pinecone import Pinecone
from src.helper import load_pdf_files, filter_to_minimal_docs, text_split, download_embeddings
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore


load_dotenv()  # take environment variables from .env.


PINECONE_API_KEY=os.environ.get("PINECONE_API_KEY")
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")
OPEN_AI_MODEL=os.environ.get("OPENAI_MODEL")


os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["OPENAI_MODEL"] = OPEN_AI_MODEL

extracted_docs = load_pdf_files("data/")
minimal_docs = filter_to_minimal_docs(extracted_docs)
text_cunks = text_split(minimal_docs)

embeddings = download_embeddings()
pinecone_api_key = PINECONE_API_KEY
pc = Pinecone(api_key=pinecone_api_key)


index_name = "medical-chatbot"



if not pc.has_index(index_name):
	pc.create_index(
		name=index_name,
		dimension=384,
		metric="cosine",
		spec=ServerlessSpec(cloud='aws', region='us-east-1')
	)

index = pc.Index(index_name)

docsearch = PineconeVectorStore.from_documents(
	documents=text_cunks,
	embedding=embeddings,
	index_name=index_name,
)
