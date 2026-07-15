# THM-M-1356 proof blocker at `3631c5c1` (slot56)

Item: `S56-M-1356-PROOF`

Intent: `prove`

Recorded: `2026-07-15T20:50:14+08:00` (`Asia/Shanghai`)

Base revision: `3631c5c14fbe46cb219d7fb03b5a64c50782e8f0`

Base tree: `640bca710e5550b90f0727860958561186ccb51f`

## Verdict

`blocked`. No placeholder-free all-degree Lean body or compatible immutable
import is available for the exact target
`Stage1Instances.THM_M_1356.RouthHurwitzTarget`. The proof item remains `[ ]`,
the lifecycle remains `planned`, and the authoritative instance vector remains
`[H1, M4, R4]`. The provisional frozen-registry vector is `[H1, M3, R4]`.
Neither vector advances. Audit completion and theorem completion are false.

The target quantifies over every positive degree and states strict
left-half-plane stability iff every finite leading Hurwitz minor is positive.
`ObligationTree.lean` only assembles the two all-degree directions supplied as
premises. `Proof.lean` contains genuine placeholder-free proofs of the exact
degree-one adapter, root characterization, minor formula, and equivalence, but
that specialization closes no frozen arbitrary-degree obligation and cannot
satisfy this phase.

The frozen registry contains 50 obligations, 45 machine-required. All 45
required `terminal_proof_body_id` fields remain null. The exact root cut is:

```text
M1356-B-STABLE-TO-MINORS
M1356-B-MINORS-TO-STABLE
```

## Failed Gates

The first workflow gate fails because `S56-M-1356-OBLIGATION_TREE` is only
worker-provisional `[_]`, not master-accepted `[x]`. Its scoped checker also
hard-pins base `431e77db6367a2eda83060b7212cb490d11ca39f` and rejects current
HEAD at that freshness assertion before substantive validation.

Independently, the first proof-content gate fails at exact arbitrary-degree
proof-body availability. The frozen route still lacks checked bodies for the
alternating even/odd construction, signed Euclidean/Sturm sequence, Hermite
hodograph and Cauchy-index bridges, regular and nonregular Routh cases,
no-pivot Hurwitz-matrix elimination, and the leading-minor product identity.
A bounded scan of pinned mathlib and `flt-regular` found no named exact
terminal. The previously audited `PerAlexandersson/RealRooted` near-candidate
contains explicit `sorry` in root-critical declarations, uses a different
toolchain, and states a materially different weak infinite-matrix criterion.
It receives no proof or integration credit.

This is another unresolved root-sized execution. The authoritative DAG still
records `attempts: 0` and `children: []`, which this worker may not edit. The
integration lane must reconcile the accumulated attempt evidence and apply
the rev-5.6 five-tick split rule if its actual scheduler count has reached the
threshold. A further retry should be assigned to a dependency-legal frozen
leaf rather than redispatching the entire root unchanged.

## Narrow Validation

All commands ran in this worker clone. The pre-existing untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts was
reused read-only. Lean sources and objects for the replay were isolated under
`/tmp` and removed. No `lake update`, `lake build`, dependency clone/fetch,
checkout, or `.lake` mutation was performed. The untracked symlink makes this
warm, dirty, nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique targets, ranks 1 through 1546, passed. |
| `python3 scripts/stage1_target.py show THM-M-1356` | 0 | Rank 966; planned; L0/rework-required; theorem incomplete. |
| `python3 -B Stage1_Instances/THM-M-1356/check_statement.py` | 0 | Expression SHA-256 `7901eb74...98bf`; four mutations distinguished; all three import-deletion probes rejected; pinned mathlib revision agreed. |
| `python3 -B Stage1_Instances/THM-M-1356/check_anchor_audit.py` | 0 | Exact local statement only; pinned-mathlib and external terminal inventories empty; provisional root `M3`. |
| `python3 -B Stage1_Instances/THM-M-1356/check_obligation_tree.py` | 1 | Stopped at the stale hard-pinned base-revision assertion before substantive checks. |
| Isolated `lake env lean --trust=0 -t0` replay of `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` | 0 | All modules elaborated; local bodies reported exactly `propext`, `Classical.choice`, and `Quot.sound`. |
| Comment/string-stripped prohibited-construct scan of the three replayed Lean modules | 0 | No `sorry`, `admit`, `sorryAx`, custom axiom/constant, unsafe/oracle, `native_decide`, `implemented_by`, or `run_tac` marker was found. |
| Exact-topic `rg` over pinned mathlib and `flt-regular`, and separately over repo-local Lean outside this dossier | 1 each | Expected no-match; no named exact all-degree candidate was found. |
| Registry and typed-graph `jq` queries | 0 | 50 obligations, 45 machine-required, all 45 required terminal IDs null, and 335 typed edges. |
| Pinned package revision/tree/status checks | 0 | mathlib `8a178386...ea95` / `bdc39a31...c2b`; `flt-regular` `56161b6e...1a27` / `32c9eace...c893`; both tracked-clean. |

The isolated replay produced these SHA-256 values:

| Output | SHA-256 |
|---|---|
| `Statement.olean` | `f847976776294835e9bb566c18d105573dd5494214c2ebb9b42dcd01d0fb3cf4` |
| `ObligationTree.olean` | `4b3dc2ef06d9f678ce5505f1a4e40c2b80dd1deb4f61d7651d4ee6d816021e4d` |
| `Proof.olean` | `dbd13ed0e7e38a5d548ba82675fd586ec9371180a772dda7f1adca99b3be66cf` |

Pinned identities were Lean 4.29.0 commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake
`5.0.0-src+98dc76e`, mathlib commit/tree
`8a178386ffc0f5fef0b77738bb5449d50efeea95` /
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`, and `flt-regular`
commit/tree `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` /
`32c9eace926573a9981787ae97643e520353c893`.

## Retry Boundary

First reconcile and accept or refresh the obligation-tree prerequisite. Then
implement dependency-legal frozen leaves without placeholders, derive both
exact all-degree direction packages, and compose them to the unchanged root.
Alternatively, integrate an immutable, license-compatible exact Lean 4
terminal only after type, dependency, provenance, placeholder, axiom, and
trust checks pass in the pinned environment.

This artifact is current-base target-scoped blocker evidence only. It does not
satisfy `S56-M-1356-PROOF`, propose `[_]`, close an obligation or the root,
change scheduler state, or claim proof completion, audit completion, theorem
completion, validation, release, receipt acceptance, or master acceptance.
Because the assigned phase is not genuinely complete,
`.stage1-worker-selftest.json` is deliberately absent.
