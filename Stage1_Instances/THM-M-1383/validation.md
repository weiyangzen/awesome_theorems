# Intake validation

Base revision: `300a2745fe5f7351353cca57a5fdb8ad2325458c` (tree
`f28a7c551a8f3600b3a402791362affb691ab478`). Validation ran on 2026-07-13 in this isolated worker
clone. Existing pinned `.lake` artifacts were used read-only; no update, build, clone, fetch, or
dependency mutation was run.

## Validation boundary

Validation covers target membership, the planned dossier, scope and source crosswalk, exact open
task topology, pinned adjacent Lean APIs, prohibited constructs, and file hygiene. The inspected
textbook and official errata discriminate among source families; the catalog does not cite or
select them. Because the catalog determines no proposition, there is no canonical Lean expression,
target-expression fingerprint, proof body, axiom report, or theorem-completion result. The probe
authenticates interfaces only.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1383` | 0 | Rank 993, planned, no accepted legacy artifacts, theorem incomplete |
| `git status --short --untracked-files=all` before editing | 0 | Only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | Base revision and tree recorded above |
| `git blame -L 10076,10081 -- Docs/researches/math_theorems.md` | 0 | All six uncited catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sha256sum /tmp/teschl-ode.pdf /tmp/thm-m-1383-teschl-extract.txt /tmp/teschl-errata.pdf && wc -c /tmp/thm-m-1383-teschl-extract.txt` | 0 | Author-hosted Teschl Chapter 5 source, four-page extract, and official errata matched the three recorded hashes; extract length was 14,252 bytes |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree} && git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | Revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`, clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1383/IntakeProbe.lean` | 0 | Six adjacent APIs elaborated; output SHA-256 `0016ea42d29bd81f5f8355ac238bcdd0e5426ee3cd4d424907c6308d7da03f5e` |
| `rg -n -i --glob '*.lean' 'two[ _-]?point[ _-]?boundary\|two[ _-]?point.*boundary[ _-]?value\|boundary[ _-]?value.*two[ _-]?point' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 1 expected | No exact-topic occurrence; intake discovery only, not an exhaustive anchor audit |
| `rg -n -i --glob '*.lean' 'boundary[ _-]?value\|boundaryValue' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 expected | No occurrence under the recorded terms; no global absence claim |
| `rg -n -i --glob '*.lean' 'boundary[ _-]?value\|boundaryValue' Formalizations/Lean/AwesomeTheorems` | 0 | Unrelated topology, PDE, conformal, obstacle, and complex-analysis hits only; no target candidate |
| `python3 -m json.tool` on all structured owned files and the worker packet | 0 | Valid JSON after finalization |
| parse `check_intake.py` with Python `ast` | 0 | Validator syntax accepted without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-1383/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | Manifest/DAG identity, source hashes, pins, null target, H5/M4/R4 boundary, exact inventory, packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-1383/check_intake.py` | 0 | Public replay mode passed in the unchanged worker base |
| `rg -n --glob '*.lean' '\b(sorry\|admit)\b\|\bsorryAx\b\|^[[:space:]]*(axiom\|constant\|opaque)\b\|^[[:space:]]*unsafe\b' Stage1_Instances/THM-M-1383` | 1 expected | No prohibited declaration |
| `for f in .stage1-worker-selftest.json Stage1_Instances/THM-M-1383/*; do out=$(git diff --no-index --check -- /dev/null "$f" 2>&1) || rc=$?; test ${rc:-0} -le 1; test -z "$out"; unset rc; done` | 0 | Every added file had no whitespace diagnostics; per-file diff status 1 was accepted only as the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-1383 .stage1-worker-selftest.json` | 0 | No tracked whitespace diagnostics |

## Result and boundary

The assigned intake is self-tested as a provisional `[_]` worker proposal. Its receipt is unsigned,
mutable, non-content-addressed, and not accepted. The authoritative checklist remains unchanged.
Ordinary theorem-proof execution is blocked by `H5` until an accountable correction or source
selection yields one stable proposition. Exact statement elaboration, source `H0`, formal anchor
audit, obligation registry, proof, composition, trust closure, readable reconstruction, hermetic
replay, and independent release gates remain open. Audit completion and theorem completion are
both false.
