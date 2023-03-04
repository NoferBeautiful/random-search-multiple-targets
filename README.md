# Random search with multiple targets

An application for modeling the process of random search by several targets in a cellular structure with the possibility of conducting experiments based on the choice of a probabilistic distribution of transitions.

The application was created for the Physics Department of Moscow State University to be used in tests for students in order to conduct experiments and their subsequent analysis.

The purpose of the experiment is to measure the entropy value depending on the parameters of the experiment - first of all, the distribution of the target jump lengths and its variance, as well as the number of targets and agents.

### Entropy calculation

The entropy in the experiment is calculated by the formula:

PHOTO

The theoretical basis suggests that a distribution with thick tails copes better with the task and provides a faster decrease in entropy, since it better promotes the hit of targets in areas not yet explored.

Full information about theoretical basis of random search may be found [here](./source/statphys_theory.pdf) (rus).

