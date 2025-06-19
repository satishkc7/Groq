import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
import re
import streamlit as st


from dotenv import load_dotenv

load_dotenv()

class StreamlitConversationalChatbot:
    def __init__(self):
        os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        
        self.llm = ChatGroq(
            groq_api_key=self.groq_api_key,
            model_name="llama3-8b-8192"
        )
        
        self.vectors = None
        self.retrieval_chain = None
        
        self.prompt = ChatPromptTemplate.from_template(
            """You are a friendly and knowledgeable conversational assistant for FoodPass on StartEngine. 
            Answer questions in a conversational and engaging way based on the provided context from the FoodPass offering page.
            Be helpful, enthusiastic, and natural in your responses. Don't mention that you're using specific sources or documents.
            Keep responses concise but informative. If you don't know something, politely say so.
            
            Context from FoodPass offering page:
            {context}
            
            User Question: {input}
            
            Your response:"""
        )
    
    def clean_text(self, text):
        """Clean and normalize text content"""
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', '', text)
        return text.strip()
    
    def scrape_website(self, base_url, max_pages=10):
        """Scrape website content starting from base_url"""
        scraped_pages = []
        visited_urls = set()
        urls_to_visit = [base_url]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        with st.status("🔍 Scraping FoodPass website...") as status:
            while urls_to_visit and len(scraped_pages) < max_pages:
                current_url = urls_to_visit.pop(0)
                
                if current_url in visited_urls:
                    continue
                    
                try:
                    response = requests.get(current_url, headers=headers, timeout=10)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Remove script and style elements
                    for script in soup(["script", "style", "nav", "footer", "header"]):
                        script.decompose()
                    
                    # Extract text content
                    text_content = soup.get_text()
                    text_content = self.clean_text(text_content)
                    
                    # Extract title
                    title = soup.find('title')
                    title_text = title.get_text() if title else "No Title"
                    
                    if len(text_content) > 100: 
                        scraped_pages.append({
                            'url': current_url,
                            'title': title_text,
                            'content': text_content
                        })
                    
                    visited_urls.add(current_url)
                    
                    # Find more links to visit (only from the same domain)
                    if len(scraped_pages) < max_pages:
                        domain = urlparse(base_url).netloc
                        for link in soup.find_all('a', href=True):
                            href = link['href']
                            full_url = urljoin(current_url, href)
                            
                            if (urlparse(full_url).netloc == domain and 
                                full_url not in visited_urls and 
                                full_url not in urls_to_visit):
                                urls_to_visit.append(full_url)
                                
                except Exception as e:
                    st.warning(f"⚠️  Error scraping {current_url}: {str(e)}")
                    continue
            
            status.update(label=f"✅ Successfully scraped {len(scraped_pages)} pages", state="complete")
        
        return scraped_pages
    
    def create_documents_from_website(self, scraped_pages):
        """Convert scraped website content to LangChain documents"""
        documents = []
        for page in scraped_pages:
            doc = Document(
                page_content=page['content'],
                metadata={
                    'source': page['url'],
                    'title': page['title']
                }
            )
            documents.append(doc)
        return documents
    
    def setup_rag_model(self, website_url, max_pages=10):
        """Setup the RAG model with website content"""
        with st.status("🚀 Setting up RAG model...") as status:
            # Scrape website
            scraped_pages = self.scrape_website(website_url, max_pages)
            
            if not scraped_pages:
                st.error("❌ No content could be scraped from the website. Please check the URL.")
                return False
            
            # Process documents
            status.update(label="📄 Processing documents...")
            embeddings = OpenAIEmbeddings()
            documents = self.create_documents_from_website(scraped_pages)
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, 
                chunk_overlap=200
            )
            final_documents = text_splitter.split_documents(documents)
            
            # Create vector store
            status.update(label="🔢 Creating vector store...")
            self.vectors = FAISS.from_documents(final_documents, embeddings)
            
            # Create retrieval chain
            document_chain = create_stuff_documents_chain(self.llm, self.prompt)
            retriever = self.vectors.as_retriever(search_kwargs={"k": 3})
            self.retrieval_chain = create_retrieval_chain(retriever, document_chain)
            
            status.update(label=f"✅ RAG model ready! Processed {len(final_documents)} document chunks", state="complete")
        
        return True
    
    def get_response(self, user_input):
        """Get response from the chatbot"""
        if not self.retrieval_chain:
            return "I'm sorry, but I haven't been set up with any company information yet. Please provide a website URL first."
        
        try:
            with st.spinner("🤖 Thinking..."):
                start_time = time.time()
                response = self.retrieval_chain.invoke({
                    'input': user_input
                })
                response_time = time.time() - start_time
                
                answer = response['answer']
                return answer
                
        except Exception as e:
            return f"I'm sorry, I encountered an error: {str(e)}"

def main():
    st.set_page_config(
        page_title="FoodPass Chatbot",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 FoodPass Conversational Chatbot")
    st.markdown("Ask me anything about the FoodPass offering on StartEngine!")
    
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = StreamlitConversationalChatbot()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    with st.sidebar:
        st.header("⚙️ Setup")
        
        if st.button("🚀 Setup FoodPass Chatbot", type="primary"):
            website_url = "https://www.startengine.com/offering/foodspass"
            success = st.session_state.chatbot.setup_rag_model(website_url)
            
            if success:
                st.success("✅ Chatbot is ready! Ask me anything about FoodPass.")
                st.session_state.chatbot_ready = True
            else:
                st.error("❌ Failed to setup chatbot. Please try again.")
                st.session_state.chatbot_ready = False
        
        if hasattr(st.session_state, 'chatbot_ready'):
            if st.session_state.chatbot_ready:
                st.success("🤖 Chatbot Status: Ready")
            else:
                st.error("🤖 Chatbot Status: Not Ready")
        else:
            st.info("🤖 Chatbot Status: Not Setup")
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("This chatbot is trained on the FoodPass offering page from StartEngine.")
    
    st.header("💬 Chat with FoodPass Assistant")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Ask me about FoodPass..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        if not hasattr(st.session_state, 'chatbot_ready') or not st.session_state.chatbot_ready:
            response = "Please setup the chatbot first using the button in the sidebar."
        else:
            response = st.session_state.chatbot.get_response(prompt)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        with st.chat_message("assistant"):
            st.markdown(response)
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    main() 
