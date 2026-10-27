import os
import boto3
from dotenv import load_dotenv
from botocore.exceptions import ClientError
import streamlit as st

# Environment variables
load_dotenv()

REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Exact Knowledge Base ID (with digit '0')
KNOWLEDGE_BASE_ID = "UTIWL0WLXD"

@st.cache_resource
def get_bedrock_agent_client():
    return boto3.client(
        service_name="bedrock-agent-runtime",
        region_name=REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

agent_client = get_bedrock_agent_client()

# --- Streamlit Setup ---
st.set_page_config(page_title="RAG Assistant | Bedrock KB", page_icon="📚", layout="centered")
st.title("📚 RAG Assistant (Bedrock Agentic KB)")
st.caption("Powered by AWS Bedrock Managed Knowledge Base & S3")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.header("Settings")
    st.write(f"**Region:** `{REGION}`")
    st.write(f"**Knowledge Base ID:** `{KNOWLEDGE_BASE_ID}`")
    st.divider()
    if st.button("Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User prompt
if prompt := st.chat_input("Ask a question about your documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        source_documents = set()

        try:
            with st.spinner("Agent searching knowledge base..."):
                # Agentic Retrieve Stream API
                response = agent_client.agentic_retrieve_stream(
                    messages=[{"role": "user", "content": {"text": prompt}}],
                    retrievers=[{"configuration": {"knowledgeBase": {"knowledgeBaseId": KNOWLEDGE_BASE_ID}}}],
                    agenticRetrieveConfiguration={
                        "foundationModelType": "MANAGED",
                        "maxAgentIteration": 5,
                    },
                    generateResponse=True,
                )

            # Stream response chunks
            for event in response.get("stream", []):
                # 1. Streamed Answer Text
                if "responseEvent" in event:
                    token = event["responseEvent"].get("text", "")
                    full_response += token
                    response_placeholder.markdown(full_response + "▌")

                # 2. Retrieved Chunks / Sources
                elif "result" in event:
                    for item in event["result"].get("results", []):
                        location = item.get("location", {}).get("s3Location", {}).get("uri", "")
                        if location:
                            doc_name = location.split("/")[-1]
                            source_documents.add(doc_name)

            # Append source list at the bottom
            final_output = full_response
            if source_documents:
                final_output += "\n\n---\n**📄 Sources:**\n"
                for doc in sorted(source_documents):
                    final_output += f"- `{doc}`\n"

            response_placeholder.markdown(final_output)
            st.session_state.messages.append({"role": "assistant", "content": final_output})

        except ClientError as err:
            error_code = err.response["Error"]["Code"]
            error_msg = err.response["Error"]["Message"]
            st.error(f"AWS Error [{error_code}]: {error_msg}")
        except Exception as e:
            st.error(f"Error: {str(e)}")