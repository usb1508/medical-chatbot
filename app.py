from flask import Flask, render_template, request, jsonify
from src import helper
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.promt import *

import os



app = Flask(__name__)



PINECONE_API_KEY=os.environ.get("PINECONE_API_KEY")
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")
OPEN_AI_MODEL=os.environ.get("OPENAI_MODEL")


os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["OPENAI_MODEL"] = OPEN_AI_MODEL

embeddings = helper.download_embeddings()

index_name = "medical-chatbot"
doc_search = PineconeVectorStore.from_existing_index(
	embedding=embeddings,
	index_name=index_name
)

retriever = doc_search.as_retriever(search_type="similarity", search_kwargs={"k":3})


chatmodel = ChatOpenAI(model_name=OPEN_AI_MODEL, temperature=0)

prompt = ChatPromptTemplate.from_messages(
	[
		("system", system_prompt),
		("user", "Answer the following question: {input}"),
	]
)

question_answer_chain = create_stuff_documents_chain(chatmodel,prompt=prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)




@app.route('/')
def index():
	return render_template('chat.html')



@app.route('/get', methods=["GET", "POST"])
def chat():
	user_message = request.form['msg']
	# print(user_message)
	response = rag_chain.invoke({"input": user_message})
	# print(response)
	bot_message = response["answer"]
	return  str(bot_message)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080, debug=True)