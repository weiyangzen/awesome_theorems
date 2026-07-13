# THM-M-1143 validation-phase result

Item `S56-M-1143-VALIDATION` was checked against base revision
`53dced5833f17a55f667239e756fc93c99810c44` (tree
`f0c4bdb31a84f0b4221b8392c9c95be1441914dc`). The phase verdict is `blocked`.
The `[_]` worker state records only a self-tested negative validation packet; it does not mean that
any failed gate, the theorem, or the audit was accepted.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Packet and frozen-input integrity | pass | The checker binds the canonical expression, registry denominator, proof receipt/blocker, source records, manifests, and phase outputs to exact hashes. |
| Source hygiene | pass for four inspected modules | Comment-aware scans found no `sorry`, `admit`, `sorryAx`, bodyless local axiom/constant, `opaque`, `unsafe`, external implementation, or native oracle. |
| Current narrow kernel replay | pass, nonrelease | The four modules elaborated at trust zero in a fresh temporary directory under bubblewrap with networking unshared, fixed locale/timezone, and only that directory writable. |
| Historical conditional proof evidence | partial only | The predecessor receipt records a trust-zero isolated replay of seven local/conditional declarations with only `propext`, `Classical.choice`, and `Quot.sound`. It does not inhabit the gradient package or root. |
| Exact source-statement identity | fail closed | The existing crosswalk has no primary edition, theorem/page, assumptions, proof, or errata evidence for the worker-selected all-positive-dimensions Euclidean statement. |
| Exact root kernel closure | fail | `InteriorGradientEstimatePackage`, corresponding to `M1143-L-GRADIENT`, is uninhabited. The exact root remains `M3`. |
| Complete trust and provenance | fail closed | There is no accepted transitive terminal-body, foundation, TCB, computation, or source-boundary packet for the exact root. |
| Hermetic release replay | fail closed | The `.lake` path is a shared warm mutable symlink and is incomplete. No clean empty-cache cold build, offline restoration, SBOM/license archive, or deterministic bundle exists. |
| Independent verification | fail closed | `Validation.lean` imports `Proof` and contains same-workspace probes. There is no distinct signed clean runner/cache or independently implemented minimal release verifier. |

The first substantive failure is `S56-M1143-X-SOURCE-IDENTITY`. The exact-root, complete
trust/provenance, hermetic release, and independent-verification gates also fail independently.
During an earlier retry, the shared canonical `.lake` was concurrently being materialized and Lake
tool discovery failed/timed out. That incident is retained below, but a later retry succeeded without
building or fetching dependencies. This packet does not attribute shared cache changes to one process.

## Commands and results

No command intentionally ran `lake update`, `lake build`, dependency `git clone`/`git fetch`, or a
manifest mutation.

```text
$ python3 Docs/tools/check_stage1_standard.py
exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

$ python3 scripts/stage1_target.py check
exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required

$ python3 scripts/stage1_target.py show THM-M-1143
exit 0; rank 348, planned lifecycle, theorem_complete=false

$ python3 -B Stage1_Instances/THM-M-1143/check_obligation_tree.py
exit 0; 12 obligations and 24 typed edges passed; root remains open M3

$ bash Stage1_Instances/THM-M-1143/check_proof.sh
exit 1; Lake tool discovery emitted "external command 'git' exited with code 128" before Lean ran

$ timeout 20 lake env which lean
exit 124; timed out while the shared dependency closure was being materialized

$ timeout 20 lake env printenv LEAN_PATH
exit 124; timed out while the shared dependency closure was being materialized

$ bash Stage1_Instances/THM-M-1143/check_proof.sh
exit 0 on retry; seven local/conditional declarations elaborated at trust zero and reported only
propext, Classical.choice, and Quot.sound

$ python3 -B Stage1_Instances/THM-M-1143/check_validation.py
exit 0; network-isolated trust-zero replay, packet integrity, exact axiom checks, source hygiene,
pins, and all negative gate decisions passed. Output SHA-256 values were
Statement `e05a7b...01610`, ObligationTree `20d57a...19d44`, Proof
`2de4c5...c90cb`, and Validation `1fc428...0ce2`

$ git diff --check -- Stage1_Instances/THM-M-1143 .stage1-worker-selftest.json
exit 0; no whitespace errors
```

## Retry condition

Independently supply a placeholder-free proof or pinned exact integration for
`M1143-L-GRADIENT`, establish primary-source identity, and complete the trust, provenance,
cold/offline, deterministic-bundle, and distinct-runner gates.

`audit_complete=false` and `theorem_complete=false`.
