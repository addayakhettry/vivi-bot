# Vivi Bot

## Dependencies

- Ollama

    The following models have been tested:
    - `gemma3:4b`
    - `granite3.2-vision:2b`
    - `qwen2.5vl:3b`

    Other models may also work. It is recommended to use vision models.

- Python

    - `flask`
    - `ollama`
    - `pdfplumber`
    - `python-docx`

## Build

1. Install all dependencies using `pip`.
2. Run `ollama` server (using `ollama serve`).
3. Run the application using `python app.py`.
4. Open 
http://127.0.0.1:5000/
 in your browser. 