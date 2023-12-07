# %%

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 
import plotly.express as px
import re

import streamlit as st 

ISH = pd.read_csv('CleanData/ISH_summary.csv', index_col=0)
BOM = pd.read_csv('CleanData/BOM_summary.csv', index_col=0)
cr_chapter = pd.read_csv('CleanData/by_chapter_cross_ref.csv', index_col=0)
cr_verse = pd.read_csv('CleanData/by_verse_cross_ref.csv', index_col=0)

# %%

st.title("Exploring Isaiah's Legacy in the Book of Mormon")

# Introduction
st.header("Introduction")
st.markdown("This Streamlit Dashboard aims to provide an interactive element in discovering the connections between the Biblical prophet Isaiah and the Book of Mormon authors. Scholars regularly debate betwen linguistic and historical contexts regarding the Book of Mormon's usage of Isaiah. Use this dashboard to visualize the connections and comprehend the dilemma.")
st.markdown("""There are a few key words that need explanation before you dive in:
- The ***Duhms category*** refers to the section of Isaiah as ascribed by Bernhard Duhm. Proto-Isaiah refers to chapters 1-39 (742-687 BCE, from Isaiah's call to prophethood to a century before the Babylonian exile), Deutero-Isaiah refers to chapters 40-55 (597-538 BCE, allegedly written during King Cyrus conquest of Babylon), and Trito-Isaiah refers to chapters 56-66 (after 538 BCE, after the Jews returned to Jerusalem). The Book of Mormon peoples left Jerusalem after 597 BCE, and therefore would only have Proto-Isaiah in their records.
- ***Similarity score*** is the language similarities between verses (calculated from python package textdistance.cosine), between 0 and 1. A detailed description on how calculating text similarities work can be found [here](https://www.newscatcherapi.com/blog/ultimate-guide-to-text-similarity-with-python).
- ***Reference type*** is a categorized version of similarity score. The type of reference denoted between verses is determined by how similar verses are. Similarity scores between .75 and 1 were considered \"Direct Quote\", .25 to .75 had \"Shared Language\", and 0 to .25 had \"Similar Themes\". This process is based on subjective inference and do not reflect scholarly standards.
- ***Bible Term Verses*** identify if the verse contains an [LDS Bible Dictionary Term]("https://www.churchofjesuschrist.org/study/scriptures/bd?lang=eng").
            """)

# %%
st.header("Cross Reference Interactive Investigation")

st.markdown("""
Use the following sections to determine the book (e.g. Isaiah, 1 Nephi, Alma), the chapter number, and associated verses to analyze information and compare texts. You will need to select a book author first, then a chapter, then the verses.
            """)
st.markdown("""
Here are some of my suggestions for exploring:
* Isaiah 7:14 &rarr; 2 Nephi 17:14
* Isaiah 9:6 &rarr; Mosiah 15:2
* Isaiah 52:7 &rarr; Mosiah 15:14-17
* 1 Nephi 20-21 &rarr; Isaiah 48-49
* 2 Nephi 7-8 &rarr; Isaiah 50-52
* 2 Nephi 12-24 &rarr; Isaiah 2-14
            """)

st.subheader("Book Data")

# custom palatte mapping from SET2 in seaborn
pal = sns.color_palette('Set2').as_hex()
colors = [pal[i] for i in range(5)]

# Select Book
select_book = st.selectbox('Select an author', pd.Series(['Isaiah']).append(pd.Series((BOM['book_title_BOM'].unique()))))

# Bar Data for Entire Book
if select_book == "Isaiah":
    count_ref = pd.melt(ISH, id_vars= ['chapter_number_ISH', 'Duhms_Class', 'verse_count_ISH'],
                        value_vars=['Direct Quote', 'Shared Language', 'Similar Theme'], 
                        var_name='Ref_Type', value_name='Ref_Count')
    book_ch_nums = count_ref['chapter_number_ISH']
else:
    count_ref = pd.melt(BOM[BOM['book_title_BOM'] == select_book], id_vars= ['book_title_BOM', 'chapter_number_BOM', 'verse_count_BOM'],
                        value_vars=['Direct Quote', 'Shared Language', 'Similar Theme'], 
                        var_name='Ref_Type', value_name='Ref_Count')
    book_ch_nums = count_ref['chapter_number_BOM']

# custom colors for book bars
color_mapping={
        'Direct Quote': colors[0],
        'Shared Language': colors[1],
        'Similar Theme': colors[2],
    }

# Generate book bar chart
bar = px.bar(data_frame=count_ref, x=book_ch_nums, y='Ref_Count', color = 'Ref_Type', title=f"Reference Counts in {select_book}", color_discrete_map=color_mapping)
bar.update_layout(xaxis_title='Chapter', yaxis_title = 'Count', legend_title = None)

hovertemplate = '<b>Count:</b> %{y}</b><br><b>Chapter Number: </b> %{x}'

bar.update_traces(
    hovertemplate=hovertemplate,
)

st.plotly_chart(bar)

# %%

st.subheader("Chapter Data")

# Select Isaiah Chapter
if select_book == "Isaiah":
    select_chapter_number = st.selectbox('Select a chapter', ISH['combo_ISH'].unique())

    # Create bar data
    ch_data = ISH[ISH['combo_ISH'] == select_chapter_number].rename({'bible_term_in_ISH': "Bible Term Verses", 'verse_count_ISH': "Verse Count"}, axis=1).melt(
        id_vars=['combo_ISH', 'chapter_number_ISH'],
        value_vars=['Direct Quote', 'Shared Language', 'Similar Theme', 'Bible Term Verses', 'Verse Count'],
        var_name='Type', value_name='Count')

# Select BOM Chapter
else: 
    select_chapter_number = st.selectbox('Select a chapter', BOM[BOM['book_title_BOM'] == select_book]['combo_BOM'].unique())

    # Create bar data
    ch_data = BOM[BOM['combo_BOM'] == select_chapter_number].rename({'bible_term_in_BOM': "Bible Term Verses", 'verse_count_BOM': "Verse Count"}, axis=1).melt(
        id_vars=['combo_BOM', 'chapter_number_BOM'],
        value_vars=['Direct Quote', 'Shared Language', 'Similar Theme', 'Bible Term Verses', 'Verse Count'],
        var_name='Type', value_name='Count')

# Custom colors for chapter bars
color_mapping_ch={
        'Direct Quote': colors[0],
        'Shared Language': colors[1],
        'Similar Theme': colors[2],
        'Bible Term Verses': colors[3],
        'Verse Count': colors[4]
    }

# Generate bar data
bar_ch = px.bar(data_frame=ch_data, x='Type', y='Count', color = 'Type', title=f"Summary of {select_chapter_number}", color_discrete_map=color_mapping_ch)
bar_ch.update_layout(xaxis_title=None, legend_title = None)

hovertemplate = '<b>Count:</b> %{y}<b>'

bar_ch.update_traces(
    hovertemplate=hovertemplate,
)

st.plotly_chart(bar_ch)

# Table data
ch_num = int(re.findall(r'\d+', select_chapter_number)[-1])

if select_book == "Isaiah":
    cr_ch = cr_verse[cr_verse['chapter_number_ISH'] == ch_num]
    DQ = cr_ch[cr_ch['similarity_category'] == "Direct Quote"]['verse_title_BOM'].reset_index(drop=True)
    SL = cr_ch[cr_ch['similarity_category'] == "Shared Language"]['verse_title_BOM'].reset_index(drop=True)
    ST = cr_ch[cr_ch['similarity_category'] == "Similar Theme"]['verse_title_BOM'].reset_index(drop=True)
    BT = cr_ch[cr_ch['bible_term_in_ISH'] == True].sort_values('verse_number_ISH')['verse_title_ISH'].drop_duplicates().reset_index(drop=True)

    ch_tb = pd.concat([DQ, SL, ST, BT], axis=1).reset_index(drop=True).fillna('-')
    ch_tb.columns = ['Direct Quote', 'Shared Language', 'Similar Theme', 'Bible Term Verses']


else:
    cr_ch = cr_verse[(cr_verse['chapter_number_BOM'] == ch_num) & (cr_verse['book_title_BOM'] == select_book)]
    DQ = cr_ch[cr_ch['similarity_category'] == "Direct Quote"]['verse_title_ISH'].reset_index(drop=True)
    SL = cr_ch[cr_ch['similarity_category'] == "Shared Language"]['verse_title_ISH'].reset_index(drop=True)
    ST = cr_ch[cr_ch['similarity_category'] == "Similar Theme"]['verse_title_ISH'].reset_index(drop=True)
    BT = cr_ch[cr_ch['bible_term_in_BOM'] == True].sort_values('verse_number_BOM')['verse_title_BOM'].drop_duplicates().reset_index(drop=True)

    ch_tb = pd.concat([DQ, SL, ST, BT], axis=1).reset_index(drop=True).fillna('-')
    ch_tb.columns = ['Direct Quote', 'Shared Language', 'Similar Theme', 'Bible Term Verses']

# st.markdown(ch_tb.style.hide(axis="index").to_html(), unsafe_allow_html=True)
st.dataframe(ch_tb, hide_index = True, height = 200, width = 1000)

# %%

# Verse comparison
st.subheader("Verse Text Comparison")

# Data Prep 
if select_book == "Isaiah":
    start_verse_df = cr_verse[cr_verse['chapter_number_ISH'] == ch_num].dropna(subset=['verse_title_ISH', 'verse_title_BOM'])
    end_verse_df = cr_verse.dropna(subset=['verse_title_BOM'])
    select_start_verse = st.selectbox(f'Select a verse from {select_chapter_number}', start_verse_df['verse_title_ISH'].unique())
    select_end_verse = st.selectbox('Select a verse from the Book of Mormon to compare', end_verse_df[end_verse_df['verse_title_ISH'] == select_start_verse]['verse_title_BOM'].unique())
    verse_tb = cr_verse[(cr_verse['verse_title_ISH'] == select_start_verse) & (cr_verse['verse_title_BOM'] == select_end_verse)][['scripture_text_ISH', 'scripture_text_BOM', 'similarity_score', 'similarity_category', 'Duhms_Class']]

else: 
    start_verse_df = cr_verse[(cr_verse['chapter_number_BOM'] == ch_num) & (cr_verse['book_title_BOM'] == select_book)].dropna(subset=['verse_title_BOM', 'verse_title_ISH'])
    end_verse_df = cr_verse.dropna(subset=['verse_title_ISH'])
    select_start_verse = st.selectbox(f'Select a verse from {select_chapter_number}', start_verse_df.sort_values('verse_number_BOM')['verse_title_BOM'].unique())
    select_end_verse = st.selectbox('Select a verse from Isaiah to compare', end_verse_df[end_verse_df['verse_title_BOM'] == select_start_verse]['verse_title_ISH'].unique())
    verse_tb = cr_verse[(cr_verse['verse_title_BOM'] == select_start_verse) & (cr_verse['verse_title_ISH'] == select_end_verse)][['scripture_text_BOM', 'scripture_text_ISH', 'similarity_score', 'similarity_category', 'Duhms_Class']]

verse_tb.columns = [select_start_verse, select_end_verse, 'Similarity Score', 'Similarity Category', "Duhm's Category"]
verse_tb['Similarity Score'] = round(verse_tb['Similarity Score'], ndigits = 4)

if verse_tb.empty:
    st.markdown("<p style='text-align: center; color: white;'>No cross references found </p>", unsafe_allow_html=True)
else: 
    st.markdown(verse_tb.style.hide(axis="index").to_html(), unsafe_allow_html=True)

st.markdown("""
            [Back to top](#cross-reference-interactive-investigation)
            """)

# %%

st.header("Conclusion")

st.markdown("""
            This dashboard aimed to provide an interactive experience whereby the casual learner or the scriptural expert can dive into the textual comparisons between Isaiah and the Book of Mormon. Structuring the vast question about the authenticity of the Book of Mormon in regards to Isaiah's writings within this dashboard will provide an interactive and meaningful experience to those wanting to learn more about the topic and the scriptures.   
            """)

# %%

repo_url = 'https://github.com/jxnpass/Isaiah-to-BoM/tree/main'
blog_url = 'https://jxnpass.github.io/2023/12/06/IsaiahToBOM-EDA.html'

url1 = "https://www.streamlit.io"
url2 = "https://medium.com/swlh/analyzing-references-in-bibles-verses-using-complex-networks-with-pandas-and-gephi-8a4edc52e7ab"
url3 = "https://scriptures.nephi.org/"
url4 = "http://www.creationismonline.com/Mormons/Mormons.html"
url5 = "https://www.churchofjesuschrist.org/study/scriptures/bd?lang=eng"

st.header("Links")
st.subheader("Project")
st.write("[GitHub Repository](%s)" % repo_url)
st.write("[Blog Link](%s)" % blog_url)

st.subheader("Credit")
st.write("Inspiration: [OpenBible.info](%s)" % url1)
st.write("Inspiration: [Medium](%s)" % url2)
st.write("Verse Data: [LDS Documentation Project](%s)" % url3)
st.write("Cross Reference Data: [Linguistics Study in the Book of Mormon](%s)" % url4)
st.write("Bible Dictionary Data: [Church of Jesus Christ](%s)" % url5)