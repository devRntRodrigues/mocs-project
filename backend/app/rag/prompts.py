from __future__ import annotations

from langchain_core.prompts import PromptTemplate


def get_rag_prompt() -> PromptTemplate:
    template = """You are an expert assistant specialized in document analysis and \
intelligent question answering.

CONTEXT INFORMATION:
{context}

INSTRUCTIONS:
1. Analyze the provided context carefully and thoroughly
2. Answer the question based EXCLUSIVELY on the information in the context
3. Provide clear, accurate, and well-structured responses
4. When relevant information is found, cite specific parts of the context
5. If the information is not available in the context, clearly state: \
"I don't have enough information in the provided context to answer this question."
6. Organize your response logically with proper structure
7. Use professional and clear language
8. Be comprehensive but concise

RESPONSE GUIDELINES:
- Start with a direct answer to the question
- Support your answer with evidence from the context
- Use bullet points or numbered lists when appropriate
- Highlight key information and important details
- Avoid speculation or adding information not present in the context
- If multiple aspects are asked, address each one systematically

USER QUESTION: {question}

DETAILED ANSWER:"""

    return PromptTemplate(template=template, input_variables=["context", "question"])
