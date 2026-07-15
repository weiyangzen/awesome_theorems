# THM-M-0353 validation-phase evidence

Item: `S56-M-0353-VALIDATION`. Base revision:
`b8c0a0c119a82ef435e23f9ff85bfd783db95736`.

Structured-recipe probe completed at `2026-07-15T16:52:53+08:00` (`Asia/Shanghai`).

## Verdict

`blocked_after_self_test_pending_master_acceptance`. The exact frozen Hermite root, byte-identical
vendored source, local complex adapter, and a separately composed exact root elaborate from copied
sources with fresh target outputs at `--trust=0 -t0`. The complete recorded recipe runs under
Bubblewrap with a read-only host root, private `/tmp`, fixed locale/timezone/thread count, and no
network. Six proof-phase declarations and the differential root are sorry-free. Both exact roots
report precisely `propext`, `Classical.choice`, and `Quot.sound`. Lean's root-closure inspection
covers 54,765 declarations across 1,742 modules and reports no unexpected bodyless nonaxiom or
unsafe declaration.

Selected provenance checks bind the local source, upstream revision/tree/blob/archive, byte identity,
Apache-2.0 license, tool identities, and clean pinned mathlib checkout. This remains nonrelease
evidence. The proof prerequisite is only `[_]`; the accepted root remains `[H1, M4, R4]`, with no
accepted receipt or obligation closure. The shared warm `.lake` artifacts are not an empty-cache
cold build, and the differential root shares the proof helpers, worker, checkout, toolchain, vendor
body, and cache. It is not an independent verifier. `audit_complete=false` and
`theorem_complete=false`.

## Route boundary

The frozen obligation graph models completeness through weighted polynomial density. The current
vendored proof establishes real completeness through Gaussian moments and Fourier uniqueness, then
the local adapter reduces the complex case to real and imaginary parts. The exact root replay passes,
but this validation worker does not rewrite or award closure to that unreconciled prerequisite graph.
Its authoritative open cut remains `M0353-P-MEMLP` and `M0353-P-BASIS`.

## Commands and results

All checks reuse the automation-provided pinned `.lake` artifacts without update, build, clone,
fetch, or repair.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0353` | 0 | Rank 846; planned, L0/rework-required, theorem incomplete. |
| `python3 -I -B Stage1_Instances/THM-M-0353/check_statement.py` | 0 | Frozen statement components, source SHA-256, and four structural mutations passed. |
| `python3 -I -B Stage1_Instances/THM-M-0353/check_obligation_tree.py` | 0 | Frozen 16-obligation registry and 76 typed edges passed; root remained open. |
| `python3 -I -B Stage1_Instances/THM-M-0353/build_vendor_manifest.py --check` | 0 | Byte-identical 99,106-byte vendor source, upstream identities, license, and pinned environment passed. |
| `bash Stage1_Instances/THM-M-0353/check_proof.sh` | 0 | Disposable trust-zero proof replay passed; six declarations sorry-free with the exact observed axiom set. |
| structured Bubblewrap argv in `validation-spec.json --probe` | 0 | Network-isolated trust-zero replay, 54,765-declaration closure inspection, selected provenance, and fail-closed decisions passed. |
| structured Bubblewrap argv in `validation-spec.json` | 0 | Final receipt, worker packet, kernel/trust/provenance observations, and fail-closed decisions passed. |
| `python3 -m json.tool Stage1_Instances/THM-M-0353/validation-spec.json` | 0 | Structured argv recipe parsed. |
| `python3 -m json.tool Stage1_Instances/THM-M-0353/validation-receipt.json` | 0 | Node-specific receipt parsed. |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | Worker handoff parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0353-validation-pycache python3 -m py_compile Stage1_Instances/THM-M-0353/check_validation.py` | 0 | Validator compiled outside the repository tree. |
| `git diff --check -- Stage1_Instances/THM-M-0353 .stage1-worker-selftest.json` | 0 | No scoped whitespace diagnostics after final artifacts. |

The inherited `check_proof.py` is not replayed as current validation evidence: it intentionally pins
the earlier proof worker's base revision and packet. This validation checker independently binds the
current base, proof and vendor inputs, proof receipt, canonical target, pinned tools/dependencies,
and authoritative validation item. The predecessor `check_proof.sh` remains a real replay because it
is source-copying and snapshot-agnostic.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel replay | provisional pass | Statement, composer, vendored source, proof bodies, exact root, and differential composition elaborate from copied sources with fresh outputs at trust zero. |
| Placeholder and unsafe boundary | provisional pass | Parser-aware source scan, `assert_no_sorry`, `#print sorries`, and Lean closure inspection find no prohibited device or unexpected bodyless/unsafe declaration. |
| Selected provenance | provisional pass | Frozen sources, upstream identities, byte identity, Apache-2.0 license, tool digests, and clean mathlib pin agree. Full transitive origin closure is absent. |
| Dependency authority | fail closed | `S56-M-0353-PROOF` is not master accepted; accepted receipts and obligation closure remain empty. |
| Frozen composition | fail closed | The frozen weighted-density route is not reconciled with the vendored moments/Fourier-uniqueness route. |
| Complete trust/provenance | fail closed | No accepted theorem-specific foundation profile, full transitive declaration/source/compiled-artifact TCB inventory, or SBOM exists. |
| Hermetic release | fail closed | Shared warm `.lake`; no clean checkout, empty-cache cold bootstrap, offline-restorable archive, or deterministic release bundle. |
| Independent verification | fail closed | The validation root shares helpers, worker, checkout, toolchain, vendor body, and cache; no distinct signed runner or independently implemented minimal verifier exists. |

The first node failure is `dependency.S56-M-0353-PROOF.master_acceptance`. The first release failure
is `S56-10.6-HERMETIC-COLD-EMPTY-CACHE`. This genuinely self-tested validation implementation
proposes only worker state `[_]`; it grants no accepted `M0-P`, release-grade `E0/E1`, `H0`, `R0`,
`AUDIT-Z`, `THEOREM-Z`, release, or theorem-completion credit.
