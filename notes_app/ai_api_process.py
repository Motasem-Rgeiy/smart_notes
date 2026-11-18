from google import genai
from google.genai import types, errors
import os
from langchain_community.document_loaders import TextLoader
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import time

load_dotenv()


gemini_api_key = os.getenv('GEMINI_API_KEY')

def content_process_gemini(content , system_settings):
    try:
        client = genai.Client(api_key=gemini_api_key)

        config = types.GenerateContentConfig(
        system_instruction=system_settings,
        temperature=0.7,
    )

    # Call generate_content_stream with configuration parameters
        response = client.models.generate_content_stream(
            model="gemini-3.1-flash-lite-preview",
            contents=content,
            config=config
    )
     

     #Process chunks as they arrive
        for chunk in response:
            print(chunk.text, end="", flush=True)
            yield chunk.text
    except errors.APIError as error:
        print(f'Error code: {error.code}')
        print(f"Error message: {error.message}")
        yield f"The server is not responded {error.code}"
    
    #return response.output_text




#content_summary_gemini(content)


def chatbot_assistant(user_input, username):
    try:
        loader = TextLoader("questions.txt", encoding='utf-8')
        documents = loader.load()
        file_content = documents[0].page_content

      
        llm = ChatGoogleGenerativeAI(
            model="gemini-3.1-flash-lite-preview",  
            api_key=gemini_api_key
        )

       
        template = """
        You are a helpful assistant. Use the following reference document containing questions and answers to answer the user. 
        If the answer cannot be found in the reference document, say "I don't have information on that in my database.".
        Don't say the user that you use the referense documnet to learn about application.
        Don't tell the user about technical details.
        Make the user has a good experience by give him answers.
        Any questions that is not exist in the document, answer them by "No".
        The most important thing: Depends on the information in the document for knowledge, but answer the user in your way.
        Now you deal with username {username}, call his name sometimes.

        Reference Document:
        {reference_data}

        User Question: {question}
        """
        prompt = PromptTemplate.from_template(template)

       
        chain = prompt | llm
        
        response = chain.invoke({
            "reference_data": file_content,
            "question": user_input,
            'username': username
        })
        
    
        # response.content is directly a string in LangChain
        
      

        for chunk in response.text:
            yield chunk
            time.sleep(0.015)

       # answer = response.text
       # print(answer)
       # return answer

    except errors.APIError as error:
        print(f'Error code: {error.code}')
        print(f"Error message: {error.message}")
        yield f"The server is not responded {error.code}"
   