colang_content = """
define user express greeting
    "hello"
    "hi"
define bot express greeting
    "Hello! I am a general physician chatbot. How can I help you today?"
define flow greeting
    user express greeting
    bot express greeting

"""
yaml_content = """
models:
-   type: main
    engine: openai
    model: gpt-3.5-turbo-0125
-   type: embeddings
    engine: openai
    model: text-embedding-3-small
"""
