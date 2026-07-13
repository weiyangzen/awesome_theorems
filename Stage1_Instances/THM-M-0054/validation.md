# Intake validation

Validation date: 2026-07-13 (Asia/Shanghai). This is a nonrelease worker check against repository
revision `c76fe0f1a7514b41f191d16840eff25e64ee9d17` and tree
`388bc991837bae9741d7e7cb88b43c216eab966a`. The automation-provided `.lake` symlink was already
untracked and was used read-only. No `lake update`, `lake build`, dependency clone/fetch, or other
`.lake` mutation was run.

## Results

| Command | Exit | Exact result or boundary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0054` | 0 | rank 1091; planned; `L0/rework_required`; no legacy slot; theorem incomplete |
| `git status --short --untracked-files=all` before editing | 0 | only the pre-existing automation-provided `Formalizations/Lean/.lake` symlink was present; it was preserved |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `c76fe0f1a7514b41f191d16840eff25e64ee9d17`; tree `388bc991837bae9741d7e7cb88b43c216eab966a` |
| `git blame -L 405,410 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error --max-time 30 'https://api.crossref.org/works/10.1007/BF01449896'` followed by a JSON field projection | 0 | Perron, *Zur Theorie der Matrices*, *Math. Ann.* 64(2), 248-263 (1907); metadata lead only |
| `curl -L --fail --silent --show-error --max-time 30 'https://link.springer.com/content/pdf/10.1007/BF01449896.pdf'` followed by byte classification | 0 | 217033-byte response began `<!DOCTYPE html>`; no source text or hash was admitted |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `cd Formalizations/Lean && lake env lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --porcelain` | 0 | empty output; pinned mathlib package remained clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0054/IntakeProbe.lean` | 0 | eight adjacent pinned declarations elaborated; complete stdout SHA-256 `ed5dadabeefa5fc6d9c575d4b6928a499e8d11b29dea235a5f6c405181c45c86`; no target or proof body |
| `rg -n -i --glob '*.lean' 'perron[- ]?frobenius\|perron.{0,40}(matrix\|spectr)\|nonnegative (square )?matrix.{0,80}(eigen\|spectr)\|spectral radius.{0,80}nonnegative' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | exactly two matches: the irreducibility file's `perron-frobenius` tag and a root-system TODO saying a fact may be proved via Perron-Frobenius; no spectral theorem declaration identified |
| prohibited-declaration scan of the owned Lean probe | 1 | expected no-match: no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` token |
| `python3 -m json.tool` on owned structured files and worker packet | 0 | valid JSON |
| `python3 -B Stage1_Instances/THM-M-0054/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, source and dependency hashes, null target, `H1/M4/R4`, exact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0054/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| `git diff --check -- Stage1_Instances/THM-M-0054 .stage1-worker-selftest.json` plus per-file no-index checks | 0 | no whitespace errors; no-index exit 1 represented only each expected new-file diff |

## Boundary

This validates only a `planned` intake dossier, scope map, source-statement crosswalk, adjacent Lean
API probe, and open downstream task DAG. The canonical human and Lean statements remain null because
the catalog does not select a source variant or conclusion bundle. The first blocked downstream
gate is `S56-M-0054-STATEMENT`. No source is accepted to `H0`; no formal artifact is accepted to
`M0`; no proof reconstruction is accepted to `R0`; and no audit or theorem completion is claimed.

The receipt timestamps delimit validation of the non-receipt inputs. Receipt serialization and
subsequent replay are necessarily later and are not represented as a release-grade signed time
attestation; the packet is explicitly mutable, provisional, and non-content-addressed.
