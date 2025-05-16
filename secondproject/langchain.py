from langchain_openai import OpenAIEmbeddings,ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from decouple import config
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate

def getResult(question,session_id):
    SECRET_KEY=config('OPENAI_API_KEY')
    chat=ChatOpenAI(openai_api_key=SECRET_KEY)

    embedding_function=OpenAIEmbeddings(openai_api_key=SECRET_KEY)

    db_path = f'./user_database/{session_id}'

    # db_connection=Chroma('gautam',embedding_function=embedding_function,persist_directory='./firstchroma_db')
    db_connection=Chroma('gautam',embedding_function=embedding_function,persist_directory=db_path)

    retriever=db_connection.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.5})
    # similar_docs=retriever.get_relevant_documents(question)

    docs = retriever.invoke(question)

    # print(docs[0].page_content)

    human_template="{question}\n{documents}"

    chat_prompt=ChatPromptTemplate.from_messages([
    HumanMessagePromptTemplate.from_template(human_template)
        ])

    formatted_chat_prompt=chat_prompt.format_messages(
    question=question,
    documents=docs
    )
    response=chat.invoke(formatted_chat_prompt)
    print(response.content)
    
    return response.content


