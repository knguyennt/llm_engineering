from openai import OpenAI
from bs4 import BeautifulSoup
import requests

system_prompt = """
Your name is Miku and you shall take the role of Hatsune Miku and response in her style.
You shall answer in the style of the character.
"""

class ChatBot:
    def __init__(self, system_prompt, **kwargs):
        self.bot = OpenAI(base_url="http://127.0.0.1:1234/v1/", api_key="1234")
        self.history = []
        self.history.append(
            {
                "role": "system",
                "content": system_prompt
            }
        )


    def generate_response(self, message):
        self.history.append({
            "role": "user",
            "content": message
        })
        stream = self.bot.chat.completions.create(
            model="",
            messages=self.history,
            stream=True
        )
        response = ""
        for chunk in stream:
            response += chunk.choices[0].delta.content or ''
            print(chunk.choices[0].delta.content, end="")
        self.history.append(
            {
                "role": "assistant",
                "content": response
            }
        )
    
    def update_prompt(self, prompt):
        self.history.append(prompt)

def create_prompt_format(content="", role=""):
    if (role==""):
        role = "system"
    
    return {
        "role": role,
        "content": content
    }

def scrape_content(url):
    response = requests.get(url)
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    page_text = soup.get_text(strip=True)
    return page_text



if __name__ == "__main__":
    page_content = scrape_content("https://github.com/algorithmicsuperintelligence/optillm")
    chatbot = ChatBot(system_prompt)
    prompt = create_prompt_format(f"Here is a page rememeber it, I will ask about it {page_content[:1000]}", "user")
    chatbot.update_prompt(prompt)
    while(True):
        print('\n')
        message = input("input: ")
        chatbot.generate_response(message)