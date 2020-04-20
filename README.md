# SARFA
## Specific and Relevant Feature Attribution
Deep learning has achieved success in various domains such as image classification, machine translation, image captioning, and deep Reinforcement Learning (RL). To explain and interpret the predictions made by these complex, black-box systems,  
various gradient and perturbation techniques have been introduced for image classification and deep sequential models.

However, interpretability for RL-based agents has received significantly less attention. Interpreting the strategies learned by RL agents can help users better understand the problem that the agent is trained to solve. Interpretation of RL agents is also an important step before deploying such models to solve real-world problems.

Our motivation behind this was to understand the moves made by AlphaZero - an RL agent trained to play Chess. We wanted to understand how Alphazero decides to make a particular move and what are the pieces it looks at. Current approaches for explaining RL agents did not work too well for Chess. They would either miss out on important pieces or highlight irrelevant ones. So we came up with SARFA - a perturbation based approach for generating saliency maps for black-box agents that builds on two desired properties of action-focused saliency. 

![SARFA Workflow](https://github.com/nikaashpuri/sarfa-saliency/blob/master/Images%20for%20blog:readme/SARFA%20Workflow.png)

SARFA captures features that are both specific and relevant to the move to be explained to generate more meaningful explanations. Let’s look at how SARFA works. We have the original state, and we have the agent’s Q-values for that state. 
Now, we perturb a specific feature of the state - for a Chess board this could mean removing a piece, for visual input this could mean blurring around a pixel. Then, we query the agent to get the Q-values for the perturbed state as well. This gives us the Q-values of state, action pairs in both the original and the perturbed state.

SARFA uses these Q-values to generate a saliency score for the perturbed feature. This is repeated over all the features in a particular state to understand the contribution of each feature to the action that the agent takes.

SARFA captures and combines two intuitive concepts:
1. Specificity: This captures the impact of perturbation only on the Q-value of the action to be explained. 
2. Relevance: This downweighs irrelevant features that alter the expected rewards of actions other than the action to be explained.

Let's understand them one by one.
### Specificity
Specificity captures whether a feature specifically impacts the action to be explained.

![Specificty - 1](https://github.com/nikaashpuri/sarfa-saliency/blob/master/Images%20for%20blog:readme/Specificty%201.png)
Consider the Chess position to be as shown. The action here (shown with the yellow arrow) is to move the white Bishop to square b6. The agent’s Q-values for the original state are shown in the top brown graph. Now, if we perturb this state by removing the white knight in the box. The agent also gives us the Q-values for the perturbed state. These are shown in the orange graph. In this position, when we remove the white knight, the agent thinks that the original move is no longer useful.
Therefore, the white knight is specifically important to explain the move,

![Specificty - 2](https://github.com/nikaashpuri/sarfa-saliency/blob/master/Images%20for%20blog:readme/Specificty%202.png)
Lets look at another example. We have the same position as before. But now lets perturb this state by removing the white queen in the box. When we remove the white queen, the agent thinks that the original move is still relatively just as good. Therefore, the white queen is not specifically important to explain the move  


### Relevance
Now lets look at Relevance. Relevance captures whether a feature is relevant to the action to be explained 
![Relevance](https://github.com/nikaashpuri/sarfa-saliency/blob/master/Images%20for%20blog:readme/Relevance.png)
Lets perturb our original position by removing this black pawn in the box. The relative Q-value of the action Bb6 falls, however, this fall is only because the Q-value of some other action (Bb4) increases. Therefore, the pawn is not relevant to the action to be explained. 

So now, we put specificity and relevance together to get SARFA. Now, let’s look at some illustrative results

### Results
![Chess Illustrative Result](https://github.com/nikaashpuri/sarfa-saliency/blob/master/Images%20for%20blog:readme/Results.png)
SARFA combines specificity and relevance to generate more meaningful explanations. 
