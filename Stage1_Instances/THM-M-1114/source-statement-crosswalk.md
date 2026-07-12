# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md` supplies the Chinese title "giant component theorem," attributes
it to Erdos and Renyi, dates it to 1960, and says only "the appearance of a giant component in a
random graph." `Docs/Stage0_Blueprint.md` repeats that phrase while leaving definitions,
hypotheses, proof path, axioms, and machine artifact unspecified. The rev-5.6 target manifest marks
the inherited `已验证` status as untrusted and requires complete L0 rework.

These records identify a historical theorem family, not an exact statement. In particular they do
not distinguish the random graph process from `G(n,p)`, define "giant," select a parameter regime,
or state a probability limit.

## Candidate primary source

Paul Erdos and Alfred Renyi, "On the evolution of random graphs," *Publications of the
Mathematical Institute of the Hungarian Academy of Sciences* 5 (1960), 17-61, is the historical
primary-paper candidate suggested by the repository attribution and year. The exact numbered
theorem/page, original parameter convention, assumptions, scanned edition, and errata have not
been independently inspected in this intake. It is therefore a discovery lead only and gives no
`H0` or proof credit.

Later textbook formulations of the `G(n,c/n)` phase transition may help interpret modern notation,
but cannot silently replace the historical root. The statement phase must either crosswalk one to
the inspected primary theorem or explicitly justify a canonical modern restatement with checked
equivalence boundaries.

## Crosswalk

| Repository/source element | Mathematical information fixed | Lean information required | Intake result |
|---|---|---|---|
| "random graph" | an Erdos-Renyi family is intended by attribution | finite graph sample space and probability law | family identified; model open |
| "giant component" | a connected component macroscopic relative to graph size | component predicate, cardinality, largest/tie convention, linear bound | informal role fixed; exact bound open |
| "appearance" | a threshold or phase-transition conclusion | parameter regime, asymptotic filter, probability mode, quantifier order | unresolved |
| Erdos/Renyi, 1960 | historical source family | immutable source pinpoint and row-level mapping | candidate paper only |
| `已验证` | legacy screening metadata | accepted human review and kernel receipts | no evidentiary credit |

## Statement and formalization boundary

A common modern theorem says that for fixed `c > 1`, `G(n,c/n)` has with high probability a unique
component of linear order (with density characterized by a branching-process equation), while for
fixed `c < 1` all components are logarithmic in size. This description is a disambiguation aid,
not the frozen canonical claim: variants differ in included regimes, constants, size asymptotics,
and uniqueness conclusions.

No theorem-specific Lean artifact was found in the repository during intake, and no mathlib or
external declaration has yet been audited. Before `H0`, an independent reviewer must inspect the
selected primary edition, theorem/page, definitions, assumptions, proof boundary, and errata.
Before statement credit, every approved source component must map to an elaborated Lean expression
and the required domain, binder, hypothesis, scope, and boundary mutations must be checked.
