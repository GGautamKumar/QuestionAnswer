from django.shortcuts import render,redirect
from django.views import View

from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from decouple import config
from langchain_community.vectorstores import Chroma
from secondproject.langchain import getResult

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers.cache_utils import DynamicCache
import os



class Home(View):
    def get(self,request):
        result_data=request.session.get('result_data','')
        conversation = request.session.get("conversation", [])     
        return render(request,'secondproject/home.html',{'result_data':result_data,'conversation':conversation})

    def post(self,request):
        question = request.POST.get('question')
        print("User Question:", question)
        pdfstore=request.FILES.get('pdf')
        if 'file_name' not in request.session:
            request.session['file_name'] = pdfstore.name

        if not request.session.session_key:
            request.session.create()

        session_id = request.session.session_key
        # print(pdfstore)
        document_path = f'./user_document/{session_id}.txt'
        print('pdfstore already in session')
        if not os.path.exists(document_path) or request.session['file_name'] != pdfstore.name:
            request.session['file_name'] = pdfstore.name
            os.makedirs('./user_document', exist_ok=True)
            with open(document_path, "w", encoding="utf-8") as f:
                pass  
        data = {}
        with open(document_path, "r", encoding="utf-8") as f:
            print("hii")
            for line in f:
                if ":" in line:
                    key, value = line.strip().split(":", 1)
                    data[key.strip()] = value.strip()

            # Now you can access values by key
        print("result:", data.get(question))
        if data.get(question) is not None:
            print("Question already in session")
            request.session['result_data']=data.get(question)
            return redirect('/')


        pdf_reader = PdfReader(pdfstore)
        full_text = ""

        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:  # Avoid adding None
                full_text += text

    
        # docs_convert = [Document(page_content=full_text)]

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = text_splitter.split_text(full_text)
        print('Length of docs',len(docs))
        # Now you can pass `docs` into your vector DB, embeddings, etc.
        print("Total chunks created:", len(docs))
        SECRET_KEY=config('OPENAI_API_KEY')

        

        print('session id: ',session_id)
        
        embedding_function=OpenAIEmbeddings(openai_api_key=SECRET_KEY)
        # print(embedding_function)
        # db=Chroma('gautam',embedding_function,'./firstchroma_db')
        db_path = f'./user_database/{session_id}'
        db = Chroma('gautam', embedding_function, db_path)
        db.add_texts(docs)
        db.persist()

        result=getResult(question,session_id)

        conversation = request.session.get("conversation",[])
        if 'conversation' not in request.session:
            request.session['conversation'] = []

        # conversation.append(f"question: {question}")
        # conversation.append(f"result: {result}")
        conversation.append({
        "question": question,
        "answer": result
        })
        request.session["conversation"] = conversation
        request.session.modified = True

        # ai_res_recipe=result
        request.session['result_data']=result
        # print(conversation)

        # new_data = {
        #     "Question": question.strip(),
        #     "result": result.strip()  
        #           } 
        new_data = {
            question.strip():result.strip()  ,
                  } 
        with open(document_path, "a", encoding="utf-8") as f:
            for key, value in new_data.items():
                f.write(f"{key}: {value}\n")         
        return redirect('/')
