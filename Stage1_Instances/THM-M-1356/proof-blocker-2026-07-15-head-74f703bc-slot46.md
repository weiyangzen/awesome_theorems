# THM-M-1356 proof blocker at `74f703bc` (slot46)

Item: `S56-M-1356-PROOF`

Intent: `prove`

Recorded: `2026-07-15T22:50:58+08:00` (`Asia/Shanghai`)

Base revision: `74f703bc3ca0b461dc2ec899f534422bd75393b8`

Base tree: `0ceaa9e760f5f8e11dd94a165f1efd19c017e184`

## Verdict

`blocked`. No eligible placeholder-free Lean 4 body or compatible pinned
import was implemented or found for the exact arbitrary-degree target
`Stage1Instances.THM_M_1356.RouthHurwitzTarget`. The proof item remains `[ ]`,
the lifecycle remains `planned`, and no frozen obligation closes.

The authoritative `instance.json` vector remains `[H1, M4, R4]`. The
statement, anchor-audit, and obligation-tree worker artifacts provisionally
propose `[H1, M3, R4]`, but no master acceptance reconciles that proposal.
This execution changes neither vector.

`Proof.lean` is genuine partial work. Its four trust-clean declarations prove
the exact degree-one polynomial adapter, root characterization, unique
Hurwitz minor, and stability/minor equivalence. The canonical target
quantifies over every positive degree, so that specialization closes none of
the frozen arbitrary-degree obligations and cannot satisfy this phase.

## Failed Gates

The first workflow failure is prerequisite acceptance and freshness.
`S56-M-1356-OBLIGATION_TREE` remains worker-provisional `[_]`, not
master-accepted `[x]`, and its checker stops at stale hard-pinned revision
`431e77db...` before substantive validation. The target-local task DAG also
retains intake-era `open` states and attempt counts, while the authoritative
DAG records provisional predecessor work. This proof worker cannot reconcile
or promote either authority.

Independently, the first proof-content failure is the absence of an all-degree
engine upstream of both exact directional cuts:

- `M1356-B-STABLE-TO-MINORS`
- `M1356-B-MINORS-TO-STABLE`

The frozen registry has 50 obligations, 45 machine-required obligations, and
all 45 required terminal body IDs remain null. More sharply, 40 of the 45
required nodes have only `planned:v1` fingerprints and prose signatures, not
exact Lean propositions. They cannot honestly receive terminal closure until
an append-only registry delta freezes checked exact interfaces.

The missing implementation frontier comprises the even/odd split, signed
Euclidean and Sturm construction, Hermite hodograph and Cauchy-index bridges,
regular and nonregular Routh cases, and the Hurwitz elimination/minor-product
engine. Pinned mathlib provides useful substrate such as
`Matrix.det_updateRow_add_smul_self`, `Matrix.det_of_upperTriangular`,
polynomial gcd/root lemmas, and degree-reducing remainder lemmas, but no exact
Routh-Hurwitz terminal or frozen leaf implementation.

The nearest recorded external source,
`PerAlexandersson/RealRooted@634a949d31683785b4181efbba6faff31e81e006`,
is ineligible. Its root-critical Hermite-Biehler, Hurwitz-matrix, and
Veronese-section declarations contain explicit `sorry`; it also uses a weak
right-half-plane and infinite total-nonnegativity interface rather than the
frozen finite strict-leading-minor equivalence.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink was
reused read-only. No `lake update`, `lake build`, dependency clone/fetch,
checkout, or `.lake` mutation was performed. Temporary Lean outputs were
isolated under `/tmp` and removed. This is warm, dirty nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique ordered targets passed. |
| `python3 scripts/stage1_target.py show THM-M-1356` | 0 | Rank 966; lifecycle `planned`; L0/rework-required; theorem incomplete. |
| `timeout --foreground --kill-after=10s 600s env LEAN_NUM_THREADS=1 python3 -B Stage1_Instances/THM-M-1356/check_statement.py` | 0 | Expression SHA-256 `7901eb74...98bf`; four mutations distinguished; three import-deletion probes failed as required; pinned mathlib revision agreed. |
| `python3 -B Stage1_Instances/THM-M-1356/check_anchor_audit.py` | 0 | Exact local statement only; pinned-mathlib and external terminal inventories empty; provisional root `M3`. |
| `python3 -B Stage1_Instances/THM-M-1356/check_obligation_tree.py` | 1 | Stopped at stale hard-pinned base revision `431e77db...`; this is a predecessor freshness failure, not proof evidence. |
| `jq -r '.replay_recipe' Stage1_Instances/THM-M-1356/proof-recheck-2026-07-15-head-5544f999-slot52.json \| bash` | 0 | Trust-zero replay elaborated `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and `assert_no_sorry` probes. The three main olean hashes remained `f8479767...3cf4`, `4b3dc2ef...21e4`, and `dbd13ed0...66cf`. |
| `jq -r '.prohibited_construct_scan' Stage1_Instances/THM-M-1356/proof-recheck-2026-07-15-head-5544f999-slot52.json \| bash` | 0 | No placeholder, bodyless declaration, unsafe/oracle construct, or prohibited proof device occurred outside comments and strings in `Proof.lean`. |
| Bounded exact-topic `rg` over repo-local source and all 7903 pinned Lean sources | 0 wrappers; 1 expected per lane | Both lanes produced the expected no-match result; no exact all-degree candidate was found. |
| Frozen registry and graph queries | 0 | 50 obligations; 45 machine-required; all 45 required body IDs null; 40 planned fingerprints; five exact expression/interface fingerprints; 335 typed edges. |
| Pinned package revision/tree/status and Lean/Lake checks | 0 | Mathlib `8a178386...ea95` / `bdc39a31...c2b`; flt-regular `56161b6e...1a27` / `32c9eace...c893`; both tracked-clean; Lean 4.29.0 and Lake 5.0.0. |
| Material-input diff and extracted target-projection hashes against `e6872c19...` | 0 | No material target or pin input changed; target-specific blueprint and DAG projections are byte-stable after canonical extraction. |
| Direct `lake env lean` on `Proof.lean` without ordered local module setup | 1 | Expected command-shape diagnostic: local `Statement` was absent from the search path. The recorded isolated ordered replay then passed. |
| `python3 -m json.tool`, target-specific `jq` invariants, and parser-oriented scan of five owned Lean modules | 0 | The blocker parsed; open-state and count invariants passed; no prohibited construct occurred outside comments and strings. |
| No-index whitespace checks on both new blocker artifacts | 1 expected per file | Each new file differed from `/dev/null` and produced no whitespace diagnostic. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The successful replay reports exactly `propext`, `Classical.choice`, and
`Quot.sound` for the existing local declarations. It establishes only the
frozen statement, conditional composition interface, and degree-one bodies;
it is not an arbitrary-degree Routh-Hurwitz proof.

## Scheduler Handoff

At least seven earlier unresolved proof evidence groups are integrated while
the authoritative item still records zero attempts and no children. This is
at least the eighth evidence group, but evidence groups do not establish
scheduler ticks. This worker therefore does not invent an attempt count or
edit scheduler authority. The integration lane must reconcile the ledger and,
if five unresolved ticks are confirmed, split this oversized item before
another whole-root redispatch.

The next dependency-legal action is to accept or repair the predecessor and
freeze exact Lean signatures for the planned frontier through an append-only
registry delta. After that, dispatch proof-ready leaf children rather than the
whole root. The determinant APIs named above are useful footholds for the
Gauss and triangular-determinant branch. An alternative is an immutable,
license-compatible exact Lean 4 terminal that passes type, dependency,
provenance, placeholder, axiom, and trust checks in the pinned closure.

This artifact is a current-base proof blocker, not a proof receipt. It changes
no Lean source, obligation, graph, debt vector, lifecycle, scheduler state, or
accepted receipt and claims no proof-phase completion, audit completion,
theorem completion, validation, release, or master acceptance. Because the
assigned phase is not genuinely complete, `.stage1-worker-selftest.json` is
deliberately absent.
