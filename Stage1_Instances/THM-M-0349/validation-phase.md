# THM-M-0349 validation phase

Item: `S56-M-0349-VALIDATION`. Base revision:
`d5ab961cb3cd92c7febcf21fb9ab746fde231c24`.

## Verdict

`blocked`. The validation implementation is self-tested, but it does not validate the theorem.
The proof predecessor is provisional and closes zero frozen obligations. Its concrete `L2`
conjugate-function contraction has no exact frozen interface for `M0349-L-L2`; it therefore remains
partial progress rather than node closure. The canonical all-`p` root remains open at `[H3, M4,
R4]`, with `audit_complete=false` and `theorem_complete=false`.

The frozen graph's package-level cut is `M0349-P-EXISTENCE` and `M0349-P-BOUND`. The expanded
analytic debt also exposes `M0349-L-WEAK11`, `M0349-L-INTERPOLATE`, `M0349-C-EXTEND`, and
`M0349-L-FOURIER-ID`. Both views are retained; this worker does not reconcile authoritative state.

## Executed Validation

`Validation.lean` imports the proof and obligation modules but adds no mathematical proof. It applies
mathlib's elaborator-aware `assert_no_sorry` checks to all proof-phase declarations and the
conditional root composition, prints the two terminal axiom sets, and traverses their transitive
constant closure for unexpected bodyless or unsafe declarations.

The checker copies `Statement.lean`, `Proof.lean`, `ObligationTree.lean`, and `Validation.lean` to a
fresh `/tmp` directory. Each module is elaborated at `--trust=0 -t0` using the hash-verified pinned
Lean executable. Every Lean invocation runs inside Bubblewrap with a read-only host root, only the
temporary directory writable, a fixed locale/timezone/thread count, and an unshared network
namespace. It uses the existing pinned compiled dependencies without running Lake, updating,
building, cloning, fetching, or mutating `.lake`.

This is fresh-output, network-isolated, warm-cache nonrelease evidence. `Validation.lean` is an
import-dependent audit in this same worker checkout and cache; it is not independent verification.

| Gate | Result |
|---|---|
| Exact target and narrow kernel replay | provisional pass: actual elaborated target fingerprint matches, partial L2 bodies elaborate, and conditional root composition checks at trust zero |
| Placeholder and unsafe observation | provisional pass: 13 `assert_no_sorry` checks plus source and transitive-closure scans find no prohibited local device, unexpected bodyless declaration, or unsafe dependency |
| Axiom observation | exactly `propext`, `Classical.choice`, and `Quot.sound`; this does not create an accepted foundation decision |
| Selected direct provenance | provisional pass: local hashes, proof receipt, clean pinned mathlib revision/tree/origin/license, and `AddCircle` source/blob/olean identities agree |
| Complete trust/provenance | fail closed: accepted foundation policy, full transitive artifact origin, complete TCB inventory, and SBOM remain absent |
| Exact root | fail closed: the L2 mapping and all remaining all-`p` analytic packages are open; zero frozen obligations close |
| Hermetic release | fail closed: dirty worker clone and shared warm dependency cache; no clean checkout, empty-cache cold build, offline restoration, or deterministic release bundle |
| Independent verification | fail closed: same worker, checkout, toolchain, and cache; no second identity/signature, independent runner, or independently implemented release verifier |
| Source/readability | fail closed: primary-source H0 mapping/errata review and independent R0 review remain open |

## Commands And Results

Commands ran on 2026-07-15 (Asia/Shanghai) from the worker root unless noted.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0349` | 0 | rank 842, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0349/check_anchor_audit.py` | 0 | bounded anchor invariants passed; neither related mathlib declaration closes the target |
| `python3 Stage1_Instances/THM-M-0349/check_obligation_tree.py` | 0 | 15 obligations and 69 typed edges passed; frozen root remains open M3 |
| `bash Stage1_Instances/THM-M-0349/check_proof.sh` | 0 | isolated pinned replay checked the concrete L2 candidate and exact allowed axioms |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0349/check_validation.py --probe` | 0 | network-isolated trust-zero replay, exact target fingerprint, trust closure, and selected provenance passed |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0349/check_validation.py --worker-packet .stage1-worker-selftest.json` | 0 | full receipt, blocker, packet, and fail-closed gate decisions passed |
| `python3 -m json.tool ...` for validation JSON and worker packet | 0 | all structured artifacts parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0349-validation-pycache python3 -m py_compile Stage1_Instances/THM-M-0349/check_validation.py` | 0 | validator compiled outside the repository |
| `git diff --check -- Stage1_Instances/THM-M-0349 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The first failed gate is
`dependency.S56-M-0349-PROOF.master_acceptance_and_M0349-L-L2.exact_node_mapping`.
Retry requires master reconciliation of the exact L2 node, complete accepted proof of every
root-critical analytic package and the premise-free all-`p` root, complete trust/source/readability
review, a clean cold offline replay, and distinct signed independent verification.
