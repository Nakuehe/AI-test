import openai
import re

# Hàm loại bỏ emoji
def remove_emoji(text):
    return re.sub(r'[^\x00-\x7F]+', '', text)

# Khởi tạo client kết nối đến Ollama
client = openai.OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Với Ollama, khóa API thường là giả, chỉ cần không rỗng
)

# Lịch sử hội thoại để giữ ngữ cảnh
message_history = []

while True:
    try:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            break

        # Loại bỏ emoji
        cleaned_input = remove_emoji(user_input)

        # Thêm vào lịch sử
        message_history.append({"role": "user", "content": cleaned_input})

        # Gửi yêu cầu đến mô hình
        response = client.chat.completions.create(
            model="gemma2:9b",
            stream=True,
            messages=message_history
        )

        print("AI: ", end="", flush=True)
        bot_reply = ""

        for chunk in response:
            content = chunk.choices[0].delta.content or ""
            bot_reply += content
            print(content, end="", flush=True)
        print()

        # Thêm phản hồi AI vào lịch sử
        message_history.append({"role": "assistant", "content": bot_reply})

    except Exception as e:
        print(f"\n[Error]: {e}")
        continue
