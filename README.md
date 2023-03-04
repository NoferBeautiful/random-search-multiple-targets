# Random search with multiple targets and agents

An application for modeling the process of random search by several targets in a cellular structure with the possibility of conducting experiments based on the choice of a probabilistic distribution of transitions.

The application was created for the Physics Department of Moscow State University to be used in tests for students in order to conduct experiments and their subsequent analysis.

## Problem statement

There is a group of agents and targets. Each tick, agents jump in a random direction to a random number of cells, which is given by a probability distribution - exponential, or a mixture of Gaussians. The goal of the agents is to find all the targets. When the last is found, the simulation ends.

The distribution densities are given as follows:

PHOTO

The purpose of the experiment is to measure the entropy value depending on the parameters of the experiment - first of all, the distribution of the target jump lengths and its variance, as well as the number of targets and agents.

PHOTO

## Entropy calculation

The entropy in the experiment is calculated by the formula:

PHOTO

The theoretical basis suggests that a distribution with thick tails copes better with the task and provides a faster decrease in entropy, since it better promotes the hit of agents in areas not yet explored.

Full information about theoretical basis of random search may be found [here](./source/statphys_theory.pdf) (rus).

## Launching

## In biology

This process occurs in biology if you take agents for predators and targets for victims. An example is the article [Scaling laws of marine predator search behaviour
](https://www.nature.com/articles/nature06518) from Nature journal.

