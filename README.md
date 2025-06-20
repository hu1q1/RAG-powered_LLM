## Problem Statement
In the internet age, information is an abundant resource. In order to make full use of the privilege of having a huge supply of text data, we enlist the help of AI. AI's capability of going through a large amount of data in a short span of time complements the enormous datasets that we have available and what's left to do is for AI to 'understand' our natural language, do some analysEs and return a condensed version of information that our human brains with relatively lower computing power can comprehend easily.


## Project Goal
In creating an RAG-powered LLM, the hope is that it can be used for general purposes, wherever large amounts of textual data needs to be understood and processed. This repo contains pdf files that serve as example inputs. Note that different preprocessing may be required for different files that may have different formats


## Benefits of RAG-powered LLM over today's widely available LLMs like ChatGPT, Gemini, Claude, etc...
1. Confidential data can be used as input without fear of leaking out into the internet
2. More flexibility in customizing any part of the whole workflow, allowing for experimentation (fun! ^-^)


## Workflow
`example_usage.ipynb` uses the custom functions `FUNCTION_single_doc_prep_to_embed.py`, `FUNCTION_embed_n_retrieve.py`, and `FUNCTION_generate_output_text.py` (this one is work in progress)
[as of June2025] currently this workflow is able to take in text input from a .pdf file, split into chunks which have token counts that are within the embedding model's limit, and create embeddings using an embedding model. When prompted with a query, it will embed the query and use similarity search to find the most relevant chunks of input text, outputing the score obtained (range 0-1, 1 being the most similar) as well as the corresponding text chunk. Now would be to get an LLM (either stored on local machine or through API calls) to generate text that have been augmented by the context it is given, to answer the query directly.


## Acknowledgement
Inspiration derived from https://www.youtube.com/watch?v=qN_2fnOPY-M