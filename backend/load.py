import string
from bs4 import BeautifulSoup
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain_core.documents import Document


def preprocess_html(html_content: str):
    soup = BeautifulSoup(html_content, "html.parser")

    # Remove all CSS style attributes
    for tag in soup.recursiveChildGenerator():
        if hasattr(tag, "attrs"):
            tag.attrs = {
                key: value for key, value in tag.attrs.items() if key != "style"
            }

    # Remove all CSS class attributes
    for tag in soup.find_all(True, {"class": True}):
        if tag.name == "div" and "ChapAn" in tag.get("class", []):
            continue  # Skip this tag if it's a <div> with class "ChapAn"
        del tag["class"]

    # Find and remove all AnnotationDrawer elements
    for tag in soup.find_all("annotationdrawer"):
        tag.decompose()

    return str(soup)


def chunk_legal_document(text: str):
    """This works for the planning code and Senate Bills like SB 423 and SB 330."""
    # Structure of planning code
    little_letters = ["(" + l + ")" for l in string.ascii_lowercase]
    numbered_sections = ["(" + str(d) + ")" for d in range(100)]
    big_letters = ["(" + l + ")" for l in string.ascii_uppercase]

    splitter = RecursiveCharacterTextSplitter(
        ["SEC"]
        + little_letters
        + numbered_sections
        + big_letters
        + ["\n\n", "\n", " "],
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
        add_start_index=False,
    )

    chunks = splitter.create_documents([text])
    return chunks


def chunk_planning_html(text: str):
    cleaned = preprocess_html(text)
    return chunk_legal_document(cleaned)


def chunk_generic_document(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
        add_start_index=True,
    )

    chunks = splitter.create_documents([text])
    return chunks


def chunk_nonplanning_document(text: str):
    soup = BeautifulSoup(text, "html.parser")

    # Remove all CSS style attributes
    for tag in soup.recursiveChildGenerator():
        if hasattr(tag, "attrs"):
            tag.attrs = {
                key: value for key, value in tag.attrs.items() if key != "style"
            }

    # Remove all CSS class attributes
    for tag in soup.find_all(True, {"class": True}):
        if tag.name == "div" and "ChapAn" in tag.get("class", []):
            continue  # Skip this tag if it's a <div> with class "ChapAn"
        del tag["class"]

    # Find and remove all AnnotationDrawer elements
    for tag in soup.find_all("annotationdrawer"):
        tag.decompose()

    # Structure of planning code
    little_letters = ["(" + l + ")" for l in string.ascii_lowercase]
    numbered_sections = ["(" + str(d) + ")" for d in range(100)]

    splitter = RecursiveCharacterTextSplitter(
        ["SEC"] + little_letters + numbered_sections + ["\n\n", "\n", " "],
        chunk_overlap=100,
        length_function=len,
        add_start_index=False,
    )

    chunks = splitter.create_documents([str(soup)])
    return chunks


def get_chunks(document_filenames: List[str]):
    chunks = []
    for doc in document_filenames:
        chunks.extend(load_document_with_beautifulsoup(doc))

    return chunks


# def init_db_from_documents(
#     document_filenames: List[str], embeddings_model: OpenAIEmbeddings
# ):
#     chunks = []
#     for doc in document_filenames:
#         chunks.extend(load_document_with_beautifulsoup(doc))

#     # db = Chroma.from_documents(
#     #     chunks, embeddings_model, persist_directory="./chroma_db"
#     # )

#     return db


def load_document_with_beautifulsoup(filepath: str):
    with open(filepath, encoding="latin-1") as f:
        planning_code = f.read()

    soup = BeautifulSoup(planning_code)
    section_chunks = []
    for c in list(soup.body.children):
        if c.name == "div" and c.codeoptions:
            section_text = ""
            if section := c.find_previous(class_="Section"):
                section_text = section.get_text()
            section_chunks.append(
                Document(
                    page_content=c.get_text(),
                    metadata={
                        "section": section_text,
                        "rid": str(c.codeoptions["destid"]).split("-", 1)[1],
                    },
                )
            )

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    final_chunks = splitter.create_documents(
        [c.page_content for c in section_chunks], [c.metadata for c in section_chunks]
    )
    final_chunks = [
        # we want the section name included in embeddings
        Document(
            page_content=c.metadata["section"] + "\n" + c.page_content,
            metadata=c.metadata,
        )
        for c in final_chunks
    ]

    return final_chunks


def load_document(filepath: str):
    with open(filepath, encoding="latin-1") as f:
        planning_code = f.read()

    if filepath.endswith("html"):
        planning_code = preprocess_html(planning_code)

    # if ('sb' in filepath and 'txt' in filepath) or 'san_francisco-ca' in filepath:
    #    chunks = chunk_legal_document(planning_code)

    # else:

    chunks = chunk_generic_document(planning_code)
    return chunks
