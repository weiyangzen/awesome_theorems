# THM-M-0319 validation-phase evidence

Item: `S56-M-0319-VALIDATION`. Base revision:
`8d6ac2078d37dc107d80c38c020de01c6f9affce`.

Final structured-recipe interval: `2026-07-15T15:08:47+08:00` to
`2026-07-15T15:11:04+08:00` (`Asia/Shanghai`).

## Verdict

`blocked_after_self_test_pending_master_acceptance`. The exact frozen Brouwer root, its local proof
declarations, all three vendored modules, and a separately spelled exact-root composition elaborate
at `--trust=0` in a fresh temporary output tree. Every Lean process runs with fixed locale,
timezone, and one thread under Bubblewrap network isolation and a read-only host root. Both exact
roots are sorry-free and use exactly `propext`, `Classical.choice`, and `Quot.sound`. Lean's
dependency-closure inspection covers 21997 declarations in 869 modules and reports no unexpected
bodyless nonaxiom or unsafe declaration. Frozen local and vendor hashes, reversible upstream
reconstruction, the MIT license, tool identities, and the clean pinned mathlib checkout agree.

This is deliberately nonrelease evidence. The proof prerequisite is only `[_]`, the accepted root
vector stays `[H1, M4, R4]`, and accepted closure stays empty. The separately written validation
root bypasses `brouwerFixedPoint` but consumes the same three local proof helpers, so it is neither
proof-independent nor a distinct verifier. The shared warm `.lake` artifacts are not an empty-cache
cold build. `audit_complete=false` and `theorem_complete=false`.

## Frozen route mismatch

The prerequisite obligation registry and typed graph model the earlier unintegrated Harfe/cube
route and keep `M0319-T-EXTERNAL` open. The proof instead uses an MIT-licensed simplex Brouwer
theorem, a finite partition of unity, and compact displacement minimization. The validator confirms
the exact new root but assigns no obligation closure because the architecture owner has not
reconciled and refrozen that route. This worker changes no prerequisite artifact or authoritative
state.

## Commands and results

All checks reuse the automation-provided pinned `.lake` artifacts without update, build, clone,
fetch, or mutation.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0319` | 0 | Rank 685; planned, L0/rework-required, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0319/check_statement.py` | 1 | Inherited checker calls the top-level Lake graph and is blocked by the pre-existing incomplete `flt-regular` checkout; the validation recipe independently replays the hash-bound statement from source. |
| `python3 Stage1_Instances/THM-M-0319/check_anchor_audit.py` | 1 | Same inherited top-level Lake blocker; structured anchor inputs remain hash-bound, but this command supplies no new passing evidence. |
| `python3 Stage1_Instances/THM-M-0319/check_obligation_tree.py` | 0 | Frozen 12-obligation registry and 31 typed edges passed with its root still open. |
| `python3 -I -B Stage1_Instances/THM-M-0319/build_vendor_manifest.py` | 0 | Three vendored files, reversible compatibility edits, bytes, hashes, license, and closure totals passed. |
| `bash Stage1_Instances/THM-M-0319/check_proof.sh` | 0 | Disposable trust-zero exact-root proof replay passed with all seven declarations sorry-free and the exact observed axiom set. |
| structured Bubblewrap argv in `validation-spec.json` | 0 | The entire Python recipe and every Lean child were network-isolated; trust-zero replay, closure inspection, selected provenance, receipt binding, and fail-closed decisions passed. |
| `python3 -m json.tool Stage1_Instances/THM-M-0319/validation-spec.json` | 0 | Structured argv recipe parsed. |
| `python3 -m json.tool Stage1_Instances/THM-M-0319/validation-receipt.json` | 0 | Node-specific validation receipt parsed. |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | Worker handoff parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0319-validation-pycache python3 -m py_compile Stage1_Instances/THM-M-0319/check_validation.py` | 0 | Validator compiled outside the repository tree. |
| `git diff --check -- Stage1_Instances/THM-M-0319 .stage1-worker-selftest.json` | 0 | No scoped whitespace diagnostics. |

The inherited `check_proof.py --require-receipt` is not validation evidence: it is snapshot-bound
to the old proof-worker base and expects the proof DAG node to remain `[ ]`, while integration has
correctly advanced it to `[_]`. The validation checker independently hash-binds the current base,
all proof and vendor inputs, proof receipt, canonical target, pinned dependency/tool identities, and
the authoritative validation item.

The statement and anchor checker failures are infrastructure-local, not kernel counterexamples:
both hard-code `lake env lean` at the top-level project, whose automation-provided `flt-regular`
checkout lacks a resolvable `HEAD`. Fetching, rebuilding, deleting, or repairing `.lake` is forbidden
for this worker. The validation recipe therefore selects the pinned Lean binary through the clean
mathlib Lake project and constructs `LEAN_PATH` only from existing artifacts, exactly as the accepted
proof recipe does.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel replay | provisional pass | Statement, frozen conditional interfaces, all vendor and local proof bodies, exact root, and differential composition elaborate from copied sources with fresh outputs at trust zero. |
| Placeholder and unsafe boundary | provisional pass | Nested-comment/string-aware scans, `assert_no_sorry`, `#print sorries`, and Lean closure inspection find no prohibited proof device or unexpected bodyless/unsafe declaration. |
| Selected provenance | provisional pass | Local inputs, vendor manifest, reconstructed upstream hashes, compatibility patch, MIT license, mathlib pin, and executable identities agree. Full transitive origin closure is absent. |
| Dependency authority | fail closed | `S56-M-0319-PROOF` is not master accepted; accepted receipts and accepted obligation closure remain empty. |
| Frozen composition | fail closed | The frozen Harfe/cube route does not represent the actual simplex/partition-of-unity proof. `M0319-T-EXTERNAL` remains the authoritative open cut. |
| Complete trust/provenance | fail closed | No accepted theorem-specific foundation profile, full transitive declaration/source/compiled-artifact TCB inventory, or SBOM exists. |
| Hermetic release | fail closed | Shared warm `.lake`; no clean checkout, empty-cache cold bootstrap, offline-restorable archive, or deterministic release bundle. |
| Independent verification | fail closed | The validation root shares proof helpers, worker, checkout, toolchain, and cache; no distinct signed runner or independently implemented minimal verifier exists. |

The first node failure is `dependency.S56-M-0319-PROOF.master_acceptance`. The first release failure
is `S56-10.6-HERMETIC-COLD-EMPTY-CACHE`. This genuinely self-tested validation implementation
proposes only worker state `[_]`; it grants no accepted `M0-L/M0-P`, release-grade `E0/E1`, `H0`,
`R0`, `AUDIT-Z`, `THEOREM-Z`, release, or theorem-completion credit.
