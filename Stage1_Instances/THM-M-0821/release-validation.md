# THM-M-0821 release-phase reconciliation

Item: `S56-M-0821-RELEASE`

Base revision: `c45f3c7090cb4adf616d45e5414985f956e807b2`

## Exact verdict

`blocked`. The lifecycle remains `planned`, the accepted root vector remains
`[H1, M3, R4]`, and both `audit_complete` and `theorem_complete` are false.
This worker accepts no receipt and makes no `AUDIT-Z`, `THEOREM-Z`, release, or
theorem-completion claim.

The first failed workflow gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`.
`S56-M-0821-VALIDATION` is only a provisional `[_]` worker projection; its
receipt has `accepted=false` and `release_grade=false`, and it has not been
master accepted. The first release-input failure is
`S56-RELEASE-IMMUTABLE-CLEAN-INPUT`. The next release gate is
`S56-10.6-HERMETIC-COLD-BUILD`.

## Evidence reconciliation

The exact frozen Sperner maximum target has substantive provisional machine
evidence. It requires both an attaining lower-middle-layer antichain and the
universal upper bound, so it is not a weakened upper-bound-only substitution.
`Proof.lean` constructs the witness and invokes pinned mathlib's
`IsAntichain.sperner`; `Validation.lean` imports only the frozen statement and
independently reconstructs the exact same target. The current network-isolated
temporary-directory replay reports eight sorry-free declarations. The proof and
differential declarations use exactly `propext`, `Classical.choice`, and
`Quot.sound`. This supports only a candidate `M0-W` route for later master
reconciliation, not accepted `M0-W`, `E0`, or `E1` evidence.

Structured authority remains weaker and therefore wins. `instance.json` and the
frozen graph stay `planned` at `[H1, M3, R4]`, with `root_closed=false`, no
accepted obligation, and no accepted receipt. The graph records six provisional
package composition certificates, but eight internal LYM source-body
decomposition plans still lack abstract-child certificates and receive no
individual closure credit. Only the master may reconcile these surfaces.

`AUDIT-Z` is blocked independently of machine closure. There is no accepted
primary-source edition/theorem/page/assumption/errata crosswalk with independent
H0 review, nor an independently reviewed R0 structured reconstruction. Release
also lacks an accepted theorem-specific foundation profile, full transitive
provenance and TCB closure, immutable clean input, empty-cache cold build,
network-disconnected offline restoration, complete SBOM and licenses, two
independent signed runner attestations, an independently implemented minimal
verifier, protected CI and mutation evidence, and a deterministic bundle.

## Commands and results

Commands ran from the worker root on 2026-07-14 (Asia/Shanghai). The
automation-provided pinned `.lake` link was reused without mutation. No
`lake update`, `lake build`, clone, fetch, checkout, dependency mutation, or
network request ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique targets and ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0821` | 0 | Rank 1379 remains planned, L0/rework-required, and theorem-incomplete. |
| `bash Stage1_Instances/THM-M-0821/check_validation.sh` | 0 | Exact proof root, six frozen compositions, and separate exact differential root elaborated in a network-isolated temporary directory; eight declarations were sorry-free with the recorded axiom profile; stdout SHA-256 `2f60f518d7193b8826f907c7d251fbf7731ca30ad7bdad8439ef1958eb0e05a6`. |
| `python3 -B Stage1_Instances/THM-M-0821/check_release.py` | 0 | Reconciled hashes, authority, receipts, graph, narrow Lean evidence, and every negative release gate; derived the exact blocked verdict. |
| `PYTHONOPTIMIZE=1 python3 -B Stage1_Instances/THM-M-0821/check_release.py` | 1 (expected) | The fail-closed guard rejected execution with Python assertions disabled. |
| `python3 -m json.tool` on the three release JSON files and `.stage1-worker-selftest.json` | 0 | All structured artifacts parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0821-release-pycache python3 -m py_compile Stage1_Instances/THM-M-0821/check_release.py` | 0 | The checker compiled without creating a generated owned file. |
| Prohibited-token scan on the four target Lean modules | 1 (expected) | No placeholder, custom axiom, bodyless declaration, unsafe/native/oracle, or external implementation escape matched after comments were excluded. |
| `git diff --check -- Stage1_Instances/THM-M-0821 .stage1-worker-selftest.json` plus new-file hygiene checks | 0 | No whitespace, CR, NUL, or terminal-newline failure. |

The historical command
`python3 -B Stage1_Instances/THM-M-0821/check_validation.py` is not a current
release recipe. It is intentionally bound to the validation turn's base revision,
worker packet, and exact dirty-path inventory. This release checker binds that
validator and its receipt by hash and runs the narrow Lean script directly
instead of manufacturing historical state.

Retry requires dependency-legal master acceptance and truthful graph
reconciliation, the eight internal composition certificates, independently
reviewed H0/R0 evidence and `AUDIT-Z`, accepted foundation/provenance/trust
closure, and a separately provisioned hermetic and independent release run
closing every remaining gate.

Status boundary: this artifact self-tests only the negative release decision. It
supplies no accepted `M0-W`, `E0`, `E1`, `AUDIT-Z`, `THEOREM-Z`, release,
theorem completion, or master acceptance.
