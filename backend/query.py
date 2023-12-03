

def query_documents(client, db, query):
    documents = db.similarity_search(query)

    full_prompt = f''',
        These are pieces of the SF planning code. Cite them when answering the user's question:,
        {(chr(10) + chr(10)).join([d.page_content for d in documents])},
    '''

    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[
        {"role": "system", "content": full_prompt}, 
        {"role": "user", "content": query},
    ])

    return response.choices[0].message.content