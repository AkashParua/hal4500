import socket
import os
from dotenv import load_dotenv
from vision_tools import what_am_i_holding
import os
import openai
from langchain.llms import OpenAI 
load_dotenv()
openai.api_key = os.getenv("OPEN_AI_API")

from langchain.agents import initialize_agent
llm = OpenAI(openai_api_key=openai.api_key,temperature=0)

from langchain.agents import AgentType
from langchain.tools import BaseTool
class WhatAmIHolding(BaseTool):
    name = "hand contents"
    description = "useful when you need to answer questions about what is in my hands or what am I holding"
    def _run(self ,query:str ) -> str:
        return what_am_i_holding()

tools = [WhatAmIHolding()]
agent = initialize_agent(
    tools, llm, agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,  verbose=True
)



soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


soc.connect((socket.gethostname(), int(os.getenv("HEARING_PORT"))))
while True:
    data = None
   
    data = soc.recv(1024).decode('utf-8')
    

    if data:
        if data == "exit":
            break

        if data == '--silence--':
            continue
            
        print(f"Human: {data}")
        response = agent.run(data)
        print(f"AI: {response}")


soc.close()