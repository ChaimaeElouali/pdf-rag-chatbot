import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from app.chain import create_qa_chain
from app.ingest import load_and_split_pdf
from app.retriever import create_vectorstore, get_retriever

load_dotenv()

st.set_page_config(
    page_title="DocuMind — PDF RAG",
    page_icon="📑",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "# DocuMind\nProfessionele PDF Q&A met retrieval-augmented generation.",
    },
)

st.markdown(
    """
    <style>
    .dm-header {
        padding: 1.25rem 0 0.75rem 0;
        border-bottom: 1px solid rgba(15, 118, 110, 0.18);
        margin-bottom: 1.25rem;
    }
    .dm-header h1 {
        font-size: 1.85rem;
        font-weight: 650;
        letter-spacing: -0.02em;
        margin: 0 0 0.35rem 0;
        color: #0F172A;
    }
    .dm-header p {
        margin: 0;
        font-size: 1.02rem;
        color: #475569;
        line-height: 1.45;
    }
    div[data-testid="stSidebar"] {
        border-right: 1px solid rgba(15, 23, 42, 0.08);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def _init_session():
    defaults = {
        "chat_history": [],
        "chain": None,
        "processed_file_sig": None,
        "page_count": None,
        "chunk_count": None,
        "current_pdf_name": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def _display_page_label(page_meta):
    if page_meta is None:
        return "Onbekende pagina"
    if isinstance(page_meta, int):
        return f"Pagina {page_meta + 1}"
    return f"Pagina {page_meta}"


def _sources_from_docs(docs):
    out = []
    for doc in docs:
        out.append(
            {
                "page": doc.metadata.get("page"),
                "content": doc.page_content or "",
            }
        )
    return out


def _render_assistant_message(content: str, sources: list | None):
    st.markdown(content)
    if not sources:
        return
    st.caption("Bronnen uit je PDF")
    for src in sources:
        label = f"📄 {_display_page_label(src.get('page'))}"
        with st.expander(label, expanded=False):
            st.markdown(src.get("content", "").strip() or "_(Geen tekst in dit fragment.)_")


_init_session()

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

with st.sidebar:
    st.markdown("### Instellingen")
    st.caption("Upload een document om te beginnen.")

    if st.button("Clear chat", use_container_width=True, type="secondary"):
        st.session_state.chat_history = []
        st.rerun()

    st.divider()
    st.markdown("##### Document")
    uploaded_file = st.file_uploader(
        "PDF-bestand",
        type="pdf",
        help="Het bestand wordt lokaal verwerkt; stel daarna vragen over de inhoud.",
    )

    if uploaded_file is not None:
        file_sig = (uploaded_file.name, uploaded_file.size)
        if st.session_state.processed_file_sig != file_sig:
            temp_path = DATA_DIR / uploaded_file.name
            with st.status("**Bezig met verwerken…**", expanded=True) as status:
                status.write("Bestand opslaan…")
                temp_path.write_bytes(uploaded_file.getbuffer())

                status.write("Tekst extraheren en in stukken splitsen…")
                chunks, num_pages = load_and_split_pdf(str(temp_path))

                status.write("Embeddings berekenen en zoekindex bouwen…")
                vectorstore = create_vectorstore(chunks)
                retriever = get_retriever(vectorstore)
                st.session_state.chain = create_qa_chain(retriever)

                status.write("✅ Document is klaar voor vragen.")

            st.session_state.processed_file_sig = file_sig
            st.session_state.page_count = num_pages
            st.session_state.chunk_count = len(chunks)
            st.session_state.current_pdf_name = uploaded_file.name

        st.success("Document actief")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Pagina’s", st.session_state.page_count or "—")
        with c2:
            st.metric("Chunks", st.session_state.chunk_count or "—")
        if st.session_state.current_pdf_name:
            st.caption(f"**Bestand:** {st.session_state.current_pdf_name}")

st.markdown(
    """
    <div class="dm-header">
        <h1>📑 DocuMind</h1>
        <p>Stel gerichte vragen over je PDF — met duidelijke bronverwijzingen per pagina.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

main = st.container()
with main:
    if st.session_state.chain is None:
        st.info(
            "**Welkom.** Upload een PDF in de zijbalk om te starten. "
            "Daarna kun je hier chatten; antwoorden worden ondersteund met fragmenten uit jouw document."
        )
        st.markdown(
            "- **Privacy:** bestanden worden lokaal opgeslagen in de map `data/`.\n"
            "- **Tips:** stel specifieke vragen voor nauwkeurigere antwoorden.\n"
            "- Open een **bron-expander** onder elk antwoord om de bijbehorende paginatekst te bekijken."
        )
    else:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                if message["role"] == "assistant":
                    _render_assistant_message(
                        message["content"],
                        message.get("sources"),
                    )
                else:
                    st.markdown(message["content"])

if question := st.chat_input("Stel een vraag over je document…"):
    if st.session_state.chain is None:
        st.warning("Upload eerst een PDF in de zijbalk.")
    else:
        st.session_state.chat_history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Antwoord samenstellen…"):
                result = st.session_state.chain.invoke({"query": question})
                answer = result["result"]
                source_docs = result.get("source_documents") or []
                sources_list = _sources_from_docs(source_docs)
                _render_assistant_message(answer, sources_list)

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": answer,
                "sources": sources_list,
            }
        )
