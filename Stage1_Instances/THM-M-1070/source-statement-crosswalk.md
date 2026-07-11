# Source-statement crosswalk

## Repository source

The controlling repository discovery record is
`Docs/researches/math_theorems.md:7842-7847`: it names "Lévy过程," attributes it to Paul Lévy
(1934), and gives only `平稳独立增量过程` (stationary independent-increment process). The matching
Stage0 record at `Docs/Stage0_Blueprint.md:29153-29178` explicitly leaves the exact definition,
assumptions, equivalent formulations, axioms, and machine artifact open. Those records establish
identity and discovery scope, not an exact theorem or proof.

## Definition-source candidates

- David Applebaum, *Lévy Processes and Stochastic Calculus*, second edition, Cambridge University
  Press, 2009, Chapter 1. This is a modern definition and regularization-source candidate; exact
  definition/theorem numbers, pages, hypotheses, and errata require direct edition inspection.
- Ken-iti Sato, *Lévy Processes and Infinitely Divisible Distributions*, Cambridge Studies in
  Advanced Mathematics 68, Cambridge University Press, 1999, Chapter 1. This is a modern
  definition-source candidate; its conventions and exact pinpoint require direct inspection.
- Paul Lévy's historical 1934 work is provenance supplied by the repository metadata, not yet an
  accepted primary statement anchor. A bibliographically exact work and passage must be identified
  before it can support `H0`.

These are discovery anchors only. No edition was inspected and no source is accepted at intake.

## Crosswalk

| Repository phrase | Intended source component | Required Lean surface | Intake status |
|---|---|---|---|
| Lévy process | one standard continuous-time process class | exact predicate/structure plus a substantive source-backed theorem deliverable | identity frozen; deliverable open |
| process | family of measurable random variables on one probability space | probability space, time index, codomain, measurability | included; encoding open |
| starts at zero | `X_0 = 0` almost surely | almost-everywhere equality at time zero | included from standard scope; source convention unverified |
| independent increments | joint independence for finite ordered disjoint increments | finite-family random-variable or sigma-algebra independence | included; exact API open |
| stationary increments | increment distribution depends only on elapsed time | equality of pushforward probability measures | included; exact API open |
| stochastic continuity | convergence in probability as time converges | topology, measurability, and convergence predicate | included; source convention unverified |
| cadlag paths | definition clause or regular modification theorem | path-space regularity or modification relation | deliberately unresolved pending source |

## Evidence boundary

The provisional `H1` means a standard published definition is strongly expected, but no exact
edition/passage/assumption/errata crosswalk or independent review exists. No repo-local or upstream
Lean declaration has been accepted or inspected, so the machine state remains `M4`. The statement
and anchor-audit phases must separately record exact source passages and exact formal candidates;
neither a matching name nor a definition assembled from assumed fields is proof evidence.
