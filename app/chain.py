from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

def create_qa_chain(retriever):
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
    prompt_template = """Gebruik de volgende context om de vraag te beantwoorden.
Als je het antwoord niet weet, zeg dan eerlijk dat je het niet weet.

Context: {context}

Vraag: {question}

Antwoord:"""

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )
    
    return chain