# THM-M-1148 obligation tree

This is the frozen proof architecture for the exact `PoissonIntegralFormula` target. All nodes are
root-relevant and machine/source/readability-required. The prior audit found representation theorems
for functions already known to be harmonic, not the required construction, so every proof node
remains open at `M4`. Planned fingerprints identify interfaces, not elaborated declarations.

## Root and statement

<a id="m1148-root"></a>
### M1148-ROOT
The exact target requires a harmonic, closure-continuous extension of arbitrary continuous real
boundary data, its boundary trace, and its interior Poisson formula.

<a id="m1148-s"></a>
### M1148-S
`S1` freezes disk domains and `R > 0`; `S2` freezes mathlib's normalized `circleAverage`; `S3`
separates interior and boundary regimes; `S4` owns the eventual axiom, foundation, and TCB audit.

<a id="m1148-s1"></a><a id="m1148-s2"></a><a id="m1148-s3"></a><a id="m1148-s4"></a>
### M1148-S1 through S4
These statement obligations prevent a unit-disk theorem, mean-value identity, unnormalized integral,
or nonpositive-radius variant from silently replacing the target.

## Normalization and branches

<a id="m1148-n"></a>
### M1148-N
Reduce a general disk to the unit disk and transport the complete solution back. `N1` owns domain
equivalences, `N2` continuity of pulled-back data, and `N3` preservation of every root conclusion.

<a id="m1148-n1"></a><a id="m1148-n2"></a><a id="m1148-n3"></a>
### M1148-N1 through N3
The transport must preserve the exact Poisson-kernel normalization, not merely harmonicity.

<a id="m1148-b"></a>
### M1148-B
Closed-disk continuity splits into `B1` interior continuity and `B2` convergence at each boundary
point. `B3` proves these regimes exhaust the closed disk and recomposes them.

<a id="m1148-b1"></a><a id="m1148-b2"></a><a id="m1148-b3"></a>
### M1148-B1 through B3
The boundary branch is essential: mathlib's audited mean-value theorem assumes continuity on the
closure and therefore cannot establish it here.

## Construction and analytic core

<a id="m1148-c"></a>
### M1148-C
`C1` defines the interior Poisson integral, `C2` establishes integrability, and `C3` extends the
candidate to a total function with prescribed boundary values.

<a id="m1148-c1"></a><a id="m1148-c2"></a><a id="m1148-c3"></a>
### M1148-C1 through C3
The construction alone gives no harmonicity or boundary continuity credit.

<a id="m1148-l"></a>
### M1148-L
The core package consists of `L1` harmonicity, `L2` unit kernel mass, `L3` concentration away from
the approached boundary point, `L4` uniform continuity of boundary data, and `L5` the near/far arc
estimate proving boundary convergence.

<a id="m1148-l1"></a><a id="m1148-l2"></a><a id="m1148-l3"></a><a id="m1148-l4"></a><a id="m1148-l5"></a>
### M1148-L1 through L5
Each leaf has an architectural budget below 100 substantive steps. These budgets do not prove the
lemmas and must be revised if implementation exposes hidden branches or imported theorem packages.

## Boundaries and terminal composition

<a id="m1148-x"></a>
### M1148-X
This bridge owns pinned mathlib declarations, terminal-body provenance, transitive dependencies,
axioms, and integration APIs. It provides no proof credit merely because the import elaborates.

<a id="m1148-t"></a>
### M1148-T
`ObligationTree.lean` kernel-checks the structural equivalence between `ConstructedSolution` and
the exact root. The composition consumes the whole solution package; all analytic children remain
open. The frozen root cut set is `M1148-C`, `M1148-L1`, `M1148-B`, and `M1148-N3`.

No proof body, H0/R0 review, audit completion, or theorem completion is claimed.
