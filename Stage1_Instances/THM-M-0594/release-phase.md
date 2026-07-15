# THM-M-0594 release reconciliation

Item: `S56-M-0594-RELEASE`. Base revision:
`f976b9b21418bfda4bc815ba2a7238e932666231` (tree
`6fbe6e3a73d5005115818a8f902da2b70f4aab24`).

## Exact verdict

`blocked`. The lifecycle remains `planned`, the accepted root vector remains
`[H1, M3, R3]`, and both `AUDIT-Z` and `THEOREM-Z` are blocked. Therefore
`audit_complete=false`, `theorem_complete=false`, and accepted receipt and
obligation lists remain empty. This worker proposes only `[_]` for the
self-tested negative reconciliation; it accepts no theorem or release state.

The first failed gate is
`dependency.S56-M-0594-VALIDATION.master_acceptance`. The prerequisite
validation receipt is provisional worker evidence with `accepted=false`,
`release_grade=false`, and `verdict=blocked`. Release is not dependency-legal.
The validation receipt in turn records the proof dependency as unaccepted.

## Evidence reconciliation

The current-base narrow replay is useful but not root closure. The exact
unrestricted `WhitneyEmbeddingTarget` elaborates at trust zero. The local
proper-injective-to-`IsEmbedding` bridge and its conditional exact-target
composer are sorry-free and report only `propext`, `Classical.choice`, and
`Quot.sound`. The composer explicitly consumes a finite-dimensional smooth,
proper, injective immersion; it does not construct one. `M0594-C-GLOBAL`
therefore has no premise-free body and the exact root remains open.

Pinned mathlib supplies only `exists_embedding_euclidean_of_compact`, whose
type adds `CompactSpace M`. Its own Whitney module marks the unrestricted weak
theorem as a TODO. The compact wrapper is a strict specialization and cannot
replace the canonical target.

The authoritative graph remains the pre-acceptance snapshot. It records the
cut `M0594-C-GLOBAL, M0594-L-TOPOLOGICAL`, `root_closed=false`, and
`H1/M3/R3`. The unaccepted proof receipt provisionally closes only the
topological bridge, reducing the provisional cut to `M0594-C-GLOBAL`; a worker
cannot reconcile that proposal into accepted graph state.

`AUDIT-Z` also fails independently. `intake.json` still records a null formal
target and an open statement gate, `README.md` remains an intake-era
projection, and the graph has not reconciled the provisional bridge evidence.
The source crosswalk is H1 rather than an independently reviewed pinpoint H0
record, and no independently accepted R0 reconstruction exists.

The historical validation recipe is content-bound but not fresh at this release
base. Running its checker exits at the deliberate base-revision assertion
(`b366bdd9...` versus current `f976b9b...`). The release checker records that
failure and runs its own current-base narrow replay; it does not relabel the
old receipt as current or accepted.

Release assurance is absent for an accepted foundation and complete transitive
TCB/provenance closure, immutable clean input, empty-cache cold build, offline
archive restoration, SBOM/licenses, deterministic build-twice bundle,
protected adversarial CI, two qualifying signed independent runners, and an
independently implemented minimal verifier. The automation-provided untracked
`.lake` symlink was reused read-only and is warm nonrelease evidence.

## Commands and results

Commands ran from the worker clone on 2026-07-15 (`Asia/Shanghai`). No `lake
update`, `lake build`, dependency clone/fetch/checkout, or `.lake` mutation was
performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0594` | 0 | Rank 255 remains planned, rework-required, and theorem-incomplete. |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 timeout --foreground 300 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0594/Statement.lean` | 0 | The exact unrestricted target elaborated. |
| Same direct Lean command for `ProofSupport.lean` | 0 | Three support bodies used only the expected axioms; the finite-index immersion endpoint and compactness-only `Fintype` bridge were exposed. |
| Same direct Lean command for `AnchorAudit.lean` | 0 | The compact-only endpoint and local strict-specialization wrapper elaborated with the expected axioms. |
| `python3 Stage1_Instances/THM-M-0594/check_obligation_tree.py` | 0 | 16 obligations and 46 typed edges passed; root remained open at M3. |
| `bash Stage1_Instances/THM-M-0594/check_proof.sh` | 0 | The topological bridge and conditional composer were sorry-free; output explicitly retained `M0594-C-GLOBAL`. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0594/check_validation.py --probe` | 1 (expected fail-closed) | The predecessor checker rejected current HEAD at its base-revision freshness assertion and was not cited as a fresh replay. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0594/check_release.py --worker-packet .stage1-worker-selftest.json` | 0 | Current-base network-isolated narrow replay and release reconciliation derived the blocked verdict, unchanged vector, and both terminal decisions false. |
| `python3 -m json.tool` over the release spec, decision, receipt, and worker packet | 0 | All structured release artifacts parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0594-release-pycache python3 -m py_compile Stage1_Instances/THM-M-0594/check_release.py` | 0 | Checker syntax compiled outside the repository. |
| `git diff --check -- Stage1_Instances/THM-M-0594 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

## Retry boundary

First supply and validate a premise-free exact body for `M0594-C-GLOBAL` and
the unchanged unrestricted root, then reconcile and master-accept the complete
dependency chain. Release additionally requires accepted H0/R0 and complete
foundation/provenance/TCB/SBOM review, immutable cold offline reproduction, two
qualifying independent attestations, an independent minimal verifier,
protected CI, deterministic bundling, and separate master `AUDIT-Z` and
`THEOREM-Z` decisions.

This packet grants no accepted `M0`, `E0/E1`, `H0`, `R0`, audit completion,
theorem completion, release, independent-verification, or master-acceptance
credit.
