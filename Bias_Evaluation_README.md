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
Inspired by the datasets used in the original study on bias in LLM debates, we will create two complementary dataset types tailored to our target community:

- **Curated Training Data** – In the original study, training data included texts reflecting partisan positions and structured debate content. For our project, we will compile approved and culturally aligned texts, including educational materials, domain-specific content, and journalism adhering to community standards. This ensures the model learns safe and contextually appropriate language.

- **Evaluation Data** – The original study used benchmark prompts and controlled debate scenarios to measure bias and alignment between agents. For our adaptation, we will design benchmark prompts that test model alignment and response safety for culturally relevant topics. This includes controlled scenarios, restricted term lists, and adversarial prompts to measure the model’s consistency in avoiding unsafe or inappropriate outputs.

This approach allows us to systematically evaluate and compare different LLMs for biases relevant to our target community, providing a foundation for safe and culturally aware chatbot development.

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
