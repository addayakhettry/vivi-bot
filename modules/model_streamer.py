import ollama

def stream_response(user_msg, encoded_img=None):
    try:
        prompt = user_msg.strip() if user_msg else "Hello"

        # ✅ If image exists, use multimodal format
        if encoded_img:
            messages = [
                {
                    "role": "system",
                    "content": "You are Vivi Bot. Reply in short, clear, friendly sentences."
                },
                {
                    "role": "user",
                    "content": prompt,
                    "images" : [
                        f"{encoded_img}",
                    ]
                }
            ]
        else:
            messages = [
                {
                    "role": "system",
                    "content": "You are Vivi Bot. Reply in short, clear, friendly sentences. Avoid long paragraphs."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]

        stream = ollama.chat(
            model="qwen2.5vl:3b",
            messages=messages,
            think=False,
            stream=True,
            options={
                "num_predict": 200,
                "temperature": 0.6,
                "top_p": 0.9,
                "num_ctx": 2 ** 16,
            },
        )

        for chunk in stream:
            if chunk.message.content:
                yield f"data: {chunk.message.content}\n\n"

        yield "data: [DONE]\n\n"

    except Exception as e:
        yield f"data: [Stream error: {e}]\n\n"
        yield "data: [DONE]\n\n"
