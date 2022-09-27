# About
This application was developed by [the Smithsonian's Data Science Lab](https://datascience.si.edu/) using [Streamlit](https://www.streamlit.io) and [txtAI](https://github.com/neuml/txtai). The lab developed the application for a forthcoming paper on the role of women in science at the Smithsonian. This paper explores the ways in which women's varied roles at the museum have been masked. This application helps unmask how women appear in the Smithsonian's Annual Reports, a collection of reports published by the Smithsonain each year.

These publications are called either Smithsonian Year or Annual Report of the Board of Regents of the Smithsonian Institution. They contain staff lists, accounts of expeditions and collecting trips, and descriptions of activities across the institution.

Searching for women in the Annual Reports is challenging for several reasons. First, while we improved the quality of the OCR for the reports using Tesseract, errors remain. Second, the annual reports were written over the course of the museum's nearly 150-year history. This means that women infrequently appear in earlier reports. When they do, often their names are masked or attached to the names of their husbands. Third, it can be difficult to securely identify a woman's gender in the annual reports unless a third-person pronoun (she or her) is used in the context of the woman's proper name.

TxtAI and this application resolve some of these issues by vectorizing all paragraphs in the Annual Reports, indexing those paragraphs, and then vectorizing them with a transformer language model. This allows users to write a query (which is subsequently vectorized) and find semantically similar results. In other words, this application does not rely exclusively on keywords to populate results.

A small subset of the Annual Reports are currently used for this beta version of the application. Due to the varied OCR quality of the annual reports, not all text data is available for each report. Only sentences larger than 7 words were indexed.

**Current Version**: 0.0.3

## Version History
### Version 0.0.4
New vectors for ~400k paragraphs from the complete OCR of the annual reports. This new version contains the paragraphs from the corrected OCR output. Added the ability to link to specific page numbers in the PDFs

### Version 0.0.3
Added broader color an threshold selection for users. Color schemas are provided as well. Added support for color-blind viewers.

### Version 0.0.2
Added Support for txtAI's Explain method which allows one to query the index and return a score for each word.

For this version, only a small subset of the Annual Reports are currently used for this beta version of the application. Due to the varied OCR quality of the annual reports, not all text data is available for each report. Only sentences larger than 7 words were indexed.

### Version 0.0.1
Initial Push. App loaded onto Streamlit Share with Basic functionality.
