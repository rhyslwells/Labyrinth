# Reinforcement Learning Theory and Concepts

## Introduction to Reinforcement Learning

Reinforcement Learning (RL) is a type of machine learning where an agent interacts with an environment and learns to make decisions that maximize cumulative rewards. The key components of an RL system include:

- **Agent**: An entity that interacts with the environment and learns to optimize its actions based on rewards. In the hunter-prey project, both the hunter and prey act as agents.
- **Environment**: The setting in which the agents operate. In the hunter-prey project, this is a 2D grid where agents interact.
- **State ($s$)**: The current situation in the environment, often defined by the positions and attributes relevant to the agent's decision-making.
- **Action ($a$)**: The available moves or decisions an agent can take.
- **Reward ($r$)**: A scalar value received after taking an action, representing feedback from the environment.
- **Policy ($\pi$)**: A strategy that the agent follows, mapping states to actions.
- **Q-Value ($Q(s, a)$)**: The expected cumulative reward for taking a particular action in a given state and following the policy thereafter. The Q-values guide the agent in making decisions that maximize long-term rewards.

## Key Terminology

- **Markov Decision Process (MDP)**: A formal framework for decision-making where outcomes depend solely on the current state (Markov property).

## Exploration vs. Exploitation

One of the major challenges in reinforcement learning is balancing exploration (trying new actions) and exploitation (choosing the best-known actions). The epsilon-greedy strategy is commonly used, where a small probability (epsilon) allows for exploration while primarily exploiting the best-known actions.

## Core Algorithms in Reinforcement Learning

### Q-Learning

Q-learning is a value-based, model-free RL algorithm where the agent learns the optimal policy by updating Q-values based on the rewards received. It is particularly useful in discrete environments like grids.

**Q-learning update rule:**

$$
Q(s_t, a_t) \leftarrow Q(s_t, a_t) + \alpha \left[ r_{t+1} + \gamma \max_{a'} Q(s_{t+1}, a') - Q(s_t, a_t) \right]
$$

**Explanation:**

- **$Q(s_t, a_t)$**: The Q-value of the current state $s_t$ and action $a_t$.
- **$\alpha$**: The learning rate, determining how much new information overrides old information.
- **$r_{t+1}$**: The reward received after taking action $a_t$ from state $s_t$.
- **$\gamma$**: The discount factor, balancing immediate and future rewards.
- **$\max_{a'} Q(s_{t+1}, a')$**: The maximum Q-value for the next state $s_{t+1}$ across all possible actions $a'$.

**Notes**:

- Q-learning is well-suited for environments where the state and action spaces are discrete and manageable in size.
- The algorithm is designed to converge to the optimal policy, even in non-deterministic environments, as long as each state-action pair is sufficiently explored.

### SARSA (State-Action-Reward-State-Action)

SARSA is another value-based RL algorithm, differing from Q-learning in that it updates the Q-values based on the action actually taken by the policy.

**SARSA update rule:**

$$
Q(s_t, a_t) \leftarrow Q(s_t, a_t) + \alpha \left[ r_{t+1} + \gamma Q(s_{t+1}, a_{t+1}) - Q(s_t, a_t) \right]
$$

**Explanation:**

- **$Q(s_t, a_t)$**: The Q-value of the current state $s_t$ and action $a_t$.
- **$\alpha$**: The learning rate, determining how much new information overrides old information.
- **$r_{t+1}$**: The reward received after taking action $a_t$ from state $s_t$.
- **$\gamma$**: The discount factor, balancing immediate and future rewards.
- **$Q(s_{t+1}, a_{t+1})$**: The Q-value for the next state $s_{t+1}$ and the action $a_{t+1}$ actually taken according to the policy.

**Notes**:

- SARSA’s on-policy nature ensures that it learns a policy that aligns with its exploration strategy, leading to more stable behavior in environments with randomness or noise.
- The learning process may be slower compared to Q-learning, but it can be more robust in environments where the agent’s behavior is expected to align closely with the policy it follows.

### Key Differences from Q-Learning

- **On-Policy vs. Off-Policy**: Unlike Q-learning, which is off-policy and updates based on the best possible action in the next state, SARSA is on-policy and updates based on the actual action taken by the agent.
- **Conservatism**: SARSA tends to be more conservative in its policy updates, making it suitable for environments where the agent’s policy needs to adapt to uncertainties.

### Deep Q-Networks (DQN)

DQN extends Q-Learning by using deep neural networks to approximate Q-values, enabling the handling of larger state spaces or more complex environments.
