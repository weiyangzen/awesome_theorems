# THM-M-1359 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the ordinary-differential-equations
catalog item `鞍结分岔` (saddle-node bifurcation). The repository supplies only that title, a generic
20th-century attribution, and the gloss `平衡点消失的分岔` (a bifurcation in which equilibria
disappear). It gives no citation, binder-complete proposition, definitions, hypotheses, or proof
source. The catalog's `已验证` (verified) field is explicitly untrusted metadata.

## Intake result

The gloss identifies a theorem family but not one truth-valued claim. A standard saddle-node result
may be the elementary scalar normal form, a local zero-count theorem for a scalar parameter family,
a finite-dimensional vector-field theorem after a center-manifold or Lyapunov-Schmidt reduction, or
a fixed-point bifurcation theorem for maps. These variants require different derivatives,
nondegeneracy conditions, transformations, neighborhoods, stability claims, and conclusions.

Even the word "disappear" does not fix the orientation: a typical fold has two equilibria on one
side of the critical parameter, one nonhyperbolic equilibrium at the critical value, and none on the
other side, but the occupied side changes under a sign or parameter reversal. Choosing a familiar
normal form from memory would broaden or substitute the catalog target.

Gerald Teschl's *Ordinary Differential Equations and Dynamical Systems*, Section 6.5, was inspected
as an authoritative discovery source. Its equation (6.33), `x' = mu + x^2`, is explicitly called a
saddle-node bifurcation and illustrates the collision and disappearance of two fixed points. The
book presents this as a prototypical example, not as a general saddle-node theorem, and the catalog
does not cite or select it. It therefore receives no canonical-statement or H0 credit.

## Formal boundary

`IntakeProbe.lean` checks only pinned generic ODE, flow, fixed-point, derivative, and implicit-function
interfaces adjacent to possible future encodings. A bounded lexical search found no exact
saddle-node or fold-bifurcation declaration in repo-local Lean or pinned mathlib. Neither observation
is an exhaustive downstream anchor audit, and neither supplies a theorem or proof body.

The provisional root vector is `[H5, M4, R4]`. `H5` says that this catalog wording is not yet a
stable proposition; it does not say that correctly stated saddle-node theorems are false or open.
All six downstream tasks remain open. No canonical Lean expression, H0, M0, R0, accepted proof
state, audit completion, theorem completion, or master acceptance is claimed.
