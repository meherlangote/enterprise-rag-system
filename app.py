import re
import streamlit as st

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from app.retrieval.hybrid_retriever import hybrid_retriever


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Enterprise RAG System",
    page_icon="🤖",
    layout="wide",
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1100px;
}

.stChatMessage {
    border-radius: 12px;
    padding: 12px;
}

code {
    font-size: 14px;
}

</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# TITLE
# =========================================================

st.title(" AI Assistant")

st.markdown(
    """
AI-Powered Technical Knowledge Understanding and Research Platform """
)

# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================================================
# LOAD LLM
# =========================================================

@st.cache_resource
def load_llm():

    llm = ChatOllama(
        model="qwen2.5:3b",
        temperature=0,
    )

    return llm


llm = load_llm()

# =========================================================
# PROMPT TEMPLATE
# =========================================================

prompt_template = ChatPromptTemplate.from_template(
    """
You are an enterprise-grade AI assistant.

IMPORTANT RULES:

1. Answer ONLY using the provided context.

2. Do NOT hallucinate.

3. If answer is not available in context, say:
"I could not find sufficient information in the provided documents."

4. Format ALL:
- formulas
- equations
- derivations
using proper LaTeX.

5. ALWAYS wrap equations inside:

$$
equation_here
$$

6. Use markdown formatting.

7. Keep answers technical and concise.

8. If code is required:
- return properly formatted code blocks

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""
)

# =========================================================
# SMART RESPONSE RENDERER
# =========================================================

def render_response(text):

    """
    Render markdown + latex
    while preserving original order.
    """

    # -----------------------------------------------------
    # Split content sequentially
    # -----------------------------------------------------

    parts = re.split(
        r"(\$\$.*?\$\$)",
        text,
        flags=re.DOTALL,
    )

    # -----------------------------------------------------
    # Render each part
    # -----------------------------------------------------

    for part in parts:

        if not part.strip():
            continue

        # -------------------------------------------------
        # LATEX BLOCK
        # -------------------------------------------------

        if (
            part.startswith("$$")
            and part.endswith("$$")
        ):

            equation = (
                part.replace("$$", "")
                .strip()
            )

            if equation:

                st.latex(equation)

        # -------------------------------------------------
        # NORMAL TEXT
        # -------------------------------------------------

        else:

            st.markdown(part)

# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        render_response(
            message["content"]
        )

# =========================================================
# CHAT INPUT
# =========================================================

query = st.chat_input(
    "Ask a question about your PDFs..."
)

# =========================================================
# MAIN QUERY PIPELINE
# =========================================================

if query:

    # =====================================================
    # STORE USER MESSAGE
    # =====================================================

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query,
        }
    )

    # =====================================================
    # DISPLAY USER MESSAGE
    # =====================================================

    with st.chat_message("user"):

        st.markdown(query)

    # =====================================================
    # ASSISTANT RESPONSE
    # =====================================================

    with st.chat_message("assistant"):

        with st.spinner(
            "Retrieving relevant context..."
        ):

            try:

                # =============================================
                # RETRIEVE DOCUMENTS
                # =============================================

                results = hybrid_retriever.retrieve(
                    query=query,
                    k=5,
                )

                # =============================================
                # EMPTY RETRIEVAL
                # =============================================

                if not results:

                    final_answer = (
                        "I could not find sufficient "
                        "information in the provided documents."
                    )

                    render_response(
                        final_answer
                    )

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": final_answer,
                        }
                    )

                else:

                    # =========================================
                    # BUILD CONTEXT
                    # =========================================

                    context = "\n\n".join(
                        [
                            doc.page_content
                            for doc in results
                        ]
                    )

                    # =========================================
                    # RETRIEVAL INFO
                    # =========================================

                    st.info(
                        f"Retrieved {len(results)} documents"
                    )

                    # =========================================
                    # BUILD PROMPT
                    # =========================================

                    formatted_prompt = (
                        prompt_template.format(
                            context=context,
                            question=query,
                        )
                    )

                    # # =========================================
                    # # GENERATE RESPONSE
                    # # =========================================

                    # response = llm.invoke(
                    #     formatted_prompt
                    # )

                    # final_answer = (
                    #     response.content
                    # )

                    # # =========================================
                    # # DISPLAY RESPONSE
                    # # =========================================

                    # render_response(
                    #     final_answer
                    # )

                    # =========================================
                    # STREAMING RESPONSE
                    # =========================================

                    response_stream = llm.stream(
                        formatted_prompt
                    )

                    full_response = ""

                    response_placeholder = st.empty()

                    for chunk in response_stream:

                        if chunk.content:

                            full_response += chunk.content

                            # Live streaming effect
                            response_placeholder.markdown(
                                full_response + "▌"
                            )

                    # =========================================
                    # FINAL RESPONSE
                    # =========================================

                    final_answer = full_response

                    # Remove streaming placeholder
                    response_placeholder.empty()

                    # Render properly formatted output
                    render_response(final_answer)
                                        
                                        
                    # =========================================
                    # STORE CHAT HISTORY
                    # =========================================

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": final_answer,
                        }
                    )

                    # =========================================
                    # SOURCE DOCUMENTS
                    # =========================================

                    with st.expander(
                        "📚 Source Documents"
                    ):

                        for idx, doc in enumerate(results):

                            st.markdown(
                                f"### Source {idx + 1}"
                            )

                            st.markdown(
                                f"""
**Metadata**
- Source: {doc.metadata.get('source', 'Unknown')}
- Page: {doc.metadata.get('page', 'N/A')}
- Section: {doc.metadata.get('section', 'N/A')}
"""
                            )

                            st.code(
                                doc.page_content[:1500],
                                language="text",
                            )

                            st.divider()

            except Exception as e:

                st.error(
                    f"Error occurred: {str(e)}"
                )