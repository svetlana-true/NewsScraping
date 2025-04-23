import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()
class OpenAIConnection:
    def __init__(self):
        dial_api_key = os.getenv('API_KEY')
        # the connection to OpenAI through AzureOpenAI service
        self.client = AzureOpenAI(
            api_key = dial_api_key,  # Put your DIAL API Key here
            api_version = "2024-02-01",
            azure_endpoint = "https://ai-proxy.lab.epam.com"
            )
        # the recommended version of the model
        self.deployment_name = "gpt-4o-mini-2024-07-18"
        # the request to OpenAI to catch the summary and topics from the article
        self.prompt_template = """Generate a very short summary that captures key points and identify the main topics with one word of article.
          The result should be the simple dictionary in brackets with the summary and topics as the list of programminwords with spaces
          like {"summary": "value", "topics": ["value 1", "value 2"]}. This is an article: """
        
    def openai_request(self, article):
        # add the body of article to the request to OpenAI 
        prompt = self.prompt_template + article.page_content
        
        #result of the request to OpenAI which is the generated summary and the main topics for article based on a provided prompt
        result = self.client.chat.completions.create(
            model=self.deployment_name,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
        # return only content body from the result
        article_content = (result.choices[0].message.content)
        return article_content
