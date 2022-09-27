import streamlit as st
import pandas as pd
from txtai.embeddings import Embeddings
import gdown
import os


def download_files():
    model_file = "./models/annual_reports_paras_full_2/"
    documents_file = "https://drive.google.com/file/d/1PSj5v3FjVpfalMM7GZTuWlb3Z-jst6SC/view?usp=sharing"

    if os.path.exists("./models/annual_reports_paras_full_2/documents"):
        pass
    else:
        output = "./models/annual_reports_paras_full_2/documents"
        gdown.download(documents_file, output, quiet=False, fuzzy=True)
        print("Download Complete")

    embeddings_file = "https://drive.google.com/file/d/1tfp9VCMfMoKojTheK8h5oneuvNwW3W_F/view?usp=sharing"


    if os.path.exists("./models/annual_reports_paras_full_2/embeddings"):
        pass
    else:
        output = "./models/annual_reports_paras_full_2/embeddings"
        gdown.download(embeddings_file, output, quiet=False, fuzzy=True)
        print("Download Complete")

    index_file = "https://drive.google.com/file/d/190G9GMVNy4YAIGIxReJOkq_-CZo7BS2S/view?usp=sharing"
    if os.path.exists("./data/annual_reports_paras_full_final.csv"):
        pass
    else:
        output = "./data/annual_reports_paras_full_final.csv"
        gdown.download(index_file, output, quiet=False, fuzzy=True)
        print("Download Complete")

download_files()



@st.cache(allow_output_mutation=True)
def load_index():
    df = pd.read_csv("data/annual_reports_paras_full_final.csv")
    return df

@st.cache(allow_output_mutation=True)
def load_bhl_index():
    df = pd.read_csv("data/filenames_bhl.csv")
    return df

df = load_index()
bhl_df = load_bhl_index()
@st.cache(allow_output_mutation=True)
def load_txtai():
    embeddings = Embeddings({"path": "sentence-transformers/all-MiniLM-L6-v2", "content": True})
    embeddings.load("models/annual_reports_paras_full_2")
    return embeddings
with open ("markdown/description.md", "r") as f:
    description = f.read()
st.sidebar.markdown(description, unsafe_allow_html=True)
st.title("Smithsonian Annual Reports")
st.sidebar.image("images/logo.png")





query = st.sidebar.text_input("Query")
num_results = st.sidebar.number_input("Number of Results", 1, 2000, 20)

search = st.sidebar.button("Search")

st.sidebar.header("Color Selector")
schema = st.sidebar.selectbox("Choose Color Schema",

                                ["Burnt Orange",
                                "Yellows",
                                "Grayscale"]
                                )
if schema == "Burnt Orange":
    high_default = "#7f0000"
    medium_default = "#ef6548"
    low_default = "#fee8c8"
elif schema == "Yellows":
    high_default = "#bfb526"
    medium_default = "#ffeb3b"
    low_default = "#f3f2af"
elif schema == "Grayscale":
    high_default = "#525252"
    medium_default = "#d9d9d9"
    low_default = "#f0f0f0"

col1, col2 = st.sidebar.columns(2)
high_thresh = col1.number_input("High Threshold", 0.0, 0.99, 0.1)
high_thresh_color = col2.color_picker('High Threshold Color', high_default)


col3, col4 = st.sidebar.columns(2)
medium_thresh = col3.number_input("Medium Threshold", 0.0, 0.99, 0.075)
medium_thresh_color = col4.color_picker('Medium Threshold Color', medium_default)

col5, col6 = st.sidebar.columns(2)
low_thresh = col5.number_input("Low Threshold", 0.0, 0.99, 0.05)
low_thresh_color = col6.color_picker('Low Threshold Color', low_default)

embeddings = load_txtai()


def create_html(result, high_thresh, medium_thresh, low_thresh, high_thresh_color, medium_thresh_color, low_thresh_color):
    output = f""
    spans = []
    for token, score in result["tokens"]:
        color = None
        if score >= high_thresh:
            color = high_thresh_color
        elif score >= medium_thresh:
            color = medium_thresh_color
        elif score >= low_thresh:
            color = low_thresh_color


        spans.append((token, score, color))

    if result["score"] >= 0.05 and not [color for _, _, color in spans if color]:
        mscore = max([score for _, score, _ in spans])
        spans = [(token, score, "#fff59d" if score == mscore else color) for token, score, color in spans]

    for token, _, color in spans:
        if color:
            if color == high_thresh_color:
                text_color = "#ffffff"
                output += f"<span style='background-color: {color}; color: {text_color}'>{token}</span> "
            else:
                output += f"<span style='background-color: {color}'>{token}</span> "
        else:
            output += f"{token} "
    return output

def html_pages(page_num, text_file):
    page_data = bhl_df[bhl_df["Archive ID"] == str(text_file)]["BHL Link URL"].tolist()
    if page_data:
        page_data = page_data[0].replace("itempdf", "item")
        return f"<a href='{page_data}#page/{page_num-1}/mode/1up'>Link to PDF</a>"
    else:
        return "Unknown Link"
    # st.write(page_data)
    # https://www.biodiversitylibrary.org/itemp/38165
    # return f"<a href='{page_data}#page/{page_num-1}/mode/1up'>Link to PDF</a>"

if search:
    res = embeddings.explain(query, limit = num_results)
    # st.write(res)
    html_txt = [create_html(r, high_thresh, medium_thresh, low_thresh, high_thresh_color, medium_thresh_color, low_thresh_color) for r in res]
    indices = [index['id'] for index in res]
    years = [df.iloc[int(index)].year for index in indices]
    pages = [df.iloc[int(index)].page_num for index in indices]
    text_files = [df.iloc[int(index)].text_file for index in indices]
    st.write(f"{len(pages)} {len(years)}")
    pages = [html_pages(page, text_file) for page, text_file in zip(pages, text_files)]
    scores = [index['score'] for index in res]
    texts = [index['text'] for index in res]
    data = {
            # "index": indices,
            "year": years,
            "page_num": pages,
            "similarity": scores,
            "text": html_txt
    }
    res_df = pd.DataFrame(data)

    st.markdown(res_df.to_markdown(), unsafe_allow_html=True)
