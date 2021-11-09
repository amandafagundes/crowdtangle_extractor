# About

Script used to collect data from Crowdtangle API

# Project

The collected data is organized into `data` folder as JSON files in the format `{query}_{begin-date}_to_{end-date}` where `query` refers to the query used in the search and `begin-date` and `end-date` are the specified range.

To execute the extractor: `$ python3 src/search.py`