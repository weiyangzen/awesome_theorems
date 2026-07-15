# THM-M-0721 proof recheck at `472dc79e` (slot71)

Item: `S56-M-0721-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T15:13:54+08:00`

Base revision: `472dc79eb4d406a6707691193fbe3ab58d0f0cc4`

Base tree: `881d873727dc80435119839b8e60e9e9c2cfb208`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact root
`Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage`. The root remains
`[H1, M3, R4]`, and this proof item remains `[ ]`.

The checked declaration `root_of_candidate_packages` is conditional composition only. It consumes,
but does not construct, the two immediate root packages:

- `M0721-T-SAT-IN-NP`: a faithful binary SAT encoding, correct bundled polynomial-time TM2
  verifier, polynomial certificate bound, and package assembly;
- `M0721-T-UNIVERSAL-HARDNESS`: arbitrary-verifier normalization, Cook-Levin tableau construction,
  both correctness directions, and a bundled polynomial-time TM2 reduction.

Eleven frozen SAT and Cook-Levin obligations remain open. Their registry entries still have planned
prose targets rather than exact Lean declaration types, so implementing their bodies also requires
an append-only registry refinement before proof credit. Pinned mathlib supplies the TM2 substrate
and identity machine but no NP-completeness endpoint. Its source-level
`TM2ComputableInPolyTime.comp` item is `proof_wanted`; trust-zero Lean reports that no such checked
constant exists. The three immutable external candidates remain supporting-only,
placeholder-dependent, or contract-incompatible, with no checked transport to the frozen Bool-word
TM2 target.

Empty, universal, identity, classical-choice, fixed-source, and conditional shortcuts cannot supply
the universally quantified polynomial-time reductions required by the exact target. A universal
encoded-verifier language would still require the absent serialization, simulation, and polynomial
runtime bodies. Assuming either root package or substituting ordinary computable reducibility would
violate the exact-target gate.

The first failed implementation gate is `M0721-N-SAT-ENCODING`. The immediate root cut is
`M0721-T-SAT-IN-NP` plus `M0721-T-UNIVERSAL-HARDNESS`. Because the assigned proof phase is not
self-tested as complete, no proof receipt or `.stage1-worker-selftest.json` is emitted.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink to canonical pinned artifacts
was reused read-only. No dependency update, build, clone, fetch, checkout, or `.lake` mutation was
performed.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all; readlink Formalizations/Lean/.lake` | 0 | Base `472dc79e...f0cc4`, tree `881d8737...1b208`; only the automation-provided `.lake` symlink was initially untracked. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546; all are L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0721` | 0 | Rank 578; `planned`; L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| `LEAN_NUM_THREADS=1 timeout 600s python3 Stage1_Instances/THM-M-0721/check_statement.py` | 0 | Expression SHA-256 `758b1033...b204`; all four weakened mutations were distinguished; pinned Lean and mathlib identities matched. |
| `python3 Stage1_Instances/THM-M-0721/check_obligation_tree.py` | 0 | Passed 18 obligations and 45 typed edges; denominator `375921a1...b92a`; root remained M3 with both terminal packages M4. |
| From `Formalizations/Lean`, stream declaration-bearing `Statement.lean` and `ObligationTree.lean` to `LEAN_NUM_THREADS=1 timeout 300s lake env lean --trust=0 -t0 --stdin` | 0 | Exact statement and conditional composition elaborated; `root_of_candidate_packages` reported exactly `[propext, Quot.sound]` and supplied no terminal package. |
| Scan owned Lean files for `sorry`, `admit`, `axiom`, `unsafe`, `proof_wanted`, or `sorryAx` | 1 expected | No prohibited proof device occurs in the owned Lean files. |
| Scan pinned mathlib for `IsNPComplete`, `NPcomplete`, `NPComplete`, `CookLevin`, `cook_levin`, or `SATLang` | 1 expected | No eligible endpoint exists. |
| Ask trust-zero Lean to print axioms for `Turing.TM2ComputableInPolyTime.comp` | 1 expected | Lean reported `Unknown constant`, confirming that source-level `proof_wanted` created no checked declaration. |
| `timeout 240s python3 Stage1_Instances/THM-M-0721/check_anchor_audit.py` | 0 | Local pins/hashes and all three immutable external candidates matched; root classification remained M2. |
| Inspect Lean/Lake/mathlib identities and hash frozen inputs | 0 | Lean 4.29.0 at `98dc76e...740`, Lake 5.0.0, mathlib `8a178386...ea95` with clean tree `bdc39a31...c2b`; all recorded target and environment hashes matched. |

## Reopen Condition

Resume after placeholder-free bodies exist for the eleven frozen SAT and Cook-Levin packages, or
after an immutable compatible Lean 4 proof already in the pinned closure can be exact-type checked,
transported to the frozen TM2 encodings, and provenance-audited without changing the dependency
lock.

This is current-base, warm-cache, nonrelease blocker evidence only. It does not satisfy
`S56-M-0721-PROOF`, change scheduler state, close either terminal package or the root, or claim
audit completion, theorem completion, validation, release, receipt acceptance, or master acceptance.
