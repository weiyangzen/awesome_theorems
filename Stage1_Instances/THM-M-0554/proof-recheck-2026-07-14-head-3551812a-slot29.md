# THM-M-0554 proof-phase recheck: blocked

Item: `S56-M-0554-PROOF`

Attempt: `2026-07-14T04:13:29+08:00`

Base revision: `3551812aeaf826b94804e464b34511a7bbc7f6ff`

Base tree: `6ed6612d0a642e6879579700427c67045c1a34d7`

## Verdict

`blocked`. No genuine Atiyah-Hirzebruch spectral-sequence proof body was
implemented or found in the pinned dependency closure. The root remains `M4`;
this attempt adds no proof receipt, composition certificate, debt-vector
change, or state transition.

The immediate root cut remains:

- `M0554-X-GENCOH`: generalized-cohomology pair, excision, and wedge infrastructure;
- `M0554-C-EXACT-COUPLE`: the skeletal-filtration exact-couple construction;
- `M0554-C-E2-MODEL`: the cellular-cohomology `E2` identification;
- `M0554-L-STRONG`: strong convergence for the finite skeletal filtration.

Pinned mathlib supplies generic spectral-sequence, CW-complex, and
singular-homology substrate only. A fresh search of every pinned package found
no AHSS, generalized-cohomology, exact-couple, or strong-convergence proof
body. Mathlib's spectral-object file documents its intended
`spectralSequence`, `homologyData`, and `spectralSequenceHomologyData`
constructions as `TODO`.

## First Failed Gate

The exact-statement-fidelity gate fails before a proof can be credited. In
`Statement.lean`, the theory facts `pointIsPoint`, `exactnessAxiom`, and
`wedgeAxiomOrRepresentability`, and the CW facts `finiteCW`, `exhaustive`, and
`cellAttachments`, are proposition-valued data rather than required proofs.
The output chooses the meanings of `coefficientConvention`,
`strongConvergence`, and `naturalityInSpace`, while
`filtrationIsInducedBy` is only `K.skeleton = K.skeleton`.

Consequently the literal proposition has a zero spectral-sequence inhabitant
using zero objects, reflexive isomorphisms, and output-selected `True`
propositions. Earlier content-addressed trust-level-zero probes established
that literal inhabitance. The term is deliberately not retained or credited:
it constructs no AHSS and consumes none of the frozen semantic children.
Accepting it would violate the no-fake-result and checked child-to-parent
composition rules.

There are also unresolved predecessor-authority defects. `instance.json`
still records a null canonical module, expression, expression hash, and
environment fingerprint with status `open_statement_phase`. `task-dag.json`
remains unfrozen, leaves statement/source/tree open, and marks proof blocked by
predecessors. In addition, `statement.json` attributes convergence fields to
`AtiyahHirzebruchConvergenceData`, a declaration absent from this dossier;
the source defines `AtiyahHirzebruchData`. A proof-only worker cannot silently
replace or reconcile those predecessor artifacts.

## Validation

All Lean commands reused the automation-provided symlink to the pinned
canonical `.lake` artifacts. No update, build, dependency clone/fetch, network
action, or `.lake` mutation was performed. Generated Lean objects were placed
in a temporary directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0554` | 0 | Rank 106; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0554/check_obligation_tree.py` | 0 | 32 obligations and 91 typed edges passed; denominator `3c72072a...8048b`; root remains M4 without a composition certificate. |
| Isolated `lake env lean --trust=0 -R "$target" -o "$tmp/Statement.olean" Statement.lean` | 0 | The frozen target elaborated with Lean 4.29.0; the temporary object was 429072 bytes and was removed. |
| `rg` over pinned `*.lean` sources for AHSS/generalized-cohomology/exact-couple/strong-convergence terms | 1 | Expected no-match result: no pinned terminal proof candidate was found. |
| The same query over repo-local Lean sources outside this dossier | 0 | Target-specific hits were the legacy `S1_M_106.lean` statement and audit surface, not a terminal proof body. |
| Prohibited-token scan over owned `*.lean` sources | 1 | Expected no-match result: no `sorry`, `admit`, `axiom`, `sorryAx`, or `unsafe` declaration token occurs. |
| Pinned toolchain, mathlib, and manifest checks | 0 | Lean `4.29.0` commit `98dc76e...16740`; mathlib `8a178386...ea95`, tree `bdc39a31...1c2b`; manifest SHA-256 `321626c8...2d81`. |
| Spectral-object source hash and TODO scan | 0 | SHA-256 `2ce62b9d...740aa`; the intended generic constructors remain documented as `TODO`. |
| `jq empty Stage1_Instances/THM-M-0554/*.json` | 0 | All pre-existing structured JSON artifacts parsed. |
| `git diff --check -- Stage1_Instances/THM-M-0554` | 0 | No pre-existing whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The self-test manifest is absent because the proof phase is blocked. |

## Retry Condition

First publish and master-accept a source-faithful statement, reconcile the
instance, task, and statement projections, and issue obligation-registry
version 2. Then implement and compose the four root-cut packages without
placeholders. An alternative is an immutable exact compatible Lean 4 AHSS
proof that can be pinned, exact-type transported, and checked with complete
provenance and trust closure.

This artifact is durable blocker evidence only. It does not satisfy
`S56-M-0554-PROOF`, close an obligation, complete the audit or theorem, or
authorize master acceptance. Because the assigned phase is not genuinely
self-tested as complete, `.stage1-worker-selftest.json` remains absent.
