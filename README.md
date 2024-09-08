# Ontology-Based Project Risk Management Recommender System

## Project Overview

**Objective**:  
This academic project aims to develop a recommender system that assists users in retrieving and recommending project risk management knowledge. The system is ontology-based and is designed to provide real-time, personalized recommendations.

**Data Sources**:
- **PMBOK 5th Edition**: A comprehensive guide to project risk management processes.
- **PMI Practice Standard for Project Risk Management**: Outlines processes and practices for managing project risks.

## Key Components

### 1. Ontology Construction:
- **PRM Ontology**:  
  We constructed an ontology for Project Risk Management (PRM), representing knowledge extracted from PMBOK and PMI standards.
- **Tools Used**:  
  - **TF-IDF** (Term Frequency-Inverse Document Frequency) to weigh the importance of terms in the documents.
  - **Levenshtein Distance** to compute the similarity between words and concepts.
  - **Chunking** to extract relationships between different entities.
- The ontology was built using the **OWL (Web Ontology Language)** format, including key concepts, relationships, and hierarchies related to PRM.

### 2. Recommendation System:
- **Collaborative Filtering**:  
  The system uses collaborative filtering techniques combined with **TF-IDF** and **cosine similarity** to recommend relevant sections of the PMBOK based on user queries.
- The **OWL ontology** is converted into a **dataframe** to allow efficient querying and provide personalized recommendations based on the user's context.

### 3. Web Application:
- A user-friendly **web interface** was developed to interact with the recommendation engine.
- The application can be launched by running `scriptweb.ipynb` and accessing the web interface through the shortcut "Run me!" in a browser.

## Steps Involved

### 1. Data Preprocessing:
- We used **SpaCy** and **NLTK** for natural language processing, which included:
  - Lemmatization
  - Removal of stopwords
  - Tokenization of the textual data from PMBOK and PMI standards.

### 2. Ontology Building:
- From the processed data, we extracted concept hierarchies and relationships.
- The ontology was structured into an **OWL graph** that can be queried for recommendations.

### 3. Recommendation Engine:
- The recommendation engine applies machine learning techniques like **TF-IDF** and **cosine similarity** to compute similarities between user input and the ontology.
- The system then suggests relevant project management resources from PMBOK.

### 4. Web Application Deployment:
- The project includes a web application that provides real-time recommendations. Users can interact with the system through a browser interface by running `scriptweb.ipynb`.

### 5. Project Structure

- `Step_1_Data_pre-processing.ipynb`: Contains the code for data preprocessing and NLP.
- `Step_2_Ontology.ipynb`: Code for building the ontology from the processed data.
- `scriptweb.ipynb`: Code for the web application and recommendation engine.
- `corpora/`: Contains the PMBOK and PMI data used for building the ontology.
- `data/`: Contains the processed data and results.
- `web_recommendation/`: Contains the code for the web interface.
- `ontology_utils.py` and `utils.py`: Utility functions for ontology and data processing.

