from flask import Flask, request, render_template, Response, stream_with_context
from modules.document_handler import extract_text
from modules.image_handler import encode_image
from modules.model_streamer import stream_response

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/stream', methods=['POST'])
def stream():
    print("\n================ NEW REQUEST ================")
    print("[DEBUG] request.form:", request.form)
    print("[DEBUG] request.files:", request.files)

    user_msg = request.form.get("message", "")
    user_img = request.files.get("image")
    user_doc = request.files.get("document")

    encoded_img = None

    # IMAGE HANDLING
    if user_img:
        try:
            print("[📸 Image received]", user_img.filename, user_img.content_type)
            encoded_img = encode_image(user_img)

            if encoded_img:
                print("[✅ Image encoded]")
                print("[📏 Base64 size]", len(encoded_img))
            else:
                print("[❌ Image encoding failed]")

        except Exception as e:
            print(f"[❌ Image read error] {e}")

    else:
        print("[⚠️ No image received]")

    # DOCUMENT HANDLING
    if user_doc:
        try:
            print("[📄 Document received]", user_doc.filename)
            doc_text = extract_text(user_doc)
            print("[✅ Document extracted length]", len(doc_text))

            user_msg += "\n\nDOCUMENT CONTENT:\n" + doc_text

        except Exception as e:
            print(f"[❌ Document error] {e}")

    return Response(
        stream_with_context(stream_response(user_msg, encoded_img)),
        mimetype="text/event-stream"
    )

if __name__ == '__main__':
    app.run(debug=True, threaded=True)

