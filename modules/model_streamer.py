import json
import requests

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
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_img}"
                            }
                        }
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

        payload = {
            "model": "qwen2.5vl:3b",
            "messages": messages,
            "stream": True,
            "options": {
                "num_predict": 200,
                "temperature": 0.6,
                "top_p": 0.9
            }
        }

        with requests.post(
            "http://localhost:11434/api/chat",
            json=payload,
            stream=True,
            timeout=None
        ) as r:

            for line in r.iter_lines(decode_unicode=True):
                if not line:
                    continue

                chunk = json.loads(line)

                text = chunk.get("message", {}).get("content", "")

                if text:
                    yield f"data: {text}\n\n"

                if chunk.get("done"):
                    break

            yield "data: [DONE]\n\n"

    except Exception as e:
        yield f"data: [Stream error: {e}]\n\n"
        yield "data: [DONE]\n\n"
