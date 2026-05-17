import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

class CustomerSupportBot:
    def __init__(self):
        # API setup
        api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.5-flash"
        
        # Load FAQ data
        self.faq_data = self.load_faq()
        
        # Conversation history
        self.conversations = {}
    
    def load_faq(self):
        """Load FAQ data from file"""
        try:
            with open("data/faq.txt", "r", encoding="utf-8") as f:
                return f.read()
        except:
            return "FAQ data পাওয়া যায়নি।"
    
    def is_bangla_question(self, text: str) -> bool:
        """Check if the question contains Bengali characters"""
        return any("\u0980" <= ch <= "\u09FF" for ch in text)
    
    def get_response(self, user_id: str, question: str) -> str:
        """Answer the user's question"""
        
        # Load conversation history
        if user_id not in self.conversations:
            self.conversations[user_id] = []
        
        history = self.conversations[user_id]
        
        # Determine language
        if self.is_bangla_question(question):
            language_rule = "- বাংলায় উত্তর দাও"
        else:
            language_rule = "- ইংরেজিতে উত্তর দাও"
        
        # Build prompt
        prompt = f"""
তুমি একজন helpful customer support assistant।

📚 আমাদের Company Information:
{self.faq_data}

💬 গ্রাহকের প্রশ্ন: {question}

নিয়ম:
{language_rule}
- সংক্ষিপ্ত ও clear করে বলো
- FAQ তে তথ্য থাকলে সেটা ব্যবহার করো
- না জানলে বলো "এই বিষয়ে আমাদের customer care এ যোগাযোগ করুন: 01700000000"
- সবসময় friendly এবং helpful থাকো
- Emoji ব্যবহার করো যেখানে উপযুক্ত
"""
        
        # Get answer from AI
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )
        
        answer = response.text
        
        # Update history
        history.append({"user": question, "bot": answer})
        if len(history) > 5:  # keep only the last 5
            history.pop(0)
        
        return answer

# For testing
if __name__ == "__main__":
    bot = CustomerSupportBot()
    
    print("🤖 Customer Support Bot started!")
    print("Type 'exit' to quit\n")
    
    user_id = "test_user"
    
    while True:
        question = input("You: ")
        if question.lower() == "exit":
            print("👋 Thank you!")
            break
        
        answer = bot.get_response(user_id, question)
        print(f"\n🤖 Bot: {answer}\n")