# Scope map

## Preserved source scope

The repository fixes only the label `Young塔` (`Young tower`), Lai-Sang Young, the year 1998,
the gloss `非一致双曲系统的工具` (`a tool for nonuniformly hyperbolic systems`), high
importance, and an untrusted `已验证` status. It supplies no primary citation, definition,
premise, or conclusion. Intake therefore preserves only the scope of a return-time tower or Markov
extension used to derive statistical properties of some nonuniformly hyperbolic systems.

Young's 1998 paper is a strong source candidate because it constructs an extension `F : Delta`
over a return map `f^R : Lambda -> Lambda`, under the positive return-time function `R`, and uses
that extension to prove several results. This observation narrows source discovery but does not
select a canonical proposition.

## Proposition-changing decisions

An approved target correction must choose an exact source theorem and freeze all of the following:

- whether the root is the tower construction, SRB-measure existence, exponential mixing, the
  central limit theorem, an example-class result, or a later generalization;
- the phase space, discrete map, differentiability or singularity assumptions, invariant set, and
  invertibility or noninvertibility convention;
- the hyperbolic product structure, stable and unstable disk families, branch partition, return
  map, separation time, contraction, distortion, and absolute-continuity hypotheses;
- the return-time codomain, positivity, measurability, integrability or tail condition, and the
  reference measure used to state it;
- the lifted tower space, tower map, projection, invariant measure, normalization, and the exact
  source definition of an SRB measure if that result is selected;
- the aperiodicity or total-ergodicity condition and exact correlation norm/rate if mixing is
  selected; and
- the observable class, centering, convergence-in-distribution convention, variance, and
  coboundary criterion if the central limit theorem is selected.

These choices produce inequivalent propositions. They are a resolution checklist, not a theorem
statement.

## Candidate families not credited

- The Markov extension `Delta = {(x, l) : x in Lambda, 0 <= l < R(x)}` with its level/return map.
- Young 1998 Theorem 1, deriving an SRB measure from P1-P5 and integrability of `R`.
- Young 1998 Theorem 2, deriving exponential correlation decay from an exponential tail and total
  ergodicity.
- Young 1998 Theorem 3, deriving a central limit theorem and a zero-variance coboundary criterion.
- The paper's specialized theorems for Axiom A attractors, expanding or piecewise hyperbolic maps,
  billiards, logistic maps, or Henon-type attractors.
- Later results using Young/Gibbs-Markov towers with other tail rates or weaker hypotheses.

No family in this list is selected or credited at intake.

## Explicit exclusions

Kakutani and Rokhlin towers (`THM-M-1409` and `THM-M-1410`) are distinct measure-theoretic roots.
A Markov partition (`THM-M-1415`) is not interchangeable with Young's countable variable-return
extension. An SRB measure (`THM-M-1417`), Pesin theory (`THM-M-1420`), and the Pesin entropy formula
(`THM-M-1421`) are neighboring notions or results, not substitutes for this target.

Also excluded are a bare sigma-type definition, a structure that takes every tower law or desired
conclusion as a field, a tautology assuming its conclusion, an arbitrary suspension, a finite
constant-height example, and a numerical return-time or correlation experiment. None identifies or
closes the received catalog item.

## Degenerate and boundary scope

An exact source must decide empty or null bases, empty branch families, zero versus positive return
times, nonreturning points, integrable versus nonintegrable tails, finite versus infinite lifted
measures, periodic tower components, noninvertible or singular maps, projection multiplicity,
constant or noncentered observables, and zero variance. Silently excluding these cases can change
the selected statement.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib provides adjacent APIs for function
iteration, Birkhoff sums, measure restriction, measure-preserving maps, and ergodicity. The
intake-only bounded spelling search found no Young-tower, Gibbs-Markov-tower, return-time-tower, or
inducing-scheme occurrence in pinned mathlib Lean sources. These facts show possible substrate only; they are
not a formal-candidate audit, statement elaboration, or machine-proof evidence.
