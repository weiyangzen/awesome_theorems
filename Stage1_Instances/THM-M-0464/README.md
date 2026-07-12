# THM-M-0464 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the metadata item named "Pila theorem". The
repository gloss, "rational-point counting in o-minimal structures", is treated as the
Pila-Wilkie counting theorem, not as a claim that every result bearing Pila's name has been
formalized. The year `2011` in the discovery metadata conflicts with the primary paper's 2006
publication date and provides no proof or machine credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Pila-Wilkie's sub-polynomial bound for rational points of bounded height in the transcendental part of a definable set | Exact quantifiers, height convention, definable-family parameters, and uniform/non-uniform form remain for the statement phase |
| Ambient geometry | subsets of real Cartesian powers definable in an o-minimal expansion of the real field | No particular Lean encoding of o-minimality or definability is selected yet |
| Exceptional locus | the algebraic part, the union of connected positive-dimensional semialgebraic subsets | Its exact source definition must be transported without replacing it by an arbitrary algebraic/Zariski locus |
| Counting | rational points of height at most `T`, bounded by `c * T^epsilon` | Source height and lower bound on `T` must be frozen before elaboration |
| Uniformity | constants may depend on the definable set and `epsilon`; family-uniform refinements are separate | Uniform variants and algebraic-point variants are excluded from the root unless source audit proves they are the intended item |
| Foundations | Lean 4 kernel plus a pinned mathlib environment | Toolchain, imports, axioms, TCB, and computation profiles remain open |

## Statement phase

The exact root is now frozen as Pila-Wilkie (2006), Theorem 1.8, first version. The canonical Lean
expression is `AwesomeTheorems.THM_M_0464.PilaWilkieStatement` in `Statement.lean`; it elaborates
against the pinned Lean 4.29.0/mathlib environment. `statement.json` records binder order, source
snapshot, hashes, imports, and exactness decisions, while `statement_validation.md` records the
node-scoped commands and output.

This is statement evidence, not proof evidence. The declaration is a definition of a `Prop`, with
no theorem declaration or proof body. Machine state is therefore `M3`, and theorem completion is
false.

## Anchor audit

The pinned mathlib and repo-local closure provide statement ingredients but no Pila-Wilkie proof.
The 2026-07-12 external Lean repository inventory is frozen and classified in `anchor-audit.json`:
three o-minimality-related projects were inspected at immutable commits, and none contains an exact
terminal theorem or a feasible proof-bearing integration. `anchor_audit.md` records the search,
trust findings, archive hashes, validation, and limitations. Machine state remains `M3`.

## Obligation architecture

`obligation-registry.json` freezes sixteen root-relevant semantic obligations before proof
execution, while `typed-graphs.json` separates proof, refinement, provenance, evidence, trust,
documentation, and workflow edges. `ObligationTree.lean` checks only the conditional unfolding
from a complete counting premise to the exact root. Every mathematical package plus source,
provenance, readability, and trust closure remains open; theorem completion is false.

## Intake verdict

Lifecycle remains `planned`; the intake vector `[H1, M4, R3]` is superseded for the machine
statement component by the provisional vector `[H1, M3, R3]`. The first-version variant and a
canonical Lean expression are now frozen, but no representation transport, proof, or closure is
credited. This dossier makes no theorem-completion or machine-proof claim.

The structured claim and exclusions are in `intake.json`; the source relationship and precise
ambiguities are recorded in `source_statement_crosswalk.md`. Validation evidence is in
`validation.md`.
