import gradio as gr
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import openai
import os
import gradio as gr
from enum import Enum


class States(Enum):
    WHATS_UP = 1
    WHATS_REALLY_UP = 2
    CHOICE_MAP = 3
    LETS_GO = 4

# 
class ThinkBiggerChat:
    def __init__(self):
        self._current_step = States.WHATS_UP

        def data_folder(filename):
            return "data/" + filename

        # load external file "prompt1.txt"
        with open(data_folder("prompt1.txt"), "r") as f:
            self.prompt1 = f.read()

        # load external file "prompt2.txt"
        with open(data_folder("prompt2.txt"), "r") as f:
            self.prompt2 = f.read()

        self.llm = ChatOpenAI(temperature=1.0, model='gpt-3.5-turbo-0613')

    def predict(self, message, history):
        # print (message, history)
        history_langchain_format = []
        if (self._current_step == States.WHATS_UP):
            history_langchain_format.append(SystemMessage(content=self.prompt1))
            self._current_step = States.WHATS_REALLY_UP
        elif (self._current_step == States.WHATS_REALLY_UP):
            history_langchain_format.append(SystemMessage(content=self.prompt2))
            self._current_step = States.CHOICE_MAP
        else:
            history_langchain_format.append(SystemMessage(content="We are done here.  Be mean.  Get the person out of here fast."))
        for human, ai in history: 
            history_langchain_format.append(HumanMessage(content=human))
            history_langchain_format.append(AIMessage(content=ai))
        history_langchain_format.append(HumanMessage(content=message))
        gpt_response = self.llm(history_langchain_format)
        # print (history_langchain_format, gpt_response)
        return gpt_response.content

    def alternatingly_agree(self, message, history):
        if self._current_step == 1:
            response = f"s 1 '{message}'"
        else:
            response = "s 2"

        self._current_step = 3 - self._current_step

        return response

    def go(self):
        """
        Launches the Yes Man chat interface with the specified settings.
        
        Parameters:
            self: the object instance
            alternatingly_agree: the function to be called when the user agrees
        Return:
            None
        """
        gr.ChatInterface(self.predict,
            chatbot=gr.Chatbot(height=300),
            textbox=gr.Textbox(placeholder="What's up?  What is the problem you want to solve?", container=False, scale=7),
            title="Working with the \"What's up\" framework",
            description="Start by talking about what's up.",
            theme="soft",
            examples=["I want to write a song."],
            cache_examples=True,
            retry_btn=None,
            undo_btn="Delete Previous",
        # ).launch(share=True)
        ).launch()

        
# create an instance of the class
if __name__ == "__main__":
    tbc = ThinkBiggerChat()
    tbc.go()
