from flask import Flask, request, render_template
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv


load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "I'm sorry, but I don't have the information you're looking for. Is there anything else I can assist you with?", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def process_question(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    # Load FAISS index with allow_dangerous_deserialization=True
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    return response["output_text"]

def upload_default_pdf():
    default_pdf_path = "https://drive.google.com/file/d/1opsgtC9LgP6PzURJt_2cAJXIcUZXhuNR/view?usp=sharing"  
    pdf_text = get_pdf_text([default_pdf_path])
    text_chunks = get_text_chunks(pdf_text)
    get_vector_store(text_chunks)


upload_default_pdf()

# Predefined queries and responses for greetings
greetings = {
    "hi": "Hello! How can I assist you today?",
    "hello": "Hi there! How may I help you?",
    "hey": "Hey! What can I do for you?",
    "how are you": "I'm just a bot, but I'm here to help you!",
    "what's up": "Not much, just here to assist you!",
    "what is your name" : "I'm a chatbot here to assist you. You can call me Wander-T!",
    "tell me about yourself" : "I'm a travel chatbot designed to assist you with various tasks and answer your questions to the best of my ability. If you have any specific questions or need assistance related to telangana travel, feel free to ask, and I'll do my best to help you! ",
    "who are you" : "I'm a travel chatbot designed to assist you with various tasks and answer your questions to the best of my ability. If you have any specific questions or need assistance related to telangana travel, feel free to ask, and I'll do my best to help you!",
    "bye" : "Byeee! Have a great day!",
    "thank you": "You're welcome! I'm here to help whenever you need assistance.",
    "what are you doing" : "I'm here, ready and waiting to assist you!",
    "how can you help me" : "I'm a travel chatbot designed to assist you with various tasks and answer your questions to the best of my ability. If you have any specific questions or need assistance related to telangana travel, feel free to ask, and I'll do my best to help you!",
    "what can you do" : "I'm a travel chatbot designed to assist you with various tasks and answer your questions to the best of my ability. If you have any specific questions or need assistance related to telangana travel, feel free to ask, and I'll do my best to help you!",
    "are you a real person" : "No, I am not a real person.",
    "who created you" : "I was created by Srigana Pulikantham",
    "do you have a name" : "Yes, my name is Wander-T"
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form.get('msg').lower()
        if user_input:
            for query, response in greetings.items():
                if user_input == query:
                    return response
            response = process_question(user_input)
            return response
    return render_template('chat.html')

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'pdf_files' in request.files:
        pdf_files = request.files.getlist('pdf_files')
        raw_text = get_pdf_text(pdf_files)
        text_chunks = get_text_chunks(raw_text)
        get_vector_store(text_chunks)
        return "PDF files uploaded and processed successfully!"
    return "No PDF files were uploaded."


if __name__ == '__main__':
    app.run(debug=True)
