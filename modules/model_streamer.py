import ollama

def stream_response(user_msg, encoded_img=None):
    try:
        prompt = user_msg.strip() if user_msg else "Hello"

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
            model="granite3.2-vision:2b",
            messages=messages,
            think=False,
            stream=True,
            options={
                "num_predict": 200,
                "temperature": 0.6,
                "top_p": 0.9,
                "num_ctx": 2 ** 8,
            },
        )

        for chunk in stream:
            if chunk.message.content:
                # Make sure the model does not pass any NULLs. This is the
                # stream terminator.
                yield chunk.message.content.replace("\0", "")

    except Exception as e:
        yield f"<p class=\"botError\">[Stream error: {e}]</p>"

    yield "\0"
