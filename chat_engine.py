import ollama


class ChatEngine:
    print("ChatEngine carregado")
    def __init__(self):
        print("ChatEngine iniciado")
        #segura histórico da conversa
        self.messages = [
            {
                "role": "system",
                "content": (
                    "Você é um assistente amigável, natural e conversacional. "
                    "Responda de forma simples, direta e humana. "
                    "Evite listas longas e explicações técnicas demais, "
                    "a menos que o usuário peça. "
                    "Fale como uma pessoa normal conversando."
                )
            }
        ]

    def ask(self, user_message):
        #add msg do user na box
        self.messages.append(
            {"role": "user", "content": user_message}
        )

        # chama modelo local
        response = ollama.chat(
            model="llama3:8b",
            messages=self.messages
        )

        reply = response["message"]["content"]

        # add resposta n histórico
        self.messages.append(
            {"role": "assistant", "content": reply}
        )

        return reply
    


## Caso o PC for um potato (< 16gb ram), e precisar usar API tá na hand a classe 
#from groq import Groq
#
#
#class ChatEngine:
#    def __init__(self):
#        self.client = Groq(api_key="sua-chave-aqui")
#        self.messages = [
#            {"role": "system", "content": "Você é um assistente amigável..."}
#        ]
#    
#    def ask(self, user_message):
#        self.messages.append({"role": "user", "content": user_message})
#        
#        response = self.client.chat.completions.create(
#            model="llama3-8b-8192",  # Llama 3 via Groq
#            messages=self.messages,
#            temperature=0.7
#        )
#        
#        reply = response.choices[0].message.content
#        self.messages.append({"role": "assistant", "content": reply})
#        return reply