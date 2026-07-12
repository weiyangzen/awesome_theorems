# Intake validation

Base revision: `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`; base tree:
`829a47c47ae831cada4f8acc6c2c00ba5883215e`.

This validation covers target membership, the planned dossier and open task DAG, source and
duplicate boundaries, JSON/scoped invariants, and a narrow pinned Lean API probe. Because the
catalogue does not select one proposition, no canonical target, expression hash, mutation result,
source acceptance, transport, or proof is claimed. The automation-provided canonical `.lake`
symlink and artifacts were used read-only; no dependency update, build, clone, fetch, or `.lake`
mutation was performed. The symlink is a pre-existing out-of-scope untracked automation input, so
this is nonrelease worker evidence.

## Commands and results

All commands ran from the worker clone root on 2026-07-13 (Asia/Shanghai), except where a `cwd` is
shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0305` | 0 | rank 1013; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; preserved read-only |
| `git rev-parse HEAD` and `git rev-parse 'HEAD^{tree}'` | 0 each | base revision and tree recorded above |
| `git blame -L 2188,2193 -- Docs/researches/math_theorems.md` and `git blame -L 9066,9071 -- Docs/researches/math_theorems.md` | 0 | both uncited catalogue records originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| repository crosswalk search for `THM-M-0305`, `THM-M-1239`, `THM-M-0998`, both Poincare spellings, and both glosses | 0 | assigned record, same-gloss PDE duplicate, and distinct variance target confirmed; no evidence transferred |
| Crossref metadata query for DOI `10.2307/2369620` | 0 | Poincare paper title, author, American Journal of Mathematics 12(3), March 1890, and starting page 211 confirmed; metadata only, no statement mapping or H0 credit |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake 5.0.0-src+98dc76e; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` and `rev-parse 'HEAD^{tree}'` | 0 each | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...b1d2` and `321626c8...2d81`, recorded in structured artifacts |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0305/IntakeProbe.lean)` | 0 | six adjacent pinned `eLpNorm`, derivative, and Gagliardo-Nirenberg-Sobolev interfaces elaborated; no target theorem was stated |
| bounded exact-topic `rg` over pinned mathlib and repo-local Lean | 0 | only the distinct probability target had Poincare-inequality names; adjacent mathlib results are named Gagliardo-Nirenberg-Sobolev; not a global absence claim |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, finalized `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 each | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0305-pycache python3 -m py_compile Stage1_Instances/THM-M-0305/check_intake.py` | 0 | scoped validator compiles without writing generated files into the owned path |
| `python3 -B Stage1_Instances/THM-M-0305/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, null target, H1/M3/R4 boundary, duplicate exclusion, exact artifact inventory and hashes, provisional packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0305/check_intake.py` | 0 | public replay mode passes without requiring the scheduler-only root packet |
| prohibited-construct `rg` over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file `git diff --no-index --check` loop, plus `git diff --check -- Stage1_Instances/THM-M-0305 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics; no-index exit 1 for a new file was treated as a difference, not an error |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0305-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted receipt. Exact source selection and independent review,
duplicate identity and ownership, canonical Lean elaboration and mutation tests, discovery and
obligation freezes, typed graphs, proof, composition, trust closure, hermetic replay, deterministic
release bundle, independent verification, and master acceptance remain open. They prevent theorem
completion but do not invalidate the planned intake.
