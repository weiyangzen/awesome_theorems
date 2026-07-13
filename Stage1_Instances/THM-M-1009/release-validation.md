# THM-M-1009 release reconciliation

Item: `S56-M-1009-RELEASE`

Base revision: `a7c34044268bf5745e40c011134b447dd1e7cd0f`

## Exact verdict

`blocked`. The lifecycle remains `planned`, the accepted root vector remains
`[H1, M3, R3]`, and both `audit_complete` and `theorem_complete` remain false. This worker accepts no receipt and makes no `E0`, accepted `M0-L`, `AUDIT-Z`, `THEOREM-Z`, release, theorem-completion, or master-acceptance claim.

The structured worker recipe is `release-spec.json`; its provisional node receipt is
`release-receipt.json`. The receipt is explicitly `release_grade=false`, records a nonrelease
warm-cache worker check, and remains subject to integration-lane acceptance.

The first failed node gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`:
`S56-M-1009-VALIDATION` is only provisional `[_]`, explicitly nonrelease, and not master-accepted.
The first intrinsic release-assurance failure is
`S56-7.3-7.4-TRANSITIVE-PROVENANCE-TCB-CLOSURE`; the first reproduction failure is
`S56-10.6-HERMETIC-COLD-BUILD`.

## Evidence reconciliation

The exact frozen generalized Borel-Cantelli lower-bound target, the repo-local proof body, and the
frozen composition path replay from temporary source copies against the pinned mathlib revision.
The checked proof roots report only `propext`, `Classical.choice`, and `Quot.sound`. A separately
written validation module checks the final tail-limit composition and exact target type without
importing `Proof.lean` or `ObligationTree.lean`. That is useful provisional differential evidence,
not a second mathematical proof or independent release verifier.

Structured authority remains fail-closed. `typed-graphs.json` predates the proof and records all 15
nodes at `H1/M3/R3`, no accepted evidence IDs, `root_closed=false`, and the four-node machine cut
`M1009-L-SECOND-MOMENT`, `M1009-L-TAIL`, `M1009-L-RATIO`, and
`M1009-L-CONTINUITY`. The proof and validation receipts are provisional and unaccepted. The intake
record also still names the legacy candidate with a null expression/environment while the later
statement record freezes the exact new declaration. The weaker accepted state therefore controls.

`AUDIT-Z` is false because the primary-source crosswalk lacks a stable source hash, exact
theorem/page/formula and assumptions, errata analysis, node mapping, and independent review; no
independently reviewed R0 reconstruction exists. `THEOREM-Z` additionally lacks accepted proof and
graph reconciliation, complete transitive provenance/foundation/TCB closure, immutable clean input,
empty-cache network-denied offline reproduction, complete SBOM/licenses, two signed independent
runner attestations, an independently implemented minimal verifier, protected CI evidence, and a
deterministic content-addressed release bundle.

## Commands and results

Commands ran from the isolated worker clone on 2026-07-14 (`Asia/Shanghai`). The pre-existing
canonical `.lake` symlink was reused without mutation. No `lake update`, `lake build`, dependency
clone/fetch, or network operation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and exactly 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-1009` | 0 | Rank 289 remains planned, L0/rework-required, and theorem-incomplete. |
| `python3 -B Stage1_Instances/THM-M-1009/check_release.py` | 0 | Content-bound authority and predecessor evidence agreed; narrow Lean replay passed and exact blocked terminal decisions held. |
| `python3 -m json.tool` on the three release JSON artifacts and `.stage1-worker-selftest.json` | 0 | Every structured release artifact parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1009-release-pycache python3 -m py_compile Stage1_Instances/THM-M-1009/check_release.py` | 0 | The checker compiled without writing generated files into the owned path. |
| `git diff --check -- Stage1_Instances/THM-M-1009 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

Retry requires dependency-legal master acceptance, reconciliation of proof and validation evidence
into current structured authority, accepted H0/R0 and AUDIT-Z evidence, complete provenance and TCB
closure, and a separately provisioned hermetic and independent release run producing the complete
deterministic evidence bundle.

Status boundary: this packet self-tests only the truthful negative release decision. It supplies no
accepted receipt, `E0`, accepted `M0-L`, `AUDIT-Z`, `THEOREM-Z`, release, theorem completion, or
master acceptance.
