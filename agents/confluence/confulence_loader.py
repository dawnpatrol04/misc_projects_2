from langchain_community.document_loaders import ConfluenceLoader
import os
from dotenv import load_dotenv , find_dotenv


def confluence_load(space_key='DevOpsWiki'):
    load_dotenv(find_dotenv())
    CONFLUENCE_TOKEN = os.getenv("CONFLUENCE_TOKEN") # xoxb
    CONFLUENCE_URL = os.getenv("CONFLUENCE_URL") # xapp

    loader = ConfluenceLoader(
        url= CONFLUENCE_URL,
        token= CONFLUENCE_TOKEN,
        space_key=space_key,
        include_attachments=False,
        include_comments=False,
    )

    documents = loader.load()
    # save documents to csv file
    with open("all_documents.txt", "w") as f:
        for document in documents:
            f.write(f"{document}\n")


if __name__ == "__main__":
    confluence_load()