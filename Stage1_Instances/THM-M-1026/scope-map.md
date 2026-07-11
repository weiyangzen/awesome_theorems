# Scope map

| Surface | Preserved scope | Open boundary |
|---|---|---|
| Family | Stable laws as the possible nondegenerate limits of normalized iid sums | necessity, converse, or biconditional root |
| Random objects | real iid random variables and their laws | sequence versus per-`n` product-space encoding |
| Normalization | positive scales and additive centerings | sign/order convention for `(sum - b_n) / a_n` |
| Convergence | convergence in distribution/weak convergence of laws | exact Lean topology and probability interface |
| Limit | nondegenerate stable probability law | definition of stability and parameterization |
| Attraction | laws whose normalized convolution powers converge to a stable law | analytic tail/regular-variation criterion, if included |

Degenerate point-mass limits, the ordinary Gaussian CLT alone, triangular-array CLTs, and statements
that merely assume stability are excluded. Boundary probes must cover zero/nonpositive scaling,
degenerate limits, Gaussian `alpha = 2`, asymmetric stable laws, and centering conventions.

The later statement phase must choose one source-pinpointed formulation and freeze every binder and
side condition. The scope seeds likely proof surfaces: iid sum laws as convolution powers,
normalization transport, tightness/subsequence reasoning, stability of limit laws, and the converse
construction or domain-of-attraction criterion. They are not yet accepted obligations.
