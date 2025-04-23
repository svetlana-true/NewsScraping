# -*- coding: utf-8 -*-
import requests
from langchain_community.document_transformers import Html2TextTransformer
from langchain_community.document_loaders import AsyncHtmlLoader
import os
from . import openai_connect
from . import vector_db
import sys
import re


os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

def get_content(urls):
    # load the content of urls 
    loader = AsyncHtmlLoader(urls)
    docs = loader.load()
        
    # html to text transformer is used for taking the 'clear' content from article 
    html2text = Html2TextTransformer()
    docs_transformed = html2text.transform_documents(docs)
    return docs_transformed

def get_urls():
    print("Enter urls or file with urls:")
    input_line = input() # waiting data from cli
    print("Your input is: " + input_line)
    urls = []
    # check that the input is a file with urls
    if ".txt" in input_line and os.path.isfile(input_line):
        with open(input_line) as file: # open the file
            # Take each line separately and save it as the element of urls list
            urls = [line.rstrip() for line in file]
    # another option of input if the urls separated with comma
    elif input_line.startswith("http"):
        urls.extend(re.split(r'[\s]+', input_line.strip()))
    # last option stops the app
    else:
        print('Wrong format of input. Use one url or the existed txt file with the url on each line')
        sys.exit()
        
    print(f"URLs are: {urls}")
    
    # taking the 'clear' content from urls 
    transformed_content = get_content(urls)
    
    # initialize class for connection with OpenAI
    openAIConnect = openai_connect.OpenAIConnection()
    # initialize class for saving data with indexes and into vectorDB 
    vectorDB = vector_db.VectorDB(urls)

    for content in transformed_content:
        # get summary and topics for each article
        article_content = openAIConnect.openai_request(content)
        # fill the vectorDb with summary and topics for each article 
        vectorDB.prepare_data(article_content)
        
    # create FAISS indices for input articles
    vectorDB.createFaissIndex()
    # initialize FAISS vector store
    vectorDB.createVectorStore()
    
    query="start"
    # The search can be repeated based on different queries until "stop" is written
    while(query != "stop"):
        print("Pring your query or write stop to stop requesting:")
        query = input()
        if query == 'stop':
            continue
        # There are two searches implemented here
        # The first search is based on FAISS indices for input articles
        vectorDB.search_in_db(query)
        # The second search is based on FAISS vecture store
        vectorDB.simularity_search(query)
