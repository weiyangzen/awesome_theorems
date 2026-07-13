# THM-M-0476 anchor-audit validation

Item: `S56-M-0476-ANCHOR_AUDIT`

Base revision: `db4b8793e70ce8af74c9c9490acfa50aa3684d5e`

Base tree: `6434a20532ae7c523ad293e67a6228ab384bfb8a`

Validation date: `2026-07-13` (`Asia/Shanghai`)

## Result

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the direct candidate
`ZMod.wilsons_lemma` in `Mathlib.NumberTheory.Wilson`. Its natural modulus, factorial, direction,
and equality in `ZMod p` agree with the frozen target. The only binder difference is mathlib's
`[Fact p.Prime]`; `AnchorAudit.lean` independently restates the explicit-premise target and checks
the adapter `letI : Fact p.Prime := ⟨hp⟩` before applying the pinned theorem.

The pinned body changes the factorial into an interval product, bijects that product with all units
of `ZMod p`, and closes with `FiniteField.prod_univ_units_id_eq_neg_one`. The product form,
converse, and stronger primality iff in the same module do not add an independent terminal body.
Lean reports `propext`, `Classical.choice`, and `Quot.sound` for the exact terminal, adapter, nearby
Wilson declarations, and units-product dependency. `#print sorries` reports the terminal and exact
adapter sorry-free. Full transitive provenance, executable TCB, and trust-policy acceptance remain
downstream gates.

The bounded external audit found one dedicated Lean 4 repository at immutable commit
`441b532e68f39d1d46636be8619d3349a80f253e`. Its `Wilson` theorem uses `Int.ModEq`, adds a
`1 < p` argument, and proves an iff under Lean 4.29.1 and a different mathlib revision. It has no
detected license and is not locally materialized, so it is a related `M3` source anchor rather than
an exact root candidate. Public Sourcegraph discovery completed with 16 matches in five indexed
repositories; the other Lean 4 results were mathlib or downstream teaching consumers. GitHub code
search required authentication, grep.app returned a security checkpoint, and the complete immutable
Formal Conjectures tree had no relevant path. These are bounded results, not global saturation.

The exact mathlib route is therefore recorded as an
`M0-W_candidate_pending_downstream_acceptance`. The authoritative planned root remains
`[H1, M3, R4]`: this phase neither installs an accepted proof-phase declaration nor freezes the
obligation tree. `AUDIT-Z` and theorem completion are both false.

## Commands and exact outcomes

All commands ran in this worker clone. Lean used the existing manifest-pinned shared Lake artifacts
read-only. No `lake update`, `lake build`, dependency clone/fetch, or other `.lake` mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 structure and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-0476` | 0 | rank 1357; planned; no legacy slot; theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | mathlib revision `8a1783...ea95`, tree `bdc39a...5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty; pinned dependency source tree clean |
| `lake env lean ../../Stage1_Instances/THM-M-0476/AnchorAudit.lean` from `Formalizations/Lean` | 0 | exact adapter and five declarations elaborated; six axiom reports matched; terminal and adapter were sorry-free; stdout SHA-256 `7140ce72...0480e` |
| `lake env lean ../../Stage1_Instances/THM-M-0476/Statement.lean` from `Formalizations/Lean` | 0 | frozen predecessor target, premise transport, four expected mutation failures, and explicit expression re-elaborated |
| `python3 -B Stage1_Instances/THM-M-0476/check_anchor_audit.py` | 0 | target identity, pins, hashes, seven records, body markers, exact adapter, receipt, packet, and narrow Lean replay agreed |
| `python3 ../../Stage1_Instances/THM-M-0476/check_statement.py` from `Formalizations/Lean` | 1 | historical predecessor receipt expected an older authoritative-blueprint hash; no statement mismatch occurred, and the successor checker binds the unchanged statement/expression hashes directly |
| `python3 -B Stage1_Instances/THM-M-0476/check_intake.py` | 1 | historical predecessor receipt expected an older shared authority hash after integration; this classified freshness failure was not repaired by rewriting predecessor evidence |
| repository-local and all-materialized-package `rg` searches | 0 | local target files plus the single pinned mathlib Wilson family located; no second exact terminal declaration found |
| immutable GitHub metadata/tree/raw inspection | 0 | `adimchimma/lean-wilsons-theorem-primes@441b532...253e` classified without cloning or integrating it |
| Sourcegraph bounded query in `anchor-audit.json` | 0 | complete response: 16 matches in five indexed repositories with `skipped=[]` |
| GitHub unauthenticated code search | 0 HTTP response | HTTP 401 access failure recorded; no negative-result claim |
| grep.app query | 0 HTTP response | Vercel Security Checkpoint recorded; no search-result claim |
| immutable Formal Conjectures recursive-tree inspection | 0 | non-truncated 1204-entry tree; no Wilson- or factorial-named path |
| `python3 -m json.tool` on each new JSON artifact and `.stage1-worker-selftest.json` | 0 | every structured artifact parsed |
| comment-stripped prohibited-construct scan over `AnchorAudit.lean` | 0 | no proof gap, bodyless declaration, unsafe/opaque body, external-code boundary, or placeholder marker |
| `git diff --check -- Stage1_Instances/THM-M-0476 .stage1-worker-selftest.json` plus no-index checks for new files | 0 | no whitespace diagnostics |

## Boundary

This self-test supports only the provisional anchor-audit node pending master acceptance. The exact
candidate still requires a frozen obligation registry, proof-phase integration and composition,
accepted terminal provenance/trust and TCB closure, primary-source and readable reconstruction
review, hermetic replay, independent verification, and deterministic release evidence. It supplies
no accepted proof state, audit-completion receipt, or theorem-completion receipt. The integration
lane must also refresh or supersede the stale predecessor authority-hash receipts before accepting
their nodes; this worker did not rewrite historical statement or intake evidence.
