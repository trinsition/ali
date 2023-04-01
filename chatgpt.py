def generate_response(lang_chain, conversation):
    input_text = " ".join(conversation)
    response = lang_chain.run(input_text)
    return response
