# Adapting Bias Evaluation Research for a Context-Specific Chatbot

## Introduction
This document adapts insights from research on detecting and analyzing bias in language models.  
The referenced paper, [Systematic Biases in LLM Simulations of Debates](https://arxiv.org/abs/2402.04049), while valuable, is based on outdated models and focuses primarily on political differences.

The primary goal of our project is to establish a robust testing framework for evaluating biases in LLMs.  
This framework will allow us to systematically assess different models and compare their alignment with culturally appropriate standards.

As a subsequent application of this framework, we plan to adapt its principles for the development of a chatbot tailored for Haredi use cases.  
This ensures that responses remain safe, controlled, and culturally aligned. By extending the methodology beyond political bias, we address a broader set of cultural and ethical considerations critical to our target community.

## Models to Use
For this project, we will employ state-of-the-art large language models such as **LLaMA-3**, **Mistral**, and **GPT-4**.  
These models provide advanced reasoning capabilities and support fine-tuning or reinforcement learning.

The primary purpose of using these models is within a testing framework to systematically evaluate biases and assess alignment with culturally appropriate standards.  
Applying the bias-detection methodology from the referenced study to modern architectures allows us to compare models, measure their cultural and ethical alignment, and guide the development of a chatbot tailored for our community.

## Datasets

Inspired by the original study, we will create two complementary dataset types tailored to our target community:

- **Curated Training Data**: culturally aligned texts, including educational content, domain-specific materials, and approved journalism.  
  **Purpose**: to ensure the model learns safe and contextually appropriate language consistent with community standards.  
  **Examples**: 
    - Texts from religious educational books  
    - Articles from community newspapers or approved online portals  
    - Domain-specific materials, e.g., guides on social conduct  
    - Structured content for teaching ethical reasoning  

- **Evaluation Data**: structured prompts and scenarios designed to test model alignment and response safety.  
  **Purpose**: to empirically evaluate whether the model avoids unsafe, biased, or culturally inappropriate outputs.  
  **Examples**: 
    - Prompts asking for advice on ethical dilemmas  
    - Questions on culturally sensitive topics  
    - Scenarios including restricted or sensitive terms  
    - Red-team style adversarial prompts to check model consistency  

**Creation and Preparation Process**:  
1. **Collection** – gather materials from approved, culturally relevant sources.  
2. **Filtering & Review** – check for alignment with community norms and remove inappropriate content.  
3. **Annotation & Marking** – identify sensitive terms, ethical issues, or bias-prone passages.  
4. **Formatting & Structuring** – convert materials into a uniform format for testing and fine-tuning.  
5. **Quantitative Checks** – measure coverage, consistency, and proportion of sensitive content to ensure dataset quality.  

This systematic approach allows us to create datasets that are representative, safe, and suitable for evaluating biases in LLMs, while guiding the development of a culturally aware chatbot.


## Evaluation Methodology
Evaluation will follow three main axes:

1. **Automatic testing** – structured prompts verifying refusal of restricted content.  
2. **Human evaluation** – domain experts judging cultural and ethical alignment.  
3. **Comparative baselines** – benchmarking against general-purpose models to demonstrate improved safety.

## Conclusion
By combining bias-detection research, modern models, and carefully designed datasets, this project develops a chatbot that is accurate, helpful, and culturally safe.  
This approach updates older methods to contemporary needs, providing robust protection against uncontrolled content while leveraging large-scale AI capabilities.

## References
- [Systematic Biases in LLM Simulations of Debates](https://arxiv.org/abs/2402.04049)
