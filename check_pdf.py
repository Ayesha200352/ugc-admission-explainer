from langchain_community.document_loaders import PyPDFLoader
import os


folder = "data/faculty_sections"


for filename in os.listdir(folder):

    if filename.endswith(".pdf"):

        path = os.path.join(folder, filename)

        print("\nChecking:", filename)

        loader = PyPDFLoader(path)

        try:
            docs = loader.load()

            for index, doc in enumerate(docs):

                if doc.page_content is None:
                    print("EMPTY PAGE:", index)

                elif len(doc.page_content.strip()) == 0:
                    print("BLANK PAGE:", index)

            print("Total pages:", len(docs))

        except Exception as e:
            print("ERROR:", e)