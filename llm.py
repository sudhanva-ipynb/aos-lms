from Config.decorators import any_access_token_required
from Importers.common_imports import *
from protos import Lms_pb2,Lms_pb2_grpc
from Importers.common_methods import *

MODEL_PATH = "./Model/Phi-3-Context-Obedient-RAG-Q4_K_M.gguf"


# Helper functions for formatting messages
def format_chat_template(messages):
    """Format the chat history into the model's input template."""
    formatted_input = ""
    for message in messages:
        if message['role'] == 'user':
            formatted_input += "<|user|>\n" + message['content'] + "\n<|end|>\n<|assistant|>\n"
        elif message['role'] == 'assistant':
            formatted_input += message['content'] + "\n<|end|>\n"
    return formatted_input


def construct_message(role, content):
    """Create a message dictionary."""
    return {"role": role, "content": content}


class ModelPipeline:
    def __init__(self, model, context_limit=1):


        self.system = [
            construct_message("user",
                              "You are a virtual assistant capable of only answering questions related to Science and Technology. If the question is unrelated, reply in denial."),
            construct_message("user", "What is an Operating System?"),
            construct_message("assistant",
                              "An operating system is software that enables applications to interact with a computer's hardware.")
        ]
        self.context = []
        self.model = model
        self.context_limit = context_limit

    def add_message(self, message):
        user_message = construct_message("user", message)

        current_context = self.system + self.context[
                                        -(self.context_limit * 2):]
        current_context.append(user_message)

        model_input = format_chat_template(current_context)
        output = self.model(model_input, max_tokens=80, top_p=0.5, temperature=0.6)
        output_text = output['choices'][0].get("text", "").strip()
        lines = output_text.split("\n")
        output_text = "".join(lines)
        assistant_message = construct_message("assistant", output_text)
        self.context.append(user_message)
        self.context.append(assistant_message)

        return output_text





class LlmService(Lms_pb2_grpc.LlmServicer):
    @any_access_token_required
    def askLlm(self, request_iterator, context,**kwargs):
        chat_pipeline = Chat()
        for request in request_iterator:
            yield Lms_pb2.AskLlmResponse(reply=chat_pipeline.add_message(request.query),code = "200")


def Chat():
    pipeline = ModelPipeline(model)

    return pipeline

def serve():
    port = "50050"
    _server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))

    Lms_pb2_grpc.add_LlmServicer_to_server(LlmService(), _server)
    _server.add_insecure_port("[::]:" + port)
    _server.start()
    print("Server started, listening on " + port)
    _server.wait_for_termination()

if __name__ == '__main__':
    model = Llama(model_path=MODEL_PATH, verbose=False, use_mlock=True, device="cuda")

    serve()