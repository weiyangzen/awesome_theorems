# Immutable Lean anchor audit

Item: `S56-M-0648-ANCHOR_AUDIT`

## Search boundary

The audit used repository commit `83b3ee61af2480377e065c884a683be47b3ea070`, Lean 4.29.0
(`98dc76e3c0a9b856c9b98726b713fb04fab16740`), and the already-present mathlib checkout at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (commit date 2026-03-30). The root Lake manifest pins
that exact mathlib revision. No dependency was updated, cloned, or fetched.

The search covered all repository `*.lean` files and every already-pinned Lake package for the
terms `Loewenheim`, `Löwenheim`, `Skolem`, `elementarySubstructure_card_eq`, and
`elementaryEmbedding_card_eq_of_ge`. It found the two terminal mathlib declarations below, local
historical probes/wrappers, and unrelated uses of “Skolem”. No second external package in the
pinned dependency closure contains a competing upward/downward Loewenheim-Skolem declaration.
Because no other external Lean repository is pinned by this target, an unpinned web hit would not
be integration evidence and was not fetched.

## Candidate inventory

| Candidate | Immutable source | Exact source location | Audit result |
|---|---|---|---|
| `FirstOrder.Language.exists_elementarySubstructure_card_eq` | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` | `Mathlib/ModelTheory/Skolem.lean:122` (body lines 126-136) | exact downward candidate: distinguished set, all four bounds, elementary substructure, containment, and exact lifted cardinality |
| `FirstOrder.Language.exists_elementaryEmbedding_card_eq_of_ge` | same mathlib revision | `Mathlib/ModelTheory/Satisfiability.lean:217` (body lines 220-236) | exact upward candidate: infinite input model, both bounds, forward elementary embedding, and exact cardinality |
| `FirstOrder.Language.exists_elementaryEmbedding_card_eq` | same mathlib revision | `Mathlib/ModelTheory/Satisfiability.lean:243` | rejected as the direct upward anchor: returns a disjunction of embedding directions and has a different hypothesis surface |
| `FirstOrder.Language.exists_elementarilyEquivalent_card_eq` | same mathlib revision | `Mathlib/ModelTheory/Satisfiability.lean:257` | rejected: elementary equivalence does not preserve the required forward embedding witness |
| repo-local `S1_M_300.lean` and `THM-M-0646` occurrences | repository base revision above | paths reported by the recorded `rg` search | discovery wrappers only; not independent terminal proof bodies and receive no duplicate proof credit |

## Exactness and provenance

`AnchorAudit.lean` repeats the frozen halves verbatim and applies each selected declaration with
precisely their binders, hypotheses, lift orientations, and conclusions. Lean
accepts both applications without transports, theorem weakening, `sorry`, or new assumptions. It
deliberately does not assemble `CanonicalTarget`; that belongs to the later proof phase.

The downward terminal body constructs a Skolem reduct of a closure after choosing a subset of the
required cardinality. The upward terminal body applies compactness to the elementary diagram,
shrinks the resulting model with the downward cardinal wrapper, then obtains the forward elementary
embedding. Both bodies are ordinary theorem definitions in the pinned source. A scoped scan of the
two source files found no `sorry`, `admit`, or `axiom` declarations. `#print axioms` reports only
`[propext, Classical.choice, Quot.sound]` for each selected declaration and each checked audit
wrapper. These are Lean/mathlib foundational axioms, not target-specific postulates or an oracle.

Mathlib is already in the repository's pinned Lake closure and is Apache-2.0 licensed. Thus both
selected candidates are dependency-feasible at this revision. Their terminal bodies are shared
mathlib bodies; local probes and wrappers must be deduplicated from coverage counts.

## Classification and boundary

The anchor result is **exact candidate found and locally applicable**. It resolves the Lean-anchor
discovery question for both halves, but does not by itself award `M0`: the canonical conjunction is
not proved here, and the obligation, composition, full provenance, validation, hermetic replay,
independent-review, and master-acceptance gates remain open. Human-source fidelity also remains
below `H0`; the historical primary-source pinpoint and errata work identified at intake is not a
Lean anchor question and is not silently promoted by mathlib comments.

No theorem completion or audit-completion claim is made.

## Validation record

All commands below ran in the worker clone. The Lean command ran from `Formalizations/Lean`; all
others ran from the repository root.

| Command | Exit | Exact result summary |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0648/AnchorAudit.lean` | 0 | both exact applications elaborated; all four `#print axioms` commands reported only `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets; ranks 1..1546; all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0648` | 0 | rank 694; planned; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0648/anchor-audit-receipt.json` | 0 | valid JSON |
| scoped `rg` candidate search over repository and pinned packages | 0 | 125 matching source lines; inventory reconciled as described above |
| scoped `rg` scan for `sorry`, `admit`, or `axiom` in both candidate modules and `AnchorAudit.lean` | 0 | no matches |
| `git diff --check -- Stage1_Instances/THM-M-0648` | 0 | no whitespace errors |
