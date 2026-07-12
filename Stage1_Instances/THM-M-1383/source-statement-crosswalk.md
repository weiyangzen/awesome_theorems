# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10076-10081` supplies exactly the title `边值问题`, attribution to
many mathematicians, the twentieth century, the gloss `两点边值问题的理论`, importance "high," and
status `已验证` (`verified`). Git history attributes all six uncited lines to repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, stable source ID,
edition, theorem/page locator, equation, definition, binder, hypothesis, conclusion, proof boundary,
correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:37614-37639` repeats the gloss and classifies it as a problem/decision
proposition, while explicitly leaving the formal system, foundation, exact definitions and
premises, proof route, dependencies, alternate forms, axioms, machine status, and artifact links
open. The rev-5.6 manifest preserves the source label only as untrusted metadata and resets this
target to `L0 / rework_required`.

## Inspected source-family discriminator

Gerald Teschl, *Ordinary Differential Equations and Dynamical Systems*, Graduate Studies in
Mathematics 140, American Mathematical Society, 2012, Chapter 5, Section 5.1, printed pages 141-144,
was inspected as an authoritative modern discovery source. It first treats a fixed-endpoint wave
equation and separation of variables. It then introduces a Sturm-Liouville problem

`L y = lambda y`

with endpoint conditions that are linear combinations of `y` and `p y'`, and lists at least two
different desired conclusions: countably many eigenvalues with corresponding eigenfunctions and
completeness of the eigenfunctions. Later sections develop still more distinct claims. Thus the
chapter confirms that "boundary-value problems" and even one named subclass do not identify a
single theorem.

The author-hosted preliminary PDF had SHA-256
`362433156525216abf596c17ce843204510e96d57afa4284a37c7aa5a9ffc36e`. A four-page extract made
with `pdftotext -f 152 -l 155 -layout` had 14,252 bytes and SHA-256
`e185478c9c6023160d469abe9c6205b1bb491cadf2b562fcaf6e6485061c6acb`. The official errata input
had SHA-256 `3eacbac5b8fc762c5d3f21183cba3ae638b9ac5fbe703cc52cf2857b9605996e`;
it corrects Chapter 5 material, including page 145, demonstrating that an eventual source admission
must bind an exact revision and relevant errata.

The catalog does not cite Teschl, select the example, select the Sturm-Liouville subclass, or select
either listed conclusion. No immutable source admission, complete assumptions/proof/errata mapping,
historical genealogy, or independent review is credited. This source is a discriminator only, not
the canonical claim and not `H0` evidence.

## Component crosswalk

| Repository element | Source-family alternatives | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `two-point` | boundary conditions imposed at two endpoint locations; separated or coupled conditions | endpoints in `Set.Icc`, evaluation and derivative predicates | endpoints, ordering, and boundary operators are absent; multipoint conditions are excluded substitutions |
| `boundary-value problem` | scalar/system, first/second/higher order, linear/nonlinear, regular/singular, homogeneous/inhomogeneous | `IsIntegralCurveOn`, `HasDerivWithinAt`, higher derivatives and operator predicates | no equation, carrier, regularity, or solution concept is selected |
| `theory` | existence, uniqueness, multiplicity, solvability, representation, estimates, spectral results, or numerical convergence | a quantified `Prop` only after one conclusion is chosen | not a truth-valued conclusion |
| collective twentieth-century attribution | classical and modern sources across many inequivalent results | source record and review receipt | not a pinpoint source or proof genealogy |
| `已验证` (`verified`) | mathematical proof, computation, formal proof, or editorial label | node-specific kernel and source receipts | explicitly untrusted; no credit |

The repository provides no ordered quantifiers, so even `for every admissible problem there exists
a unique solution` cannot be inferred. That universal statement is false without substantial
hypotheses, while an existential statement or a conditional criterion would be a different target.

## Neighbor crosswalk

The catalog itself separates narrower ODE topics: `THM-M-1384` through `THM-M-1391` schedule
Sturm-Liouville theory, Sturm comparison and separation, oscillation theory, the eigenvalue problem,
Weyl asymptotics, the Courant min-max principle, and the Prufer transform; `THM-M-1392` through
`THM-M-1394` schedule Green-function representation, the Fredholm alternative, and the shooting
method. It also separately schedules PDE Dirichlet, Neumann, Robin, and Green-function records.
This separation is strong scope evidence against folding any one of those claims into
`THM-M-1383`; it does not select a residual theorem for this target.

## Lean discovery boundary

Pinned mathlib's `Mathlib.Analysis.ODE` directory exposes basic integral curves, Picard-Lindelof
local initial-value existence, Gronwall initial-value uniqueness, and transformations. The intake
probe elaborates representative APIs from those modules. A bounded name search found no boundary-
value occurrence in pinned mathlib and no two-point boundary occurrence in pinned mathlib or repo-
local Lean source. The repo-local generic `boundary-value` hits concern unrelated topology, PDE,
and complex-analysis targets; none identifies this ODE topic. Generic initial-value machinery does
not establish satisfaction of a second endpoint condition.

This is deliberately not the downstream anchor audit: no external formal registry was exhaustively
searched, no candidate statement was normalized, and no machine debt stronger than `M4` is claimed.

## Gate decision

The exact source statement is unresolved. Retry requires an accountable source/target correction
that selects one immutable, independently reviewed, truth-valued proposition and maps every domain,
binder, assumption, conclusion, endpoint convention, degenerate case, proof boundary, and erratum.
Until then the canonical mathematical statement and Lean expression remain null, ordinary theorem-
proof execution is blocked by `H5`, and all downstream phases remain open.
