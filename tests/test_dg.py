"""
Create a unit test later.

This prompt
'list all the design guidelines other than the RDG and UDG '

recieves a stack trace that includes this error message:

Traceback (most recent call last):
  File "/Users/Salim/Library/Caches/pypoetry/virtualenvs/housing-lUKQsRGf-py3.11/lib/python3.11/site-packages/langchain/output_parsers/pydantic.py", line 29, in parse
    json_object = json.loads(json_str, strict=False)
                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/Cellar/python@3.11/3.11.5/Frameworks/Python.framework/Versions/3.11/lib/python3.11/json/__init__.py", line 359, in loads
    return cls(**kw).decode(s)
           ^^^^^^^^^^^^^^^^^^^
  File "/usr/local/Cellar/python@3.11/3.11.5/Frameworks/Python.framework/Versions/3.11/lib/python3.11/json/decoder.py", line 337, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/Cellar/python@3.11/3.11.5/Frameworks/Python.framework/Versions/3.11/lib/python3.11/json/decoder.py", line 355, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)

During handling of the above exception, another exception occurred:

[...]
    raise OutputParserException(msg, llm_output=text)


To answer your question accurately, I would need the specific excerpts from the San Francisco planning code that relate to design guidelines, including any that reference the RDG (Residential Design Guidelines) and UDG (Urban Design Guidelines), and any other design guidelines mentioned in the code. Without the actual text or specific references to these documents, I cannot provide a list of all design guidelines. 

If you can provide the excerpts or references to the relevant sections of the San Francisco planning code, I would be able to help further. Once I have the necessary information, I can format the response in the JSON structure as required"


"""
