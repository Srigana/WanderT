**This project is a Flask-based web application that allows users to interact with a chatbot that can process PDF files and answer questions based on the content extracted from them. It leverages various technologies, such as Google Generative AI, LangChain, and FAISS, to provide detailed responses to user queries.**

**Features**
PDF Upload and Processing:
Users can upload PDF files, and the application will extract text from them.
The text is split into chunks for efficient processing.

Question Answering:
The chatbot can answer questions based on the content of the uploaded PDF.
If a question doesn't have an answer in the provided content, the chatbot will notify the user.

Greeting Responses:
The chatbot can respond to predefined greetings like "hello", "hi", and more.
Integration with Google Generative AI:

Uses Google's embedding models for text understanding and question answering.
Requirements
Python 3.8+
Flask
PyPDF2
LangChain
LangChain Google Generative AI (langchain_google_genai)
FAISS
dotenv
Google API Key for access to Google's Generative AI models
**Setup**
Step 1: Clone the Repository
git clone https://github.com/yourusername/chatbot-with-pdf-processing.git
cd chatbot-with-pdf-processing
Step 2: Install Dependencies
Install the required libraries by running:
pip install -r requirements.txt
Step 3: Set Up Environment Variables
Create a .env file in the root directory and add your Google API key like this:
GOOGLE_API_KEY=your-google-api-key
Step 4: Run the Application
Start the Flask application with:
python app.py
The application will be available at http://localhost:5000.

Step 5: Interact with the Chatbot
Upload a PDF:
Navigate to the /upload_pdf route to upload and process PDF files. You can use the form to select and upload multiple PDFs.

Ask Questions:
The chatbot will respond to questions based on the uploaded PDFs. If the answer is not available in the context, it will return a default message.

Predefined Greetings:
The chatbot recognizes various greeting phrases (e.g., "Hi", "Hello", "How are you?").
