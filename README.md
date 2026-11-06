# Persian Text Dataset Preparation

A Python project for preprocessing Persian text and preparing datasets for text correction tasks.

## Overview

This project provides a simple pipeline for preparing Persian text datasets. It includes text cleaning, sentence tokenization, synthetic spelling error generation, and dataset creation.

## Features

- Persian text extraction and preprocessing
- Text normalization and cleaning
- Sentence tokenization using Hazm
- Removal of empty sentences
- Synthetic spelling error generation
- Creation of paired incorrect and correct sentences
- Exporting the final dataset to CSV format

## Project Structure

```text
persian-text-dataset-preparation/
├── prepare_dataset.py
├── requirements.txt
├── README.md
├── .gitignore
```

## Requirements

- Python 3.x
- Hazm

## Usage

1. Place your input text files in the appropriate directories inside `data/raw/`.
2. Configure the input and output paths in `prepare_dataset.py`.
3. Run the script:

```bash
python prepare_dataset.py
```

4. The processed files and final CSV dataset will be saved in `data/processed/`.

## Output

The final dataset is exported as a CSV file containing two columns:

- `wrong_sentence`: Sentence containing spelling errors.
- `correct_sentence`: Original correct sentence.
