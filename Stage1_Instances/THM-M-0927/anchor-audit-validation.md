# THM-M-0927 anchor-audit validation

Item: `S56-M-0927-ANCHOR_AUDIT`

Base revision: `4a10a7a4ddff88e302d5a303b16dd687d9468f63`

Base tree: `730de242597680b39a7087d3204dfd1e6c41c60e`

Validation date: 2026-07-13 (`Asia/Shanghai`)

## Result

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the natural-index
Binet theorem `Real.coe_fib_eq` in `Mathlib.NumberTheory.Real.GoldenRatio`. Its substantive terminal
body is the function theorem `Real.coe_fib_eq'`: it proves that `Nat.fib` and the difference of the
two geometric characteristic-root solutions agree by uniqueness for the Fibonacci linear
recurrence. The pointwise theorem is a `funext_iff` wrapper around that body.

`AnchorAudit.lean` repeats the frozen DLMF target literally. Its adapter invokes the pinned theorem,
unfolds `Real.goldenRatio` and `Real.goldenConj`, and normalizes powers of quotients. The audit
checker separately prints the statement target and audit copy with explicit universes/arguments and
compares them after normalizing only Lean's generated proof-field names. This preserves `Nat.fib`,
the `Nat` binder, real coercion, both root signs, the `2^n * sqrt 5` denominator, and index zero.

Lean reports only `propext`, `Classical.choice`, and `Quot.sound` for `Real.coe_fib_eq`, its terminal
body, the broader integer theorem, and the exact adapter. `assert_no_sorry` and `#print sorries`
report all four declarations sorry-free. The pinned source block contains transparent theorem bodies
and no proof-gap, bodyless, unsafe, opaque, external-code, or oracle marker. Complete transitive
provenance, executable TCB, generated-artifact, computation, and release acceptance remain later
gates.

The bounded external audit found an independent educational proof in
`fpvandoorn/LeanCourse23@390f7c49ce3ced7ad5ffcf74e039dcc8f912afdf`. It proves a Binet formula
by two-step induction, but for a file-local Fibonacci function and denominator `phi - psi`, under
Lean 4.2.0 and a different mathlib pin. The same source file contains unrelated `sorry` exercises,
and no checked transports or upstream kernel receipt were available. It is therefore a blocked
`M5` research lead, not `M1` or exact root evidence. An immutable automath result merely wraps its
own pinned `Real.coe_fib_eq`; AlphaProof results are downstream consumers; mathlib3 is historical.

Sourcegraph's bounded `coe_fib_eq` search completed with 18 matches in five repositories and no
skipped results. GitHub code search required authentication and grep.app returned security
checkpoints. These limitations are recorded rather than converted into a global absence claim.
The frozen seven-record inventory is fully classified, but discovery saturation is not claimed.

The exact pinned route is recorded as an
`M0-W_candidate_pending_downstream_acceptance` with nonrelease direct-kernel evidence. The
authoritative planned root remains `[H1, M3, R4]`: this phase does not install an accepted proof
declaration or freeze the obligation tree. `AUDIT-Z` and theorem completion are both false.

## Commands and exact outcomes

All commands ran in this worker clone. Lean used the existing manifest-pinned shared Lake artifacts
read-only. No `lake update`, `lake build`, dependency clone/fetch, or other `.lake` mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 structure and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-0927` | 0 | rank 1546; planned; no legacy slot; theorem incomplete |
| manifest-driven `git rev-parse HEAD` and `git status --porcelain` over all 11 materialized packages | 0 | every package matched its manifest revision and had a clean source worktree |
| `lake env lean ../../Stage1_Instances/THM-M-0927/Statement.lean` from `Formalizations/Lean` | 0 | frozen exact target, checked transports, four expected mutations, and boundary witnesses re-elaborated; stdout SHA-256 `4195b975...23f4b` |
| `lake env lean ../../Stage1_Instances/THM-M-0927/AnchorAudit.lean` from `Formalizations/Lean` | 0 | exact adapter and three candidate interfaces elaborated; four expected axiom sets and four sorry-free reports; stdout SHA-256 `b068ed13...f0209` |
| `python3 -B Stage1_Instances/THM-M-0927/check_anchor_audit.py --worker-packet .stage1-worker-selftest.json` | 0 | authority identity, exact serialized target equality, pins, source/body hashes, seven records, adapter, receipt, packet, and Lean replay agreed |
| `python3 -B Stage1_Instances/THM-M-0927/check_statement.py` | 1 | historical receipt has a stale shared-blueprint input after integration; unchanged statement source and expression are checked independently here |
| repository-local and all-materialized-package `rg` searches | 0 | no independent local proof beyond the pinned mathlib family; one mathlib consumer found |
| bounded Sourcegraph, GitHub, grep.app, and immutable Git/raw inspection | mixed, recorded | exact mathlib route, one nonexact teaching proof, historical predecessor, and downstream consumers classified; access failures receive no negative-search credit |
| `python3 -m json.tool` on each new JSON artifact and `.stage1-worker-selftest.json` | 0 | all structured artifacts parsed |
| comment-stripped prohibited-construct scan over `AnchorAudit.lean` and the pinned natural-Binet block | 1 (expected no match) | no proof gap, bodyless declaration, unsafe/opaque body, external-code boundary, or placeholder marker |
| `git diff --check -- Stage1_Instances/THM-M-0927 .stage1-worker-selftest.json` plus no-index checks | 0 | no whitespace diagnostics |

## Boundary

This self-test supports only the provisional anchor-audit node pending master acceptance. The
statement predecessor is itself provisional. The obligation registry, proof-phase integration and
composition, complete provenance/trust and TCB closure, primary-source and readable reconstruction
review, hermetic replay, independent verification, and deterministic release evidence remain open.
No accepted proof state, audit-completion receipt, or theorem-completion receipt is claimed.
