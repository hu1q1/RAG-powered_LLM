import fitz
# from tqdm.auto import tqdm
import pandas as pd
import textwrap # Define helper function to print wrapped text 

# -----------------------------------------------------------------------#

# PDF_PATH = "Am I Logging the Right AWS Log Sources_.pdf"
# NUM_SENTENCE_CHUNK_SIZE = 7 # define each chunk should contain how many sentences (by trial and error, depending on your specific file contents)
# -----------------------------------------------------------------------#

def single_doc_prep_to_embed(PDF_PATH: str, 
                             NUM_SENTENCE_CHUNK_SIZE: int,
                             DOCUMENT_NAME: str
                             ) -> pd.DataFrame:
    '''
    parameters:

    PDF_PATH: str,
    NUM_SENTENCE_CHUNK_SIZE: int,
    DOCUMENT_NAME: str
    '''
    
    def open_and_read_pdf(pdf_path: str) -> list[dict]:
        doc = fitz.open(pdf_path)  # open a document
        pages_and_texts = []
        # for page_number, page in tqdm(enumerate(doc)):  # iterate the document pages
        for page_number, page in enumerate(doc):  # iterate the document pages

            text = page.get_text()  # get plain text encoded as UTF-8
            text = text.replace("\n", " ").strip()
            pages_and_texts.append({"page_number": page_number + 1,
                                    "page_char_count": len(text),
                                    "page_word_count": len(text.split(" ")),
                                    "page_sentence_count_raw": len(text.split(". ")),
                                    "page_token_count": len(text) / 4,
                                    "text": text})
        return pages_and_texts

    def split_into_chunks(input_list: list, slice_size: int) -> list[list[str]]:
        return [input_list[i : (i + slice_size)] for i in range(0, len(input_list), slice_size)]


    def print_wrapped(text, wrap_length=80):
        wrapped_text = textwrap.fill(text, wrap_length)
        return wrapped_text

    # -----------------------------------------------------------------------#



    pages_and_texts = open_and_read_pdf(pdf_path=PDF_PATH)

    print("First pages's info (including the text): \n")
    print(pages_and_texts[0])
    print(print_wrapped(pages_and_texts[0]["text"]))
    print("\n")
    print("\n")
    print("\n")

    # Loop through pages and texts and split sentences into chunks
    for item in pages_and_texts: # is a list of dictionaries 
        item["sentence_chunks"] = split_into_chunks(input_list=item["text"].split(". "),
                                            slice_size=NUM_SENTENCE_CHUNK_SIZE)
        item["num_chunks"] = len(item["sentence_chunks"])

    print("Summary stats after chunking: \n")
    print(pd.DataFrame(pages_and_texts).describe().round(2))
    print("\n")
    print("\n")
    print("\n")


    # Split each chunk into its own item
    pages_and_chunks = []
    # for item in tqdm(pages_and_texts):
    for item in pages_and_texts:

        for sentence_chunk in item["sentence_chunks"]:
            chunk_dict = {}
            chunk_dict["document_name"] = DOCUMENT_NAME
            chunk_dict["page_number"] = item["page_number"]
            
            # Join the sentences together into a paragraph-like structure, aka a chunk (so they are a single string)
            joined_sentence_chunk = ". ".join(sentence_chunk).strip()
            chunk_dict["sentence_chunk"] = joined_sentence_chunk

            # Get stats about the chunk
            chunk_dict["chunk_char_count"] = len(joined_sentence_chunk)
            chunk_dict["chunk_word_count"] = len([word for word in joined_sentence_chunk.split(" ")])
            chunk_dict["chunk_token_count"] = len(joined_sentence_chunk) / 4 # 1 token = ~4 characters
            
            pages_and_chunks.append(chunk_dict)

    print("Total number of chunks: ")
    print(len(pages_and_chunks))
    print("\n")

    print("First chunk's info: \n")
    print(pages_and_chunks[0])
    print(print_wrapped(pages_and_chunks[0]["sentence_chunk"]))
    print("\n")
    print("\n")
    print("\n")

    print("Summary stats for each chunk: \n")
    print(pd.DataFrame(pages_and_chunks).describe().round(2))


    return pd.DataFrame(pages_and_chunks)