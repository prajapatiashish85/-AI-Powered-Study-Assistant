import streamlit as st
import tempfile
import time

from google import genai

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="🎓",
    layout="wide"
)


# ---------------------------------------
# SESSION STATE
# ---------------------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ---------------------------------------
# SIDEBAR
# ---------------------------------------

with st.sidebar:
    st.title("🎓 AI Study Assistant")
    st.markdown("---")

    st.subheader("📌 Features")
    st.success("✔ PDF Upload")
    st.success("✔ AI Question Answering")
    st.success("✔ FAISS Search")
    st.success("✔ Gemini AI")
    st.success("✔ Chat History")

    st.markdown("---")

    st.info("""
Built with:

• Streamlit  
• LangChain  
• HuggingFace  
• FAISS  
• Google Gemini
""")

    if st.button("🗑 Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()


# ---------------------------------------
# MAIN HEADING
# ---------------------------------------

st.title("🎓 AI Powered Study Assistant")

st.caption(
    "Upload your study material and ask questions using AI-powered retrieval."
)

st.write(
    "Upload your PDF and ask questions using Gemini AI."
)

st.divider()


# ---------------------------------------
# GEMINI API
# ---------------------------------------

api_key = st.text_input(
    "Enter Gemini API Key",
    type="password"
)

client = None

if api_key:
    try:
        client = genai.Client(api_key=api_key)
        st.success("✅ Gemini Connected")

    except Exception as error:
        st.error(f"Gemini connection error: {error}")

st.divider()


# ---------------------------------------
# PDF UPLOAD
# ---------------------------------------

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

vector_db = None
documents = []
chunks = []
full_text = ""


# ---------------------------------------
# LOAD AND PROCESS PDF
# ---------------------------------------

if uploaded_file:

    st.info(
        f"📄 Uploaded file: {uploaded_file.name}"
    )

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        temp_file.write(uploaded_file.getvalue())
        pdf_path = temp_file.name

    try:
        with st.spinner("Reading PDF..."):
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()

        st.success("✅ PDF Loaded Successfully")

        for page in documents:
            full_text += page.page_content + "\n"

        if not full_text.strip():
            st.error(
                "PDF me readable text nahi mila."
            )

        else:
            # ---------------------------------------
            # TEXT CHUNKING
            # ---------------------------------------

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )

            chunks = splitter.split_text(full_text)

            # ---------------------------------------
            # EMBEDDINGS AND FAISS
            # ---------------------------------------

            with st.spinner(
                "Creating embeddings and FAISS database..."
            ):
                embedding_model = HuggingFaceEmbeddings(
                    model_name="BAAI/bge-small-en-v1.5"
                )

                vector_db = FAISS.from_texts(
                    texts=chunks,
                    embedding=embedding_model
                )

            st.success(
                "✅ FAISS Vector Database Ready"
            )

            # ---------------------------------------
            # DOCUMENT STATISTICS
            # ---------------------------------------

            st.subheader("📊 Document Statistics")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Pages",
                len(documents)
            )

            col2.metric(
                "Chunks",
                len(chunks)
            )

            col3.metric(
                "Characters",
                len(full_text)
            )

            col4.metric(
                "Words",
                len(full_text.split())
            )

    except Exception as error:
        st.error(
            f"PDF processing error: {error}"
        )


# ---------------------------------------
# RAG FUNCTION
# ---------------------------------------

def ask_ai(question, vector_database, gemini_client):

    docs = vector_database.similarity_search(
        question,
        k=3
    )

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    prompt = f"""
You are an AI Study Assistant.

Answer only from the provided PDF context.

If the answer is not available in the context, say:
"I couldn't find the answer in the uploaded PDF."

Give a clear and easy-to-understand answer.

Context:
{context}

Question:
{question}

Answer:
"""

    last_error = None

    for attempt in range(3):
        try:
            response = gemini_client.models.generate_content(
                model="gemini-flash-latest",
                contents=prompt
            )

            return response.text, docs

        except Exception as error:
            last_error = error

            if attempt < 2:
                time.sleep(5)

    raise RuntimeError(
        f"Gemini server error: {last_error}"
    )


# ---------------------------------------
# ASK QUESTION
# ---------------------------------------

st.divider()
st.header("💬 Ask Questions")

question = st.text_input(
    "Ask anything from your PDF",
    placeholder="Example: Explain Decision Tree"
)

if st.button(
    "🚀 Ask AI",
    use_container_width=True
):

    if client is None:
        st.error(
            "Please enter Gemini API Key."
        )

    elif vector_db is None:
        st.error(
            "Please upload and process a PDF first."
        )

    elif not question.strip():
        st.warning(
            "Please enter a question."
        )

    else:
        try:
            with st.spinner(
                "AI is generating the answer..."
            ):
                answer, docs = ask_ai(
                    question,
                    vector_db,
                    client
                )

            st.markdown("## 🤖 AI Answer")
            st.success(answer)

            st.session_state.chat_history.append(
                {
                    "question": question,
                    "answer": answer
                }
            )

            st.subheader("📚 Retrieved Sources")

            for index, doc in enumerate(
                docs,
                start=1
            ):
                with st.expander(
                    f"Source {index}"
                ):
                    st.write(
                        doc.page_content
                    )

        except Exception as error:
            st.error(
                "Gemini server abhi busy hai. "
                "Thodi der baad dobara try karein."
            )

            st.caption(str(error))


# ---------------------------------------
# CHAT HISTORY
# ---------------------------------------

st.divider()
st.header("💬 Chat History")

if st.session_state.chat_history:

    for index, chat in enumerate(
        reversed(
            st.session_state.chat_history
        ),
        start=1
    ):
        with st.expander(
            f"Question {index}: {chat['question']}"
        ):
            st.markdown(
                f"**Question:** {chat['question']}"
            )

            st.markdown(
                f"**Answer:** {chat['answer']}"
            )

    chat_text = ""

    for chat in st.session_state.chat_history:
        chat_text += (
            f"Question: {chat['question']}\n"
        )

        chat_text += (
            f"Answer: {chat['answer']}\n"
        )

        chat_text += (
            "-" * 60 + "\n"
        )

    st.download_button(
        label="📥 Download Chat History",
        data=chat_text,
        file_name="chat_history.txt",
        mime="text/plain",
        use_container_width=True
    )

else:
    st.info(
        "No chat history available."
    )


# ---------------------------------------
# FOOTER
# ---------------------------------------

st.divider()

st.caption(
    "© 2026 AI Powered Study Assistant | "
    "Developed by Ashish Prajapati"
)