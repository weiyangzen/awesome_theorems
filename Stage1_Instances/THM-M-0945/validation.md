# Intake validation

Base revision: `a3b18eec39bf04be025b1641cae02f4d44fdf11a`; base tree:
`fdfff18dea4c6798c5b322b6088dfe556109c134`.

This validation covers target membership, the planned dossier and six-task open DAG, repository and
primary-source boundaries, exact owned-file invariants, and a narrow pinned Lean substrate probe.
Because the source-to-Lean conventions have not been independently approved, no canonical target,
expression hash, statement mutation, checked transport, or proof is claimed. The automation-
provided canonical `.lake` symlink and pinned artifacts were used read-only; no dependency update,
build, clone, fetch, or `.lake` mutation was performed. The pre-existing untracked symlink makes
this nonrelease worker evidence.

The Green-Tao primary-source observations were dated discovery inputs, not replay-stable validation
recipes. The Annals-hosted 67-page, 488,947-byte PDF had SHA-256 `967dd6f5...e52c89`; its Theorem
1.1 on printed page 482 and nondegenerate `r != 0` boundary on page 524 were inspected. Crossref
metadata had SHA-256 `bb8ee3a0...4e69d2`, and the arXiv `math/0404188v6` metadata response had
SHA-256 `adb22946...f7ee0`. No remote file was added to the repository or credited as H0 evidence.

## Commands and results

All repository commands ran from the worker clone root on 2026-07-13 (Asia/Shanghai), except where
a `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0945` | 0 | rank 1484; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; preserved read-only |
| `git rev-parse HEAD` and `git rev-parse 'HEAD^{tree}'` | 0 each | base revision and tree recorded above |
| `git blame -L 6903,6908 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error --max-time 30 -o /tmp/green-tao.pdf https://annals.math.princeton.edu/wp-content/uploads/annals-v167-n2-p03.pdf` | 0 | 488,947-byte, 67-page publisher PDF; SHA-256 `967dd6f5bb53d70abdbb07be0afe59e60b2a232e2c3387966013a09960e52c89`; dated mutable discovery only |
| `pdftotext -layout /tmp/green-tao.pdf /tmp/green-tao.txt && sed -n '1,180p' /tmp/green-tao.txt && rg -n 'Theorem 1\.|Theorem 1\.[0-9]\|arbitrarily long\|arithmetic progression' /tmp/green-tao.txt \| head -80` | 0 | pinpoint Theorem 1.1 on page 482 and the nondegenerate proof boundary on page 524 inspected; not H0 evidence |
| `curl -L --fail --silent --show-error --max-time 30 https://api.crossref.org/works/10.4007/annals.2008.167.481 -o /tmp/green-tao-crossref.json` | 0 | 1,702-byte Crossref response; SHA-256 `bb8ee3a0f97671d134cb51e22160bb58cc2b427e47390dbaeb88bdf75d4e69d2`; publication metadata only |
| `curl -L --fail --silent --show-error --max-time 30 'https://export.arxiv.org/api/query?id_list=math/0404188' -o /tmp/green-tao-arxiv.xml` | 0 | 2,236-byte arXiv response; SHA-256 `adb2294676bc800d07a8df69b0fe8a9200b7eb66d35553b7d86d14f7ce9f7ee0`; v6 correction lead only |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake 5.0.0-src+98dc76e; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | no output; pinned dependency worktree remained clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0945/IntakeProbe.lean)` | 0 | eight adjacent pinned prime, length-three progression, Roth, and finite-color APIs elaborated; output SHA-256 `648f295c...c961a7`; no target theorem was stated |
| `rg -n -i 'green.?tao\|arbitrarily long arithmetic progressions\|prime numbers contain infinitely many arithmetic progressions' Formalizations/Lean/AwesomeTheorems --glob '*.lean'` | 1 (expected no match) | no exact repo-local declaration found |
| `rg -n -i 'green.?tao\|arbitrarily long arithmetic progressions\|prime numbers contain infinitely many arithmetic progressions' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 (expected no match) | no exact pinned-mathlib declaration found; not a global absence claim |
| `python3 -m json.tool Stage1_Instances/THM-M-0945/instance.json` | 0 | instance JSON is valid |
| `python3 -m json.tool Stage1_Instances/THM-M-0945/task-dag.json` | 0 | task-DAG JSON is valid |
| `python3 -m json.tool Stage1_Instances/THM-M-0945/intake-receipt.json` | 0 | receipt JSON is valid |
| `python3 -m json.tool .stage1-worker-selftest.json` | 0 | worker packet JSON is valid |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0945-pycache python3 -m py_compile Stage1_Instances/THM-M-0945/check_intake.py` | 0 | scoped validator compiles without writing generated files into the owned path |
| `python3 -B Stage1_Instances/THM-M-0945/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, H1/M4/R4 planned boundary, null target, source hashes, artifact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0945/check_intake.py` | 0 | public replay mode passes without requiring the scheduler-only root packet |
| `rg -n '\\b(sorry\|admit\|sorryAx)\\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0945 --glob '*.lean'` | 1 (expected no match) | no prohibited Lean declaration |
| `for f in Stage1_Instances/THM-M-0945/* .stage1-worker-selftest.json; do rc=0; out=$(git diff --no-index --check /dev/null "$f" 2>&1) \|\| rc=$?; test "$rc" -le 1; test -z "$out"; done` | 0 aggregate | every internal no-index exit 1 was the expected new-file difference with empty diagnostic output |
| `git diff --check -- Stage1_Instances/THM-M-0945 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0945-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Immutable source admission, convention mapping and
independent review, canonical Lean elaboration and mutations, complete anchor audit and discovery
freeze, obligation registry, typed graphs, proof, composition, trust closure, readable
reconstruction, hermetic replay, deterministic release bundle, and independent verification remain
open. They prevent statement, audit-completion, and theorem-completion claims, but do not invalidate
the planned intake.
