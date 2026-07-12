# Scope map

## Repository boundary

The repository supplies a name, Watts/Strogatz attribution, the year 1998, and the phrase
"small-world phenomenon". It does not specify a graph distribution, observable, quantifier order,
finite-size bound, asymptotic regime, probability level, or conclusion. "Small-world" is also used
as a classification of measured networks. Neither a phenomenon label nor a classification is by
itself a theorem.

## Provisional included family

A legal downstream target must select one exact result about a source-specified Watts-Strogatz
model. Its scope is expected to expose:

- a finite ring-lattice graph, including vertex count and neighborhood degree;
- the exact random-rewiring procedure and its treatment of loops, duplicate edges, and dependence;
- a rewiring parameter and all parameter ranges;
- precise characteristic-path-length and clustering-coefficient definitions;
- one quantitative conclusion, with explicit expectation, probability, or asymptotic semantics.

This is a discovery boundary, not a conjunction and not an ordered Lean binder list.

## Decisions required at statement freeze

The statement phase must select and inspect an exact primary result. It must freeze the graph model,
whether the edge count or degree sequence is preserved, the randomness space, connectivity policy,
ordered versus unordered vertex pairs, the convention for unreachable pairs, local versus global
clustering, normalization, and the scaling of graph size, degree, and rewiring probability. It must
also distinguish a proved analytic result from a numerical observation in Figure 2 of the 1998
paper.

Boundary cases include an empty or singleton vertex type, degree zero, degree at least the number of
vertices, nonintegral neighborhood conventions, rewiring probabilities zero and one, disconnected
samples, vertices of degree below two, and ratios with zero denominators.

## Explicit exclusions

- Substituting the informal "six degrees of separation" slogan or an arbitrary diameter bound.
- Defining `SmallWorld G` to contain the desired path-length and clustering claims as fields, then
  proving them by projection.
- Replacing the Watts-Strogatz rewiring distribution by an Erdos-Renyi graph, Newman-Watts model, or
  deterministic graph family without a checked, source-faithful relationship.
- Presenting the existence of a graph that has small diameter and high clustering as the random
  model's characteristic-regime theorem.
- Treating plots, simulations, measurements of three empirical networks, or the metadata value
  `已验证` as mathematical or kernel proof.

`IntakeProbe.lean` checks only graph-library substrate. It does not select or elaborate the root.
