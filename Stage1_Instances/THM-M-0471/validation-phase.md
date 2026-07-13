# THM-M-0471 validation-phase handoff

Item: `S56-M-0471-VALIDATION`. Base revision:
`f023dbc3411d83201065d1a1156d7406b81135d4` (tree
`3b3a73ec19293a2a9b8d9c7e67f0d25da2a511b4`).

The narrow structured recipe freshly elaborates the frozen statement, both conditional
composition certificates, the proof-phase exact roots and supporting declarations, and a
separately written exact-root reconstruction. `Validation.lean` imports neither `Proof` nor
`ObligationTree`; it reconstructs the same natural-number prime-list target directly with the
pinned `Nat.primeFactorsList` family. This is useful same-worker differential evidence, not a
distinct-runner attestation or a second terminal proof body.

Every observed axiom set is contained in `propext`, `Classical.choice`, and `Quot.sound`; the two
proof roots and differential root report exactly that set. The runner also checks the frozen
18-obligation machine denominator, proof receipt, typed proof reachability, prohibited constructs,
pinned mathlib commit/tree/cleanliness/remote/license, and direct source, body-slice, and `.olean`
hashes for `Mathlib/Data/Nat/Factors.lean` and `Mathlib/Data/List/Prime.lean`.

## Commands and exact results

Commands ran on 2026-07-13 (`Asia/Shanghai`).

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0471
  exit 0: rank 1353, planned, legacy artifacts unaccepted, theorem_complete=false

git status --short --untracked-files=all
  exit 0: before owned work, only the automation-provided canonical Formalizations/Lean/.lake
  symlink was untracked; this is a dirty nonrelease worker checkout

bash Stage1_Instances/THM-M-0471/check_validation.sh
  exit 0: read-only-host, network-denied temporary replay elaborated Statement, ObligationTree,
  Proof, and Validation; 24 proof declarations plus the differential root were sorry-free; exact
  roots had the allowlisted axiom closure; deterministic stdout SHA-256 was
  97ce534ac3d2011dcd3210c0e39711c53181e7cb5462e3ca9e751799a0f4999c

python3 -B Stage1_Instances/THM-M-0471/check_obligation_tree.py
  exit 1: the predecessor recipe is snapshot-bound to its obligation-tree base revision and fails
  closed after integration; its artifacts are hash-bound here but its stale receipt is not replayed

python3 -B Stage1_Instances/THM-M-0471/check_proof.py
  exit 1: the predecessor checker is snapshot-bound to its proof worker packet/base and fails
  closed on this validation snapshot; the underlying Lean proof is freshly replayed instead

python3 -B Stage1_Instances/THM-M-0471/check_validation.py
  exit 0: exact/differential kernel replay, observed trust, selected provenance, input freshness,
  fail-closed predecessor-recipe status, receipt, and worker packet passed

python3 -m json.tool Stage1_Instances/THM-M-0471/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-0471/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0: all three validation JSON artifacts parsed

PYTHONPYCACHEPREFIX=/tmp/stage1-m0471-validation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-0471/check_validation.py
  exit 0

rg -n '\b(sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|^[[:space:]]*(axiom|constant|opaque|unsafe)\b' \
  Stage1_Instances/THM-M-0471 --glob '*.lean'
  exit 1 with empty output: pass; no prohibited construct found

git diff --check -- Stage1_Instances/THM-M-0471 .stage1-worker-selftest.json
plus direct newline/trailing-whitespace checks over every validation-phase file
  exit 0: no whitespace errors
```

The script invokes the pinned Lean 4.29.0 executable through `lake env lean` while fixing
`LEAN_PATH` to explicit pre-existing compiled-library paths, so Lake performs no manifest
resolution. Resolving the full manifest previously materialized an absent, unrelated `flt-regular`
package. Each Lean subprocess runs with fixed locale/timezone, a read-only host root, only a fresh
temporary directory writable, and no network namespace. No `lake update`, `lake build`, clone/fetch,
network request, or `.lake` write was performed by this validation phase. The shared warm cache
remains performance evidence only, not section 10.6 hermetic evidence.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | Exact statement, two compositions, proof roots, supporting declarations, and differential root freshly elaborate. |
| Placeholder/unsafe | pass | Lean sorry checks and comments-stripped scans of target modules and selected terminal sources pass. |
| Trust observation | provisional pass | Exact roots report precisely `propext`, `Classical.choice`, and `Quot.sound`; helpers report subsets. |
| Selected provenance | pass | Frozen hashes, clean pinned mathlib commit/tree, official remote, source blobs/body slices/compiled artifacts, and license agree. |
| Dependency acceptance | fail closed | The proof receipt is worker-provisional `[_]`, not master-accepted `[x]`. |
| Predecessor recipe freshness | fail closed | Snapshot-bound obligation/proof checkers reject the integrated validation tree; no stale receipt is relabeled as fresh evidence. |
| Complete trust/provenance | fail closed | `M0471-S-FOUNDATION` and `M0471-X-PROVENANCE`, full declaration/import closure, compiler/bootstrap/plugin TCB, and SBOM remain open. |
| Hermetic reproduction | fail closed | The canonical shared warm `.lake` was reused; no new clean checkout, empty-cache bootstrap, offline archive restoration, or deterministic release bundle exists. |
| Independent verification | fail closed | The differential module ran under this worker, checkout, and cache and shares the same terminal bodies; there is no distinct signed runner or independently implemented minimal verifier. |

This validation node is genuinely self-tested as provisional, fail-closed worker evidence. The
accepted instance stays `[H1, M3, R4]` with no accepted closed obligation or receipt. The first node
gate is proof dependency master acceptance; the first release-specific gate is the section 10.6
empty-cache cold bootstrap. Primary-source `H0`, independently reviewed readable `R0`, complete
provenance/trust, deterministic evidence, `AUDIT-Z`, `THEOREM-Z`, release, and master acceptance
remain open; audit and theorem completion remain false.
