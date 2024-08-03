import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from flask import Flask, request, render_template


llm_app = Flask(__name__)

#
def initialize_chatbot():
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Provide response to the user queries"),
            ("user", "Question: {question}")
        ]
    )
    
    llm = Ollama(model="llama3")
    output_parser = StrOutputParser()
    
    chain = prompt | llm | output_parser
    return chain

# Initialize chatbot
chain = initialize_chatbot()

@llm_app.route('/ai', methods=['POST'])
def home():
    request_data = request.get_json()
    output = chain.invoke({'question': request_data['Question']})

    return output, 201

if __name__ == '__main__':
    llm_app.run(debug=True)




