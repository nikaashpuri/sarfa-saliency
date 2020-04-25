# SARFA
Link to the paper - [SARFA paper](https://arxiv.org/abs/1912.12191)

Working example - [Example](Example.ipynb)
### Dependencies
1. Python3
2. Packages listed in requirements.txt
### Using SARFA to interpret your RL Models
1. Clone Repository
```
git clone https://github.com/nikaashpuri/sarfa-saliency.git
```
2. Navigage to cloned repository
```
cd sarfa-saliency
```
3. Install minimal dependencies using pip (if you want to use SARFA with your Reinforcement Learning Models)
```
pip install -r requirements-minimal.txt
```
3. Install all dependencies using pip (if you want to use the examples included in the repository)
```
pip install -r requirements.txt
```
4. Use SARFA in your code
```python
import sarfa_saliency
.....
.....

dict_q_vals_before_perturbation, original_action = RL_agent.q_values(state) # this is a dictionary, where the key is an action, and the value is the q-value of that action for this state 

# now perturb the state, this step depends on your domain 
# if you are using images or chess boards, you can use the perturbtations provided in our examples 
perturbed_state = perturb(state)

dict_q_vals_after_perturbation = RL_agent.q_values(perturbed_state)

saliency = sarfa_saliency.computeSaliencyUsingSarfa(original_action, dict_q_vals_before_perturbation, dict_q_vals_after_perturbation)

# that's all folks 
```

