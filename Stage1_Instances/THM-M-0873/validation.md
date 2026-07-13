# Intake validation

Validation covers only the `planned` intake for `S56-M-0873-INTAKE`. The worker used the existing
pinned `.lake` symlink read-only. It did not run `lake update`, `lake build`, clone/fetch a
dependency, or modify the dependency cache.

Base repository revision: `748243faadc15828fb087059337fd05b7be9fdeb`

Base tree: `e46d642646f80980838b6f016f5d69b817bd464d`

Pinned Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`

Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0873` | 0 | rank 1427; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 6397,6402 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| source and duplicate crosswalk over catalog/Stage0 | 0 | target record, algorithm/P-NP/WL neighbors, and duplicate `THM-M-1567` confirmed; no evidence transferred |
| `curl -L --fail --max-time 90 -A Mozilla/5.0 -sS https://arxiv.org/pdf/1512.03547v2 -o /tmp/thm-m-0873-babai-v2.pdf`; `file`; `wc -c`; `pdfinfo`; `sha256sum`; `pdftotext -layout` | 0 | Babai v2: 89 pages, 843,393 bytes, SHA-256 `b6393ff3...9c62`; page 4 definition, Theorem 1.1.1, Corollary 1.1.2 inspected; pre-fix discovery input only; acquisition log SHA-256 `34f98fc3...2c2a` |
| `curl -L --fail --max-time 90 -A Mozilla/5.0 -sS https://arxiv.org/pdf/1710.04574v1 -o /tmp/thm-m-0873-helfgott.pdf`; `file`; `wc -c`; `pdfinfo`; `sha256sum`; `pdftotext -layout` | 0 | Helfgott post-fix exposition: 67 pages, 659,668 bytes, SHA-256 `f16a953a...f2d2`; graph reduction, Theorem 1.1, correction account, and Corollary 1.2 inspected; acquisition log SHA-256 `e31bc08a...cdab` |
| `curl -L --fail --max-time 90 -sS http://people.cs.uchicago.edu/~laci/update.html -o /tmp/thm-m-0873-update.html`; `curl -L --fail --max-time 90 -sS http://people.cs.uchicago.edu/~laci/upcc-fix.pdf -o /tmp/thm-m-0873-upcc-fix.pdf`; inspect/hash | 0 | update HTML SHA-256 `d96a4083...42ca`; four-page fix SHA-256 `e4438bf1...5653`; withdrawal/restoration and repaired recursive call crosswalked; author host required HTTP because HTTPS certificate verification failed |
| `curl -L --fail --max-time 180 -sS http://people.cs.uchicago.edu/~laci/quasi25.pdf -o /tmp/quasi25.pdf`; inspect/hash | 0 | 109 pages, 873,346 bytes, SHA-256 `3b80cf8a...a9c`; result and correction notes inspected; document's incomplete-revision warning retained; combined author-host acquisition log SHA-256 `84e8c954...eac7` |
| `curl -L --fail --max-time 60 -sS https://api.crossref.org/works/10.1145/2897518.2897542` | 0 | 2016 STOC extended-abstract metadata, pages 684-697; filtered metadata SHA-256 `67e1d498...f4cb`; publisher text was not obtained or credited |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision and tree shown above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | no output; dependency remained clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0873/IntakeProbe.lean)` | 0 | seven adjacent graph-isomorphism/language/reduction APIs elaborated; complete stdout SHA-256 `f312f54d...acf8`; no target or proof credit |
| bounded exact-topic `rg` over pinned mathlib and repo-local Lean | 1 (expected no match) | no exact graph-isomorphism quasipolynomial declaration under the recorded patterns; not a complete anchor audit or global absence claim |
| `python3 -m json.tool` on owned structured artifacts and worker packet | 0 | all JSON parses after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0873-pycache python3 -m py_compile Stage1_Instances/THM-M-0873/check_intake.py` | 0 | scoped validator compiles without generated files under the owned path |
| `python3 -B Stage1_Instances/THM-M-0873/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | identity, current authority hashes, planned H1/M4/R4 boundary, null target, artifact inventory, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0873/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited-construct scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` for every owned file and worker packet | 0 aggregate | no whitespace diagnostics; each no-index exit 1 is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0873 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; scoped validator covers untracked files |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0873-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Exact source admission and independent review,
canonical Lean elaboration and statement mutations, complete formal anchor audit, obligation
registry, typed graphs, proof, composition, trust closure, hermetic replay, deterministic release
bundle, and independent verification remain open. These boundaries prevent statement, proof,
audit-completion, and theorem-completion claims but do not invalidate the planned intake.
