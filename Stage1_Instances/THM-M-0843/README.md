# THM-M-0843 rev-5.6 dossier

This directory is the fail-closed `planned` intake dossier for Szemerédi's regularity lemma.
The repository source gives only the title, Endre Szemerédi, the year 1975, and the gloss "regular
partition of a dense graph." That identifies the finite dense-graph regularity-lemma family, but it
does not state the uniformity convention, equitable-partition requirement, parameter order, or
whether the size bound is existential or explicit.

Pinned mathlib contains a directly relevant theorem,
`szemeredi_regularity`, in
`Mathlib.Combinatorics.SimpleGraph.Regularity.Lemma`. A narrow Lean probe checks its exact
displayed type and the definitions that give meaning to its partition predicates. The candidate is
the effective equitable version documented by Dillies and Mehta: for positive `epsilon` and a
lower bound `l` no larger than the finite vertex count, it returns an `epsilon`-uniform
equipartition into between `l` and an explicit `bound epsilon l` parts.

That was the intake boundary: its probe was discovery evidence rather than a statement or proof
receipt. The statement phase below now selects the inspected effective/equitable variant. The
anchor-audit phase then checks its exact mathlib adapter and terminal axiom report, while full trust
closure remains downstream. The accepted root remains `[H1, M3, R4]`; the audit records an
unaccepted `M0-W / E2` candidate. Accepted proof state, audit completion, and theorem completion are
all false. Intake commands remain recorded in `validation.md`.

## Statement result

The statement phase selects the effective Lean-facing formulation displayed in Section 3 of the
inspected ITP article. `Statement.lean` freezes the exact finite-graph binders, positive real
tolerance, graph-size premise, equitable full-vertex partition, explicit bound, and mathlib
ordered-off-diagonal uniformity predicate. It uses the two independently necessary definition
imports `Regularity.Bound` and `Regularity.Uniform`; the proof-bearing `Regularity.Lemma` module is
not imported.

`check_statement.py`, `statement.json`, `statement-validation.md`, and
`statement-receipt.json` bind the explicit expression fingerprint, environment, checked one-way
transport to an existential-bound form, and four required structural mutations. This is a
self-tested statement proposal pending master acceptance. It supplies no formal-anchor audit,
proof credit, debt-vector promotion, audit completion, or theorem completion.

## Anchor-audit result

`AnchorAudit.lean` now checks the frozen proposition through the exact pinned mathlib declaration
`szemeredi_regularity`. `anchor-audit.json` records the immutable mathlib revision and tree, exact
source and support-module hashes, normalized statement match, terminal proof-body location, direct
proof dependencies, machine axiom report, supplemental placeholder/unsafe/oracle checks, license,
and the bounded public-search ledger. `check_anchor_audit.py` rechecks those facts and reruns the
narrow Lean adapter without mutating `.lake`.

The exact adapter is classified as a self-tested `M0-W / E2` candidate pending master acceptance;
it is not accepted `E1` closure or theorem completion. Public code-search access failures also mean
discovery saturation is not claimed. Obligation-tree composition, full transitive provenance and
TCB acceptance, H0/R0, hermetic validation, independent verification, and release remain open.

## Obligation-tree result

`obligation-registry.json` now freezes version 1 of the semantic architecture before proof-phase
closure credit. The 44 obligations expand the actual pinned `szemeredi_regularity` source through
its cardinality and tolerance branches, energy induction, chunk/equitabilise constructions,
density engine, energy recomposition, terminal body, exact adapter, and source/trust boundaries.
`typed-graphs.json` keeps proof, refinement, provenance, evidence, trust, documentation, and
workflow edges separate; `obligation-tree.md` is the readable projection.

`ObligationTree.lean` kernel-checks only the exact root composition from the adapter and pinned
terminal interfaces. Eighteen internal relations are deliberately recorded as unverified
source-body decomposition plans, not composition certificates. The aggregate validation recipe and
receipt preserve that boundary: zero obligations close, the accepted root remains `[H1, M3, R4]`,
and audit and theorem completion remain false pending proof-phase certificates and master review.

## Proof result

`Proof.lean` now adopts the explicit `szemeredi_regularity` body from pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. It checks the exact root both through the frozen
terminal-adapter composition and through a direct exact-type wrapper. Lean reports the terminal and
both root wrappers sorry-free, with only `propext`, `Classical.choice`, and `Quot.sound` in their
axiom closures. The single upstream terminal body is not duplicated.

This is provisional proof-node evidence for an `M0-W` root proposal. The receipt binds exact
declaration evidence for the root, terminal, and adapter, but credits no frozen obligation as
accepted or individually closed. It withholds individual closure credit for the 18 internal
source-body decompositions that still lack abstract-child composition certificates. The accepted
instance therefore remains `[H1, M3, R4]`, and validation, release, H0/R0, master acceptance, and
theorem completion remain open.

## Validation result

`Validation.lean` gives a separately written exact-target wrapper that imports
neither the proof nor the obligation tree. `check_validation.py` replays the
frozen modules from fresh temporary source copies and checks the exact terminal,
composition, proof roots, differential root, observed axiom set, local source
hygiene, immutable mathlib pin, direct regularity-source provenance, terminal
olean, and license. Exact commands and decisions are in `validation-phase.md`;
the structured recipe and provisional receipt are `validation-spec.json` and
`validation-receipt.json`.

This is same-worker warm-cache corroboration, not rev-5.6 hermetic or
independent-runner evidence. The prerequisite proof remains provisional, the
frozen graph remains `[H1, M3, R4]` with zero accepted closed obligations, and
the 18 internal source-body decompositions retain no individual closure
credit. `audit_complete=false` and `theorem_complete=false`; no `E1`, accepted
`M0-W`, release, or master acceptance is claimed.
