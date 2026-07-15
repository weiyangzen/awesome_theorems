# THM-M-1356 proof-phase recheck at `471e4458` (slot56)

Item: `S56-M-1356-PROOF`

Intent: `prove`

Recorded: `2026-07-15T20:33:47+08:00` (`Asia/Shanghai`)

Base revision: `471e4458269351ee096972776c478d019941b679`

Base tree: `e30e1cefce39148420ccc4525b726d57f58ee94b`

## Verdict

`blocked`. No eligible placeholder-free Lean 4 body was implemented or found
for the exact all-degree root
`Stage1Instances.THM_M_1356.RouthHurwitzTarget`. The proof item remains `[ ]`,
the lifecycle remains `planned`, and no frozen obligation closes. The
authoritative instance vector remains `[H1, M4, R4]`; predecessor worker
artifacts provisionally propose `[H1, M3, R4]`, but no master receipt accepted
that proposal.

The existing `Proof.lean` remains genuine partial work. Its four trust-clean
declarations prove the exact degree-one coefficient adapter, root
characterization, unique Hurwitz minor, and stability/minor equivalence. A
fresh trust-zero replay and `assert_no_sorry` probes passed. The canonical
target quantifies over every positive degree, however, so this specialization
closes none of the 45 machine-required obligations and cannot satisfy this
phase.

The conditional declarations in `ObligationTree.lean` consume both complete
all-degree implications as explicit premises; they prove neither implication.
The two exact root-cut nodes remain:

- `M1356-B-STABLE-TO-MINORS`
- `M1356-B-MINORS-TO-STABLE`

Their missing implementation frontier includes the alternating even/odd
construction, signed Euclidean and Sturm sequences, Hermite hodograph and
Cauchy-index bridges, regular and five nonregular Routh cases, Hurwitz-block
elimination, and the leading-minor product identity. Bounded repo-local and
pinned dependency searches found no named exact terminal. The previously
audited immutable `PerAlexandersson/RealRooted` near-candidate remains
ineligible because its root-critical declarations contain explicit `sorry`
and its infinite total-nonnegativity/right-half-plane interface differs from
the frozen finite strict-minor target.

## Workflow Boundary

The first workflow failure is prerequisite acceptance and freshness:
`S56-M-1356-OBLIGATION_TREE` remains worker-provisional rather than master
accepted, and its checker rejects current HEAD at its stale hard-pinned base
revision before substantive checks. Independently, the first proof-content
failure is the absence of an exact arbitrary-degree engine upstream of both
directional cuts.

Three prior target-scoped proof evidence groups are integrated: the original
degree-one proof/blocker record and two later blocker rechecks. This is a
fourth unresolved evidence group, while the authoritative DAG still says zero
attempts and no children. Artifact groups alone do not establish scheduler
execution-tick count. The integration lane must reconcile that drift and apply
section 10.2 if five unresolved execution ticks are confirmed. The current
frozen leaf frontier is recorded in the companion JSON; this worker does not
edit scheduler authority or invent unapproved children.

No material THM-M-1356 proof input changed after the preceding integrated
recheck. Since comparison base `12d9becb`, the blueprint and DAG changed only
for unrelated theorem IDs.

## Narrow Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink to the
canonical pinned artifacts was reused read-only. No `lake update`, `lake
build`, dependency clone/fetch, network operation, or `.lake` mutation was
performed. Temporary Lean outputs were isolated under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique ordered targets passed. |
| `python3 scripts/stage1_target.py show THM-M-1356` | 0 | Rank 966; lifecycle `planned`; L0/rework-required; theorem incomplete. |
| `timeout --foreground --kill-after=10s 600s env LEAN_NUM_THREADS=1 python3 -B Stage1_Instances/THM-M-1356/check_statement.py` | 0 | Expression SHA-256 `7901eb74...98bf`; four mutations distinguished; three minimal-import deletion probes failed as required; mathlib pin agreed. |
| `python3 -B Stage1_Instances/THM-M-1356/check_anchor_audit.py` | 0 | Exact local statement only; pinned-mathlib topic inventory and external terminal-candidate inventory empty; provisional root `M3`. |
| `python3 -B Stage1_Instances/THM-M-1356/check_obligation_tree.py` | 1 | The predecessor checker stopped at its stale hard-pinned base revision `431e77db...`; this is a freshness failure, not Lean proof evidence. |
| Isolated `lake env`-selected Lean replay with `--trust=0 -t0`, followed by `assert_no_sorry` probes | 0 | `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` elaborated. Each degree-one declaration reported exactly `[propext, Classical.choice, Quot.sound]`; `Proof.olean` SHA-256 was `dbd13ed0...e66cf`, and the replay-log SHA-256 was `80069c16...aefc`. |
| Comment/string-stripped prohibited-construct scan of `Proof.lean` | 0 | No placeholder, bodyless declaration, unsafe/oracle construct, or prohibited proof device was found. |
| Bounded exact-topic scan over repo-local and pinned Lean source | 0 wrapper, 1 expected per lane | Both lanes produced the expected no-match result; no exact all-degree candidate was found. |
| Frozen registry and typed-graph queries | 0 | 50 obligations, 45 machine-required, all 45 required terminal IDs null, and 335 typed edges. |
| Pinned package revision/tree/status and Lean/Lake version checks | 0 | Mathlib `8a178386...ea95` / `bdc39a31...c2b`; flt-regular `56161b6e...1a27` / `32c9eace...c893`; both tracked-clean; Lean 4.29.0 and Lake 5.0.0. |

Exact input hashes, full command summaries, environment identities, cut set,
candidate classification, known failures, retry condition, and attempt-ledger
boundary are recorded in the companion JSON.

This is current-base durable blocker evidence only. It does not satisfy
`S56-M-1356-PROOF`, propose `[_]`, close an obligation or the root, change
scheduler state, or claim audit completion, theorem completion, validation,
release, receipt acceptance, or master acceptance. Because the phase is not
genuinely complete, `.stage1-worker-selftest.json` is deliberately absent.
