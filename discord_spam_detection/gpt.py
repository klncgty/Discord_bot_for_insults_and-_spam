import openai
from langchain.memory import ConversationBufferMemory



class GptService:
    def __init__(self):
        openai.api_key = "gpt_api_key"
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    
    
    def ask_gpt(self, message):
        # Mesajı doğrudan belleğe ekleyelim
        self.memory.chat_memory.messages.append({'role': 'user', 'content': message})

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-vision-preview",
                messages=self.memory.chat_memory.messages + [{"role": "system", "content": "mesaj, küfür ve hakaret içeriyor mu onu kontrol et. eğer mesaj anlam olarak veya kelime içeriği olarak küfür veya hakaret içeriyorsa, cevap olarak sadece tek bir kelime ile, OLUMSUZ diye cevap ver."},
                                                             ],
                max_tokens=900,
                temperature=0,
                n=1,
                frequency_penalty=0.9,
                presence_penalty=0.0
            )
            # Yanıtı belleğe ekleyelim
            self.memory.chat_memory.messages.append(
                {'role': 'system', 'content': response["choices"][0]["message"]["content"]})
            print(response)
            
            answer = response["choices"][0]["message"]["content"]
            return answer
        
        except Exception as e:
                print(e)
                return "Something went wrong..."