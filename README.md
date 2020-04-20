# SARFA
## Specific and Relevant Feature Attribution
Deep learning has achieved success in various domains such as image classification, machine translation, image captioning, and deep Reinforcement Learning (RL). To explain and interpret the predictions made by these complex, black-box systems,  
various gradient and perturbation techniques have been introduced for image classification and deep sequential models.

However, interpretability for RL-based agents has received significantly less attention. Interpreting the strategies learned by RL agents can help users better understand the problem that the agent is trained to solve. Interpretation of RL agents is also an important step before deploying such models to solve real-world problems.

This is the code for SARFA - a perturbation basedapproach for generating saliency maps for black-box agents that builds on two desired properties of action-focused saliency. 

1. Specificity: This captures the impact of perturbation only on the Q-value of the action to be explained. 
2. Relevance: This downweighs irrelevant features that alter the expected rewards of actions other than the action to be explained.
