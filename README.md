
# Personalized Networking Assistant

A smart tool designed to enhance professional networking by automatically extracting themes from event descriptions and generating engaging, context-aware conversation starters.

# Description: model selection process

The model  selection process is arguably the most consequential step in any AI application.
Choosing the wrong model can result in slow responses, poor accuracy, high resource consumption, or output that fails to meet user expectations.
For this project, two distinct NLP tasks required model evaluation: event theme classification and conversation text generation.

# Theme Extraction: [DistilBERT](https://huggingface.co)

For extracting themes from event descriptions, the team evaluated several Hugging Face transformer models.
The primary requirement for extracting themes from event descriptions was the ability to classify 
text into categories without task-specific training data—a technique known as zero-shot classification.
This is critical because the application must work for any type of networking event.

# Why DistilBERT was chosen:

It achieves the optimal balance between inference speed and classification accuracy.
For a real-time web application where users expect immediate feedback, the response time is critical.
Its compact size makes it highly deployable in resource-constrained environments.

# Conversation Generation: [GPT-2](https://huggingface.co)

For generating conversation starters, the requirement was a model capable of producing natural, contextually coherent text based on a structured prompt.

# Why GPT-2 Small was chosen:

It runs efficiently on standard hardware without needing GPU acceleration.
It produces conversation starters that are sufficiently natural and engaging—short, punchy opening lines suitable for professional networking.
Integration via the Hugging Face pipeline API makes it straightforward to configure and maintain.

