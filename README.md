# Vietnamese Address Classification

## Overview
This project implements an address parsing solution in Python to extract province, district, and ward information from Vietnamese address strings. It leverages a Trie data structure for efficient string matching and the `editdistance` library to find the closest matches within a specified edit distance. The solution processes input addresses, normalizes them, and compares results against a test dataset.

## Features
- **Trie-based Search**: Uses a custom `MyTrie` class to store and search province, district, and ward names efficiently.
- **Edit Distance Matching**: Employs the `editdistance` library to find the closest match within a maximum edit distance of 2.
- **Address Segmentation**: Handles various delimiters (e.g., commas, periods, spaces) and preprocesses strings to remove prefixes like "tỉnh" or "huyện".
- **Evaluation**: Compares results against a ground truth dataset and generates an Excel report with detailed and summary statistics.

## Prerequisites
- Python 3.x
- Required libraries:
  - `editdistance`
  - `pandas`
  - `xlsxwriter`
  - Standard libraries: `time`, `re`, `collections`, `itertools`, `json`


## Usage
1. **Prepare Input Data**
   - Ensure `list_province.txt`, `list_district.txt`, and `list_ward.txt` are in the working directory or downloaded via the script.
   - Place `test.json` (test cases) in the working directory.

2. **Run the Notebook**
   - Execute all cells sequentially in Jupyter or Colab.
   - The `Solution` class processes addresses and outputs results.
   - The final cell evaluates performance and generates an Excel file named `GROUP_2.xlsx`.

4. **Output**
   - **Excel File**: Contains two sheets:
     - `summary`: Total correct answers, score (out of 10), max/avg execution time.
     - `details`: Per-test-case comparison of predicted vs. actual values.

## Code Structure
- **Cell 1**: Downloads data files.
- **Cell 2**: Installs dependencies.
- **Cell 3**: Imports libraries.
- **Cell 4**: Implements the `Solution` class with address parsing logic. Defines `MyTrieNode` and `MyTrie` for Trie-based search.
- **Cell 5**: Downloads the test JSON file.
- **Cell 6**: Defines normalization groups for evaluation.
- **Cell 7**: Runs tests, evaluates results, and generates output files.

## Example
For an input address like `"Xã Hòa Bình, Huyện Hòa Vang, Thành phố Đà Nẵng"`:
- **Output**: `{"province": "Đà Nẵng", "district": "Hòa Vang", "ward": "Hòa Bình"}`