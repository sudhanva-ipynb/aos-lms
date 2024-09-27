from Importers.common_imports import *
from Importers.common_methods import *
from Database.methods import *



def format_chat_template(messages):
    formatted_input = ""

    for message in messages:
        if message['role'] == 'user':
            formatted_input += "<|user|>\n" + message['content'] + "\n<|end|>\n<|assistant|>\n"
        elif message['role'] == 'assistant':
            formatted_input += message['content'] + "\n<|end|>\n"

    return formatted_input


def construct_user_message(content):
    return {"role": "user", "content": content}


def construct_assistant_message(content):
    return {"role": "assistant", "content": content}

class ModelPipeline:
    def __init__(self,model):
        self.system = [
        {"role": "user",
         "content": "You are a virtual assistant capable of only answering questions related to Science and Technology if the question is unrelated reply in denial."},
        {"role": "user", "content": "What is an Operating Systems?"},
        {"role": "assistant",
         "content": "An operating system is software that enables applications to interact with a computer's hardware."}
    ]
        self.context = []
        self.model  = model
    def add_message(self, message):
        user_message = construct_user_message(message)
        messages = self.system
        messages.extend(self.context)
        messages.append(user_message)
        output = self.model(format_chat_template(messages), max_tokens=80, top_p=0.5, temperature=0.6)
        output_text = output['choices'][0].get("text", "")
        assistant_message = construct_assistant_message(output_text)
        self.context = [user_message, assistant_message]
        return output_text.split("\n")[0]

model = Llama(model_path="Phi-3-Context-Obedient-RAG-Q4_K_M.gguf",verbose=False,use_mlock=True)
