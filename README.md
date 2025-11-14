# Research Paper Classification

This project is a comprehensive system for classifying research papers into various scientific disciplines. The pipeline includes web scraping from Mendeley, data cleaning and preprocessing, and a fine-tuned BERT model for classification.

## Uploaded Files

The following files are included in this repository:

*   `gdrive_folder_downloader.ipynb`: A Jupyter notebook to download the dataset from Google Drive.
*   `mendeley_scraper.ipynb`: A Jupyter notebook for scraping research paper data from Mendeley.
*   `research_papers_bert_finetuning.ipynb`: A Jupyter notebook for fine-tuning the BERT model for text classification.

## Project Data and Models on Google Drive

The core datasets, trained model, and training artifacts are hosted on Google Drive.

### Model & Training Artifacts

*   **Main Model Folder (`bert_text_classifier`):** [https://drive.google.com/drive/folders/1IqttC-7FPdlnA-5zWzbyNF5d3-uIntbr](https://drive.google.com/drive/folders/1IqttC-7FPdlnA-5zWzbyNF5d3-uIntbr)
*   **Training Checkpoints (`bert_classification_output`):**
    *   checkpoint-6988: [https://drive.google.com/drive/folders/1oAKMa9rNeLulQzhqvw3u35_lDp1Il2j4](https://drive.google.com/drive/folders/1oAKMa9rNeLulQzhqvw3u35_lDp1Il2j4)
    *   checkpoint-13976: [https://drive.google.com/drive/folders/1S6bk9CSK7EXqaRzvRPA6cYowJFi8tE5S](https://drive.google.com/drive/folders/1S6bk9CSK7EXqaRzvRPA6cYowJFi8tE5S)

### Datasets

*   **Primary Cleaned Dataset (`cleaned_dataset.csv`):** [https://drive.google.com/file/d/1tv57_K5XjJ46Rlzj3mhRYf7_TElCovYh/view?usp=drivesdk](https://drive.google.com/file/d/1tv57_K5XjJ46Rlzj3mhRYf7_TElCovYh/view?usp=drivesdk)
*   **Raw Scraped Data (`Mendeley_Research`):**
    *   Computer Science: [https://drive.google.com/drive/folders/1xPFKizXlFf4GkQqOeQHjAkkHpQOAefkU](https://drive.google.com/drive/folders/1xPFKizXlFf4GkQqOeQHjAkkHpQOAefkU)
    *   Medicine: [https://drive.google.com/drive/folders/1uuRWFhe3OSDbqBwYFRuzfB72oG8E9Vfv](https://drive.google.com/drive/folders/1uuRWFhe3OSDbqBwYFRuzfB72oG8E9Vfv)
    *   Business: [https://drive.google.com/drive/folders/1dXWtIzKl5AOUsqBfSZC6BHRiIT8dYPX3](https://drive.google.com/drive/folders/1dXWtIzKl5AOUsqBfSZC6BHRiIT8dYPX3)
    *   Chemistry: [https://drive.google.com/drive/folders/105je5xW-uXM4mGWEf2mBnml2AjzhAVZc](https://drive.google.com/drive/folders/105je5xW-uXM4mGWEf2mBnml2AjzhAVZc)
    *   Mathematics: [https://drive.google.com/drive/folders/1UEBxx55Rc-LoVLMP-mBjBCBh3TsAzZKe](https://drive.google.com/drive/folders/1UEBxx55Rc-LoVLMP-mBjBCBh3TsAzZKe)
    *   Psychology: [https://drive.google.com/drive/folders/1IZ1zTLb2cfBp136v-hNBwvq3qASM-e9d](https://drive.google.com/drive/folders/1IZ1zTLb2cfBp136v-hNBwvq3qASM-e9d)
    *   Environmental Science: [https://drive.google.com/drive/folders/1IDv2CCm23I71pm8-D06YaRdCThpZX98C](https://drive.google.com/drive/folders/1IDv2CCm23I71pm8-D06YaRdCThpZX98C)
    *   Biology: [https://drive.google.com/drive/folders/105je5xW-uXM4mGWEf2mBnml2AjzhAVZc](https://drive.google.com/drive/folders/105je5xW-uXM4mGWEf2mBnml2AjzhAVZc)
    *   Physics: [https://drive.google.com/drive/folders/19mnlfDM81N3phXZhZn1wqfkApv3ft8HR](https://drive.google.com/drive/folders/19mnlfDM81N3phXZhZn1wqfkApv3ft8HR)

## How to Use

1.  **Download the data:** Access the datasets from the Google Drive links provided above. The `gdrive_folder_downloader.ipynb` notebook can be used as a reference for programmatically downloading the data.
2.  **Scrape new data (Optional):** Run the `mendeley_scraper.ipynb` notebook to scrape additional research paper data from Mendeley.
3.  **Train the model:** Run the `research_papers_bert_finetuning.ipynb` notebook to fine-tune the BERT model on the provided dataset.

## Model Performance

The fine-tuned BERT model achieves the following performance:

*   **Evaluation Loss:** 0.184
*   **Accuracy:** 95.39%

### Classification Report

| Category              | Precision | Recall | F1-Score | Support |
| --------------------- | --------- | ------ | -------- | ------- |
| Biology               | 0.94      | 0.93   | 0.94     | 3177    |
| Business              | 0.96      | 0.97   | 0.97     | 3179    |
| Chemistry             | 0.94      | 0.96   | 0.95     | 3073    |
| Computer Science      | 0.96      | 0.93   | 0.95     | 2987    |
| Environmental Science | 0.95      | 0.94   | 0.95     | 2850    |
| Mathematics           | 0.93      | 0.96   | 0.95     | 3091    |
| Medicine              | 0.97      | 0.96   | 0.96     | 3067    |
| Physics               | 0.97      | 0.95   | 0.96     | 3181    |
| Psychology            | 0.97      | 0.97   | 0.97     | 3348    |

## Hugging Face Model

The fine-tuned model is available on Hugging Face at: [https://huggingface.co/Emran025/bert_text_classifier](https://huggingface.co/Emran025/bert_text_classifier)
