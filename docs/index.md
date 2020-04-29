---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
list_title: More Details
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

Welcome to the webpage for the ICLR 2020 SARFA Saliency paper.

# Explain Your Move: Understanding Agent Actions Using Specific and Relevant Feature Attribution

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

> As deep reinforcement learning (RL) is applied to more tasks, there is a need to visualize and understand the behavior of learned agents. Saliency maps explain agent behavior by highlighting the features of the input state that are most relevant for the agent in taking an action. Existing perturbation-based approaches to compute saliency often highlight regions of the input that are not relevant to the action taken by the agent. Our proposed approach, SARFA (Specific and Relevant Feature Attribution), generates more focused saliency maps by balancing two aspects (specificity and relevance) that capture different desiderata of saliency. The first captures the impact of perturbation on the relative expected reward of the action to be explained. The second downweighs irrelevant features that alter the relative expected rewards of actions other than the action to be explained. We compare SARFA with existing approaches on agents trained to play board games (Chess and Go) and Atari games (Breakout, Pong and Space Invaders). We show through illustrative examples (Chess, Atari, Go), human studies (Chess), and automated evaluation methods (Chess) that SARFA generates saliency maps that are more interpretable for humans than existing approaches.

### Citation

```(bibtex)
@inproceedings{salrl:iclr20,
  author = {Piyush Gupta and Nikaash Puri and Sukriti Verma and Dhruv Kayastha and Shripad Deshmukh and Balaji Krishnamurthy and Sameer Singh},
  title = {Explain Your Move: Understanding Agent Actions Using Specific and Relevant Feature Attribution},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year = {2020}
}
```
