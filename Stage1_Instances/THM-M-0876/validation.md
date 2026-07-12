# Intake validation

Validation covers only the `planned` intake for `S56-M-0876-INTAKE`. The worker used the existing
pinned `.lake` symlink read-only. It did not run `lake update`, `lake build`, clone/fetch a
dependency, or modify the dependency cache.

Base repository revision: `02cc55f883d5b5d091ead6851bffe89199eb8391`

Base tree: `035212d041a1e61553b3d2f465964c9bbb35e47d`

Pinned Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`

Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0876` | 0 | rank 1017; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 6418,6423 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --max-time 90 -A 'Mozilla/5.0' -sS https://arxiv.org/pdf/1512.03547 -o /tmp/thm-m-0876-babai.pdf`; `file`; `wc -c`; `pdfinfo`; `sha256sum`; `pdftotext` | 0 | dated source discovery: 89-page, 843,393-byte v2 PDF, SHA-256 `b6393ff3...9c62`; abstract and page 4 results inspected; post-v2 flaw/repair and final correction history unaudited; not a replay-stable network recipe or admitted H0 bundle |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision and tree shown above |
| preliminary `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0876/IntakeProbe.lean)` | 1 | `SimpleGraph.Finite.overFinIso` was not a valid declaration name; the unsupported check was removed without substituting a target statement |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0876/IntakeProbe.lean)` | 0 | seven adjacent graph-isomorphism/language/reduction APIs elaborated; complete stdout SHA-256 `f312f54d...acf8` |
| bounded exact-topic search over pinned mathlib and repo-local Lean | 1 (expected no match) | no graph-isomorphism complexity/quasipolynomial/P/NP declaration under the recorded patterns; this is not a complete anchor audit or external absence claim |
| `python3 -m json.tool` on all structured artifacts and the worker packet | 0 | all JSON artifacts are valid after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0876-pycache python3 -m py_compile Stage1_Instances/THM-M-0876/check_intake.py` | 0 | scoped validator compiles without generated files under the owned path |
| preliminary `python3 Stage1_Instances/THM-M-0876/check_intake.py --worker-packet .stage1-worker-selftest.json` | 1 | checker detected Markdown trailing spaces in `validation.md`; the spaces were removed, its provisional hash was refreshed, and all checks were rerun |
| `python3 Stage1_Instances/THM-M-0876/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, planned H5/M4/R4 boundary, hashes, null target, artifact inventory, packet, and six open tasks agree |
| `python3 Stage1_Instances/THM-M-0876/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited-construct scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; each no-index exit 1 is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0876 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; no-index checks cover untracked files |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0876-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Source/proposition selection and independent
review, canonical Lean elaboration and statement mutations, complete formal anchor audit,
obligation registry, typed graphs, proof, composition, trust closure, hermetic replay,
deterministic release bundle, and independent verification remain open. These failures prevent
statement, branch-proof, audit-completion, and theorem-completion claims, but do not invalidate the
planned intake.
