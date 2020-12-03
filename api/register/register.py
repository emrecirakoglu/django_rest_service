from api.Message.messages import RegisterMessage


class RegisterManager:
    def __init__(self):
        pass

    def register_client(self, register_message: RegisterMessage):
        print(register_message.as_json())
        print("Client registered")
