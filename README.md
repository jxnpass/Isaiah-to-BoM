This repository holds the code for my project "Exploring Isaiah's Legacy in the Book of Mormon", which is illustrated in two blogs, one that talks about [data collection](https://jxnpass.github.io/2023/12/05/IsaiahToBOM-DC.html#data-building), and the other about the [EDA](https://jxnpass.github.io/2023/12/06/IsaiahToBOM-EDA.html).

I like to organize my repository and coding into steps. In the folder [Scripts](/Scripts/) there are six different Jupyter notebooks that perform different functions.
[1-scrape_data.ipynb](/Scripts/1-scrape_data.ipynb) 
* scrapes data from three different sources
* cleans and compiles data into csv files in [Dirty Data](/DirtyData/)
[2-combine_data.ipynb](/Scripts/2-combine_data.ipynb)
* takes previous csv files and turns it into a cross reference dataset with verse IDs and scriptural text
* exports into new csv found in [Dirty Data](/DirtyData/)
[3-build_verse_data.ipynb](/Scripts/3-build_verse_data.ipynb)
* main goal is to make the data more comprehensive
* analyze textual similarities
* calculate word counts in verses and verse counts in chapters
* detects biblical terminology in verses
* categorizes textual similarities and Isaiah chapters using Duhm's classifications
* exports into new datasets found in [Clean Data](/CleanData/)
[4-build_chapter_data](/Scripts/4-build_chapter_data.ipynb)
* I do not talk about these steps in the blog, but in simple terms it takes above data and aggerates it by chapter
* exports into new csv files
[5-networks.ipynb](/Scripts/5-networks.ipynb)
* takes chapter and verse cross reference data from [Clean Data](/CleanData/) and generates [chapter](https://jxnpass.github.io/assets/Isaiah-to-BOM/network-visuals/by_chapter.html) and [verse](https://jxnpass.github.io/assets/Isaiah-to-BOM/network-visuals/by_verse.html) networks 
* uses chapter data to provide comprehensive hover node and edge information in chapter network
* uses verse data to provide comprehensive hover node and edge information in verse network
* IMPORTANT: read [the blog](https://jxnpass.github.io/2023/12/06/IsaiahToBOM-EDA.html#cross-reference-networks) before looking at the networks to know what certain illustrations mean
[streamlit-app.py](/streamlit-app.py)
* uses chapter and verse cross reference data and provides interactive element to explore textual similarities and comparisons
* the app can be viewed [here](https://isaiah-to-bom.streamlit.app/)

