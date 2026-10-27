# 📚 Enterprise RAG Assistant: AWS Bedrock Knowledge Base & Streamlit

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![AWS Bedrock](https://img.shields.io/badge/AWS-Bedrock%20KB-FF9900.svg?logo=amazon-aws&logoColor=white)](https://aws.amazon.com/bedrock/)
[![Amazon S3](https://img.shields.io/badge/Amazon-S3-569A31.svg?logo=amazon-s3&logoColor=white)](https://aws.amazon.com/s3/)
[![OpenSearch](https://img.shields.io/badge/Vector%20Store-Managed%20OpenSearch-005FD6.svg?logo=opensearch&logoColor=white)](https://opensearch.org/)

An enterprise-grade, cloud-native **Retrieval-Augmented Generation (RAG)** system built with **Amazon Bedrock Knowledge Bases** and **Streamlit**. It indexes unstructured documents (PDFs) from **Amazon S3**, leverages a serverless vector store for semantic retrieval, and streams synthesized answers with exact document citations using Bedrock's **Agentic Retrieve Stream** runtime.

---

## 🏛️ System Architecture

```text
  ┌───────────────────────┐
  │   Unstructured Data   │ (PDFs, Policies, FAQs)
  └───────────┬───────────┘
              │ (Automated Upload)
              ▼
    ┌───────────────────┐
    │  Amazon S3 Bucket │
    └─────────┬─────────┘
              │ (Data Source Sync)
              ▼
┌───────────────────────────────┐
│  Bedrock Knowledge Base (KB)  │
│  - Text Chunking Engine       │
│  - Titan Embeddings Model     │
│  - Managed Vector Store       │
└──────────────┬────────────────┘
               ▲
               │ Semantic Retrieval / Citations
               ▼
┌───────────────────────────────┐
│     Bedrock Agent Runtime     │
│ (agentic_retrieve_stream API) │
│ - Query Planning              │
│ - Managed Claude Model        │
└──────────────┬────────────────┘
               ▲
               │ Token-by-Token Streaming
               ▼
┌───────────────────────────────┐
│      Streamlit Web Client     │
│   (Real-time Chat & UI)       │
└───────────────────────────────┘
