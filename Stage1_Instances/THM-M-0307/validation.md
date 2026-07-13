# Intake validation

Base revision: `d257e1e5e5fa003d6e1f26344c0331bf99374fa9`; base tree:
`fa06b50b528e038d182d5479a18296f63fa5eae5`.

This validation covers target membership, the planned dossier and open task DAG, source and
duplicate-record boundaries, exact owned-file invariants, and a narrow pinned Lean substrate
probe. Because the catalog does not select one proposition, no canonical target, expression hash,
mutation result, source acceptance, transport, or proof is claimed. The automation-provided
canonical `.lake` symlink and pinned artifacts were used read-only; no dependency update, build,
clone, fetch, or `.lake` mutation was performed. The symlink is a pre-existing out-of-scope
untracked automation input, so this is nonrelease worker evidence.

## Commands and results

All commands ran from the worker clone root on 2026-07-13 (Asia/Shanghai), except where a `cwd` is
shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0307` | 0 | rank 1308; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (preflight) | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; preserved read-only |
| `git rev-parse HEAD` and `git rev-parse 'HEAD^{tree}'` | 0 each | base revision and tree recorded above |
| `git blame -L 2202,2207 -- Docs/researches/math_theorems.md` and `git blame -L 9052,9057 -- Docs/researches/math_theorems.md` | 0 | both identical uncited catalog blocks originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| repository crosswalk search for `THM-M-0307`, both trace-theorem records, neighboring Sobolev targets, and exact-topic Lean terms | 0 | one retained target, byte-identical source duplicate, proposition-changing scope choices, and neighbor exclusions confirmed; no evidence transferred |
| Crossref work-metadata query for DOI `10.1090/S0002-9939-96-03132-2` | 0 | confirmed Ding, title, journal, volume 124(2), 1996, and pages 591-600; metadata only, no source statement mapping or H0 credit |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake 5.0.0-src+98dc76e; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` and `rev-parse 'HEAD^{tree}'` | 0 each | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | no output; pinned dependency tree remained clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0307/IntakeProbe.lean)` | 0 | six adjacent pinned `Lp`, measure-restriction, manifold-boundary, and smooth Sobolev-inequality interfaces elaborated; no target theorem was stated |
| bounded exact-topic `rg` over pinned mathlib | 1 (expected no match) | no exact `TraceOperator`, `SobolevTrace`, or Sobolev boundary-trace theorem name found; not a global absence claim or downstream anchor audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, finalized `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 each | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0307-pycache python3 -m py_compile Stage1_Instances/THM-M-0307/check_intake.py` | 0 | scoped validator compiles without writing generated files into the owned path |
| `python3 -B Stage1_Instances/THM-M-0307/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, H5/M4/R4 planned boundary, null target, source hashes, exact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0307/check_intake.py` | 0 | public replay mode passes without requiring the scheduler-only root packet |
| prohibited-construct `rg` over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file `git diff --no-index --check` loop, plus `git diff --check -- Stage1_Instances/THM-M-0307 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics; no-index exit 1 for a new file was treated as a difference, not an error |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0307-INTAKE` only. It supports a
truthful `planned` dossier, not an accepted receipt. Exact source selection and independent review,
canonical Lean elaboration and mutation tests, discovery and obligation freezes, typed graphs,
proof, composition, trust closure, hermetic replay, deterministic release bundle, independent
verification, and master acceptance remain open. They prevent theorem completion but do not
invalidate the planned intake.
