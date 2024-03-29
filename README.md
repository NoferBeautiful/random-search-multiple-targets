# Random search with multiple targets and agents

An application for modeling the process of random search by several targets in a cellular structure with the possibility of conducting experiments based on the choice of a probabilistic distribution of transitions.

The application was created for the Faculty of Physics of Moscow State University to be used in tests for students in order to conduct experiments and their subsequent analysis.

## Problem statement

There is a group of agents and targets. Each tick, agents jump in a random direction to a random number of cells, which is given by a probability distribution - exponential, or a mixture of Gaussians. The goal of the agents is to find all the targets. When the last is found, the simulation ends.

The distribution densities are given as follows:

<img src="/images_github/im_densities.jpg" alt="drawing" width="400"/>

The purpose of the experiment is to measure the entropy value depending on the parameters of the experiment - first of all, the distribution of the target jump lengths and its variance, as well as the number of targets and agents.

<img src="/images_github/gif_work.gif" alt="drawing" width="480"/>

## Implemented features

- Flexible choice of experiment environment - field size and number of agents.
- The possibility of using multiple probability distributions for the length of agent jumps.
- Free choice of variance and peak ratio for distributions with a convenient GUI.
- Change the simulation speed for full control over the experiments.

## Entropy calculation

The entropy in the experiment is calculated by the formula:

<img src="/images_github/im_entropy.jpg" alt="drawing" width="300"/>

The theoretical basis suggests that a distribution with thick tails copes better with the task and provides a faster decrease in entropy, since it better promotes the hit of agents in areas not yet explored.

Full information about theoretical basis of random search may be found [here](./source/statphys_theory.pdf) (rus).

## In biology

This process occurs in biology if you take agents for predators and targets for victims. An example is the article [Scaling laws of marine predator search behaviour
](https://www.nature.com/articles/nature06518) from Nature journal.

## Usage

To download and run this model please get it from [here](https://drive.google.com/drive/folders/1BTbJeQcihBA1ofYMU3jxXIlxbmImIVxA?usp=sharing) and run "main.exe" then.
