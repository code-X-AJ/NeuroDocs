import os
from fastapi import FastAPI, UploadFile, File, HTTPException
import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain.vectorstores import FAISS
# from langchain.chains import ConversationRetrievalChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
load_dotenv()
from pydantic import BaseModel
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

app = FastAPI()
class QuestionRequest(BaseModel):
    question: str

# Global variables to store document and conversation state
vector_store = None
conversation_memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)
custom_prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
    You are an expert document analysis assistant. 

    Based on the following context documents, please provide a concise, well-structured answer to the question.

    Please ensure your answer:
    1. Is brief but informative, focusing on the most important points
    4. Uses bullet points sparingly for clarity when needed
    5. Keeps the total response to around 100 words
    6. If the information is not in the context, clearly state that

    Question: {question}

    Context:
    {context}

    Answer:
    """
)


# Initialize LLM using OpenAI (ensure your API key is set in your .env file)
llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), temperature=0.5)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Read PDF contents
    contents = await file.read()

    # Extract text from PDF
    pdf_text = ""
    try:
        with fitz.open(stream=contents, filetype="pdf") as doc:
            for page in doc:
                pdf_text += page.get_text()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing PDF: {str(e)}")

    # Split text into chunks using RecursiveCharacterTextSplitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", "!", "?", " ", ""]
    )
    chunks = splitter.split_text(pdf_text)

    # Create vector store from text chunks and update global variable
    global vector_store
    try:
        vector_store = FAISS.from_texts(
            texts=chunks,
            embedding=OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"), model="text-embedding-3-large")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating embeddings: {str(e)}")
    
    return {"status": "success", "filename": file.filename, "total_chunks": len(chunks)}

@app.post("/query")
async def query_document(request: QuestionRequest):
# async def query_document(question: str):
    question = request.question

    if not vector_store:
        raise HTTPException(status_code=400, detail="No document uploaded yet.")

    try:
        # Create a simple retrieval-based QA chain.
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",  # "stuff" combines context into a single string
            retriever=vector_store.as_retriever(),
            chain_type_kwargs={"prompt": custom_prompt_template},
            memory=conversation_memory
        )
        # Run the QA chain with the provided question.
        print("question..........", question)
        answer = qa_chain.run(question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during query processing: {str(e)}")

    return {"question": question, "answer": answer}
