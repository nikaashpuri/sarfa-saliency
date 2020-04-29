---
layout: post
title:  "Specific and Relevant Feature Attribution (SARFA)"
date:   2020-04-25 17:01:20 +0530
categories: jekyll update
---
<style>
.button {
  background-color: #eeeeee;
  box-shadow: 0 5px 0 #2a7ae2;
  color: black;
  padding: 0.5em 1em;
  position: relative;
  text-decoration: none;
  text-transform: uppercase;
  border-radius: 5px;
  border-color: black;
}

.button-left {
  border-radius: 5px 0px 0px 5px;
}

.button:hover {
  background-color: #cccccc;
  text-decoration: none;
}

.button:active {
  box-shadow: none;
  top: 5px;
}
</style>

Published in ICLR 2020 as _"Explain Your Move: Understanding Agent Actions Using Specific and Relevant Feature Attribution"_.

* [Nikaash Puri](https://www.linkedin.com/in/nikaash-puri/), Adobe
* [Sukriti Verma](https://www.linkedin.com/in/sukritivermaa/), Adobe
* [Piyush Gupta](https://www.linkedin.com/in/piyushgupta22/), Adobe
* [Dhruv Kayastha](https://www.linkedin.com/in/dhruvkayastha/), Indian Institute of Technology Kharagpur
* [Shripad Deshmukh](https://www.linkedin.com/in/shripad-deshmukh/), Indian Institute of Technology Madras
* [Balaji Krishnamurthy](https://www.linkedin.com/in/balaji-krishnamurthy-4241695/), Adobe
* [Sameer Singh](http://sameersingh.org/), University of California, Irvine

<a href="https://arxiv.org/abs/1912.12191" class="button">ArXiv</a>
<a href="https://arxiv.org/pdf/1912.12191.pdf" class="button">PDF</a>
<a href="https://openreview.net/forum?id=SJgzLkBKPB" class="button">OpenReview</a>
<a href="https://github.com/nikaashpuri/sarfa-saliency" class="button">Code+Data</a>


Deep learning has achieved success in various domains such as image classification, machine translation, image captioning, and deep Reinforcement Learning (RL). To explain and interpret the predictions made by these complex, black-box systems,  
various gradient and perturbation techniques have been introduced for image classification and deep sequential models.

However, interpretability for RL-based agents has received significantly less attention. Interpreting the strategies learned by RL agents can help users better understand the problem that the agent is trained to solve. Interpretation of RL agents is also an important step before deploying such models to solve real-world problems.

Our motivation behind this was to understand the moves made by AlphaZero - an RL agent trained to play Chess. We wanted to understand how Alphazero decides to make a particular move and what are the pieces it looks at. Current approaches for explaining RL agents did not work too well for Chess. They would either miss out on important pieces or highlight irrelevant ones. So we came up with SARFA - a perturbation based approach for generating saliency maps for black-box agents that builds on two desired properties of action-focused saliency. 

![useful image]({{ site.url }}/assets/sarfa_workflow.png)

SARFA captures features that are both specific and relevant to the move to be explained to generate more meaningful explanations. Let’s look at how SARFA works. We have the original state, and we have the agent’s Q-values for that state. 
Now, we perturb a specific feature of the state - for a Chess board this could mean removing a piece, for visual input this could mean blurring around a pixel. Then, we query the agent to get the Q-values for the perturbed state as well. This gives us the Q-values of state, action pairs in both the original and the perturbed state.

SARFA uses these Q-values to generate a saliency score for the perturbed feature. This is repeated over all the features in a particular state to understand the contribution of each feature to the action that the agent takes.

SARFA captures and combines two intuitive concepts:
1. Specificity: This captures the impact of perturbation only on the Q-value of the action to be explained. 
2. Relevance: This downweighs irrelevant features that alter the expected rewards of actions other than the action to be explained.

Let's understand them one by one.
### Specificity
Specificity captures whether a feature specifically impacts the action to be explained.

![Specificty - 1]({{ site.url }}/assets/specificity_1.png)
Consider the Chess position to be as shown. The action here (shown with the yellow arrow) is to move the white Bishop to square b6. The agent’s Q-values for the original state are shown in the top brown graph. Now, if we perturb this state by removing the white knight in the box. The agent also gives us the Q-values for the perturbed state. These are shown in the orange graph. In this position, when we remove the white knight, the agent thinks that the original move is no longer useful.
Therefore, the white knight is specifically important to explain the move,

![Specificty - 2]({{ site.url }}/assets/specificity_2.png)
Lets look at another example. We have the same position as before. But now lets perturb this state by removing the white queen in the box. When we remove the white queen, the agent thinks that the original move is still relatively just as good. Therefore, the white queen is not specifically important to explain the move  


### Relevance
Now lets look at Relevance. Relevance captures whether a feature is relevant to the action to be explained 
![Relevance]({{ site.url }}/assets/relevance.png)
Lets perturb our original position by removing this black pawn in the box. The relative Q-value of the action Bb6 falls, however, this fall is only because the Q-value of some other action (Bb4) increases. Therefore, the pawn is not relevant to the action to be explained. 

So now, we put specificity and relevance together to get SARFA. Now, let’s look at some illustrative results

### Results

#### Illustrative Results
![Chess Illustrative Result]({{ site.url }}/assets/results.png)
SARFA combines specificity and relevance to generate more meaningful explanations. The black rook and queen are important because the action exploits their position. The white knight is important because it protects the square the bishop goes to.  


#### Human Studies
We conducted a human study with 40 expert chess players. We showed them 15 puzzles that had one correct move. 
For each puzzle, we show either the puzzle without a saliency map, or the puzzle with a saliency map generated by one of three different approaches. We observed that the saliency maps generated by SARFA help players solve puzzles more accurately while taking less time than alternative approaches.
