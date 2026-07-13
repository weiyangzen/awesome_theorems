# Intake validation

Base revision: `a3b18eec39bf04be025b1641cae02f4d44fdf11a`; base tree:
`fdfff18dea4c6798c5b322b6088dfe556109c134`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, bibliographic source discrimination, JSON and scoped invariants, a narrow pinned Lean
Roth-family API and axiom probe, bounded repository/mathlib search, prohibited-construct hygiene,
and whitespace. It does not validate a canonical theorem statement, source-fidelity result, proof,
or terminal status.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

Crossref and Semantic Scholar bibliographic records for K. F. Roth's "On Certain Sets of Integers,"
*Journal of the London Mathematical Society* s1-28(1) (1953), 104-109, DOI
`10.1112/jlms/s1-28.1.104`, were inspected as dated mutable discovery inputs. Their observed SHA-256
digests were `ac676873...65a8` and `1098c6ec...aa87`. The latter reports the paper closed with no
open-access PDF, and the DOI publisher endpoint returned an access challenge. No source file was
added. The paper body, exact statement, definitions, premises, proof, corrections, and errata were
not inspected or independently reviewed, so no H0 claim is made.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a different
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0947` | 0 | rank 1486; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 6917,6922 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref metadata fetch for DOI `10.1112/jlms/s1-28.1.104`; `jq`; `wc -c`; `sha256sum` | 0 | matching author, title, journal, January 1953, volume/issue and pages; 2,404-byte transient JSON, SHA-256 `ac676873...65a8`; discovery only |
| Semantic Scholar metadata fetch for the same DOI; `jq`; `wc -c`; `sha256sum` | 0 | matching author/title/year/DOI and closed/no-open-PDF status; 423-byte transient JSON, SHA-256 `1098c6ec...aa87`; discovery only |
| DOI/publisher article access | 0 at `curl` transport, HTTP 403 downstream | publisher body blocked by an access challenge; no source theorem inspection claimed |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision `8a178386...a95`, tree `bdc39a31...e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty; pinned package worktree remained clean |
| `sha256sum` on toolchain, lock, and the two pinned Roth source modules | 0 | hashes recorded in `instance.json` and `intake-receipt.json` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0947/IntakeProbe.lean)` | 0 | six exact-family interfaces elaborated; three candidate axiom reports were `[propext, Classical.choice, Quot.sound]`; complete output SHA-256 `0d20ca0e...fb2b8` |
| bounded case-insensitive Roth/three-AP search over pinned mathlib and repo-local Lean | 0 | located the direct pinned Roth declarations, adjacent Ruzsa-Szemeredi/Behrend work, and unrelated Thue-Siegel-Roth legacy material; discovery only, not a complete anchor audit |
| `python3 -m json.tool` on owned JSON and the root worker packet | 0 | all finalized structured artifacts parse as JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0947-pycache python3 -m py_compile Stage1_Instances/THM-M-0947/check_intake.py` | 0 | scoped validator compiles without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0947/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H1/M3/R4 boundary, source hashes, null target, artifact inventory, worker packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0947/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited-construct scan over the owned Lean probe | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 per new file is only the expected content difference |
| `git diff --check -- Stage1_Instances/THM-M-0947 .stage1-worker-selftest.json` | 0 | no tracked-diff whitespace diagnostics |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0947-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Exact primary-source admission and review,
canonical formulation selection and Lean elaboration, statement mutations, complete anchor and
terminal-body provenance audit, obligation registry, typed graphs, proof composition, readable
reconstruction, hermetic replay, deterministic release bundle, and independent verification remain
open. These failures prevent statement, audit-completion, and theorem-completion claims, but they do
not invalidate the planned intake.
