import streamlit as st
import pandas as pd
from txtai.embeddings import Embeddings
import gdown
import os

st.write("test")
#
# def download_files():
#     documents_file = "https://drive.google.com/file/d/1qvHCmLFW9z3QJQpUvINsfdVEufTEaKUv/view?usp=sharing"
#
#     if os.path.exists("./models/annual_reports/documents"):
#         pass
#     else:
#         output = "./models/annual_reports/documents"
#         gdown.download(documents_file, output, quiet=False, fuzzy=True)
#         print("Download Complete")
#
#     embeddings_file = "https://drive.google.com/file/d/1ZrLR_e6u4AotBtNGllC7k49IbI94y7dG/view?usp=sharing"
#     if os.path.exists("./models/annual_reports/embeddings"):
#         pass
#     else:
#         output = "./models/annual_reports/embeddings"
#         gdown.download(embeddings_file, output, quiet=False, fuzzy=True)
#         print("Download Complete")
#
# download_files()
#
#
# @st.cache(allow_output_mutation=True)
# def load_txtai():
#     embeddings = Embeddings({"path": "sentence-transformers/all-MiniLM-L6-v2", "content": True})
#     embeddings.load("models/annual_reports")
#     return embeddings
#
# st.title("Smithsonian Annual Reports")
# st.sidebar.image("images/logo.png")
# with open ("markdown/description.md", "r") as f:
#     description = f.read()
# st.sidebar.markdown(description, unsafe_allow_html=True)
# query = st.sidebar.text_input("Query")
# num_results = st.sidebar.number_input("Number of Results", 1, 2000, 20)
#
# embeddings = load_txtai()
#
#
# def create_html(result):
#     output = f""
#     spans = []
#     for token, score in result["tokens"]:
#         color = None
#         if score >= 0.1:
#             color = "#fdd835"
#         elif score >= 0.075:
#             color = "#ffeb3b"
#         elif score >= 0.05:
#             color = "#ffee58"
#         elif score >= 0.025:
#             color = "#fff59d"
#
#         spans.append((token, score, color))
#
#     if result["score"] >= 0.05 and not [color for _, _, color in spans if color]:
#         mscore = max([score for _, score, _ in spans])
#         spans = [(token, score, "#fff59d" if score == mscore else color) for token, score, color in spans]
#
#     for token, _, color in spans:
#         if color:
#             output += f"<span style='background-color: {color}'>{token}</span> "
#         else:
#             output += f"{token} "
#     return output
#
#
# if st.sidebar.button("Search"):
#     res = embeddings.explain(query, limit = num_results)
#
#     html_txt = [create_html(r) for r in res]
#     indices = [index['id'] for index in res]
#
#     scores = [index['score'] for index in res]
#     texts = [index['text'] for index in res]
#     data = {
#             "index": indices,
#             "similarity": scores,
#             "text": html_txt
#     }
#     df = pd.DataFrame(data)
#
#     st.markdown(df.to_markdown(), unsafe_allow_html=True)
