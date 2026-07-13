# THM-M-0914 release reconciliation

Item: `S56-M-0914-RELEASE`

Base revision: `c8b8f4f857647bcc095dc48e8c30390991351ab3`

## Exact verdict

`blocked`. The lifecycle remains `planned`, the accepted root vector remains
`[H1, M3, R4]`, and both `audit_complete` and `theorem_complete` remain false. This worker accepts no
receipt and makes no `AUDIT-Z`, `THEOREM-Z`, release, or theorem-completion claim.

The structured worker recipe is `release-spec.json`; its provisional node receipt is
`release-receipt.json`. The receipt is explicitly `release_grade=false` and records a dirty
warm-cache worker run. Only the integration lane can accept it.

The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`. The generated execution DAG projects
`S56-M-0914-VALIDATION` as provisional `[_]`, while the target-local task DAG still records it as
`open` with no evidence IDs or accepted states. Its receipt is `accepted=false`, non-release-grade,
and itself reports the proof prerequisite as unaccepted. The first additional release-assurance
failure is `S56-10.6-HERMETIC-COLD-BUILD`.

## Evidence reconciliation

The narrow replay elaborates the exact `Fin (n + 1) -> Fin n` collision target through pinned
mathlib and every frozen proof child. A separately written `Validation.lean` route imports neither
`Proof` nor `ObligationTree` and reconstructs the same root through noninjectivity. Bubblewrap denied
network access, Lean ran with `--trust=0`, all 15 covered declarations were sorry-free, the observed
axioms stayed within `propext`, `Classical.choice`, and `Quot.sound`, and the inspected closure had no
unsafe or unexpected bodyless declarations.

This remains provisional evidence. Both routes ran in this worker against the same shared warm
`.lake` cache. Structured authority remains `planned` and `[H1, M3, R4]`, with `root_closed=false`,
zero accepted closed obligations, and no accepted receipts. A successful wrapper replay cannot turn
that state into accepted `M0-W` or `E1`.

`AUDIT-Z` is open because the inventory is neither accepted nor fully reconciled: discovery was
explicitly bounded, inspected external archives were not retained for independent replay, source
and historical boundaries remain open, and transitive provenance/trust classification is
incomplete. `THEOREM-Z` additionally lacks independently reviewed H0 source fidelity and R0
reconstruction, accepted foundation and TCB closure, immutable clean input, an empty-cache offline
build, complete SBOM/licenses, two qualifying signed runner attestations, an independently
implemented minimal verifier, protected release CI, and a deterministic content-addressed bundle.

## Commands and results

Commands ran from this isolated worker root on 2026-07-14 (`Asia/Shanghai`). No `lake update`,
`lake build`, dependency clone/fetch, source edit outside this target, or `.lake` mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and exactly 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required. |
| `python3 scripts/stage1_target.py show THM-M-0914` | 0 | Rank 1456 remains planned and theorem-incomplete. |
| `bash Stage1_Instances/THM-M-0914/check_validation.sh` | 0 | Exact proof and differential roots replayed with network denied and `--trust=0`; 15 declarations were sorry-free, with allowed axioms and no unsafe or unexpected bodyless declarations. |
| `python3 -B Stage1_Instances/THM-M-0914/check_release.py` | 0 | Bound current evidence and authority, performed a fresh narrow Lean replay, and derived the blocked terminal decisions. |
| `python3 -B Stage1_Instances/THM-M-0914/check_validation.py` | 1 | Historical phase validator requires its old base revision and now-absent root worker packet; the mismatch is recorded rather than hidden. |
| `python3 -m json.tool` on `release-spec.json`, `release-decision.json`, `release-receipt.json`, and `.stage1-worker-selftest.json` | 0 | Every structured release artifact parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0914-release-pycache python3 -m py_compile Stage1_Instances/THM-M-0914/check_release.py` | 0 | Checker bytecode was written outside the repository. |
| `git diff --check -- Stage1_Instances/THM-M-0914 .stage1-worker-selftest.json` | 0 | No whitespace errors; the checker also inspected every untracked handoff file. |

The historical validation checker hard-codes its phase base `c45f3c7...` and the validation worker
packet. Its immutable receipt is hash-bound provisional evidence, not a current release recipe. The
release checker therefore performs a fresh scoped Lean replay instead of manufacturing old state.

Retry requires dependency-legal master acceptance, reconciliation of both structured state views
and the exact-root graph, a complete accepted audit inventory, independently reviewed H0/R0,
complete accepted trust and supply-chain closure, and separately provisioned hermetic and
independent release runs that close every remaining gate.

Status boundary: this artifact self-tests only the negative release decision. It supplies no
accepted `M0-W`, `E1`, `AUDIT-Z`, `THEOREM-Z`, release, theorem completion, or master acceptance.
