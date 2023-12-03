
# %%
from langchain.text_splitter import RecursiveCharacterTextSplitter

# %%
with open('../san_francisco-ca-1.txt', encoding='latin-1') as f:
    planning_code = f.read()

# %%
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 50,
    length_function = len,
    add_start_index = True,
)

# %%
chunks = splitter.create_documents([planning_code])
len(chunks)

# %%
openai_key = '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'
import openai
from langchain.embeddings import OpenAIEmbeddings
embeddings_model = OpenAIEmbeddings(api_key=openai_key)

# %%
chunk_embeddings = embeddings_model.embed_documents([c['page_content'] for c in chunks])







query = "Show me changes to building height limits in 2022"

documents = db.similarity_search(query)

full_prompt = f'''
These are pieces of the SF planning code. Cite them when answering the user's question:

{(chr(10) + chr(10)).join([d.page_content for d in documents])}
'''

print(full_prompt)

response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": full_prompt},
    {"role": "user", "content": query},
  ]
)
response.choices[0].message.content