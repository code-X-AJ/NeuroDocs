import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set the FastAPI server URL
# API_URL = "http://localhost:8000"  # Change if your FastAPI runs on different port
API_URL = "https://neurodocs-1.onrender.com"  # Change if your FastAPI runs on different port

st.set_page_config(
    page_title="NeuroDocs",
    page_icon="📄",
    layout="wide"
)

def main():
    st.title("📄 NeuroDocs")
    
    # Sidebar for API configuration
    with st.sidebar:
        st.header("Configuration")
        api_endpoint = st.text_input("API Endpoint", API_URL)
        st.write("---")
        st.markdown("### How it works")
        st.markdown("""
        1. Upload a PDF document
        2. The system extracts text and creates embeddings
        3. Ask questions about your document
        4. Get AI-powered answers based on document content
        """)
    
    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # File uploader
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    
    # Process the uploaded file
    if uploaded_file is not None:
        if st.button("Process PDF"):
            with st.spinner("Processing PDF..."):
                try:
                    # Send the file to the FastAPI endpoint
                    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                    response = requests.post(f"{api_endpoint}/upload", files=files)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"Successfully processed {result['filename']}!")
                        
                        # Store the upload success in session state
                        st.session_state.pdf_uploaded = True
                        
                    else:
                        st.error(f"Error processing PDF: {response.text}")
                        
                except Exception as e:
                    st.error(f"Error connecting to API: {str(e)}")
    
    # Query input - only show if a PDF has been uploaded
    if st.session_state.get("pdf_uploaded", False):
        query = st.chat_input("Ask a question about your PDF...")
        
        if query:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": query})
            
            # Display user message
            with st.chat_message("user"):
                st.write(query)
            
            # Send query to API
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = requests.post(
                            f"{api_endpoint}/query",
                            json={"question": query}
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            answer = result["answer"]
                            st.write(answer)
                            
                            # Add assistant response to chat history
                            st.session_state.messages.append({"role": "assistant", "content": answer})
                        else:
                            st.error(f"Error getting answer: {response.text}")
                            
                    except Exception as e:
                        st.error(f"Error connecting to API: {str(e)}")
    else:
        st.info("Please upload and process a PDF to start asking questions.")

if __name__ == "__main__":
    main()
