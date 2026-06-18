# ESWA2026
Repository for submited article named "Unsupervised Topic Modeling of Song Lyrics with Large Language Models: A Zero-Shot Framework for Discourse Analysis"

# Repository Overview

The repository provides the materials required to reproduce the experiments presented in the manuscript, including:

Topic discovery using Large Language Models (LLMs);
Topic modeling baselines based on BERTopic and TopicGPT;
Multi-label topic classification experiments using Zero-shot, Few-shot, and Chain-of-Thought prompting;
Self-consistency and ensemble-based classification strategies;
Annotated benchmark datasets;
Experimental results and supplementary materials.

# Repository Structure
## Datasets

### funk_lyrics_estrofes_1000.xlsx

Large-scale corpus containing Brazilian Funk lyrics segmented into excerpts. The dataset is used in the topic discovery and topic classification experiments.

### 218_excerpts_annotated.xlsx

Human-annotated benchmark dataset used to evaluate topic classification performance. The dataset contains manually validated excerpt-topic pairs across the discourse-level topics defined in the study.

## Topic Discovery

### topic_identification.ipynb

Implementation of the LLM-based topic discovery pipeline, including theme extraction and topic generation.

### TopicGPT_FunkLyrics.ipynb

Implementation and evaluation of TopicGPT as a baseline topic modeling approach.

### bertopics_results_106_topics.xlsx

Complete BERTopic output containing the 106 topics generated during the large-scale comparative evaluation.

## Topic Classification
### few_shots_classification.ipynb

## Few-shot prompting experiments for multi-label topic classification.

### chain_of_thought.ipynb

Chain-of-Thought (CoT) prompting experiments, including topic-specific reasoning criteria.

## ensemble_prompt_classification.py

Implementation of the self-consistency and ensemble-based classification strategy proposed in the study.

## Data Collection
### scrapper.ipynb

Scripts used to collect and preprocess Brazilian Funk lyrics.

## Supplementary Material
### anexos_ESWA.pdf

Supplementary material containing additional experimental details, prompt templates, topic descriptions, classification criteria, examples, and complementary results referenced throughout the manuscript.



These resources enable the reproduction and extension of the experiments reported in the paper.

Citation

If this repository contributes to your research, please cite the corresponding article after publication.
