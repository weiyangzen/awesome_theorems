# Intake validation

Base revision: `9c75282d42a7ef447d885d1d56997a79418bcd8a`; base tree:
`cc5285432a02107fadffb68c698690d1b98ac5f2`.

This validation covers target membership, the planned dossier and open task DAG, duplicate and
neighbor boundaries, source-family discrimination, exact owned-file invariants, and a narrow pinned
Lean substrate probe. Because the catalog does not select one exact proposition, no canonical
target, expression hash, mutation result, source acceptance, transport, or proof is claimed. The
automation-provided canonical `.lake` symlink and pinned artifacts were used read-only; no dependency
update, build, clone, fetch, or `.lake` mutation was performed. The symlink is a pre-existing out-of-
scope untracked automation input, so this is nonrelease worker evidence.

## Commands and results

All commands ran from the worker clone root on 2026-07-13 (Asia/Shanghai), except where a `cwd` is
shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0974` | 0 | rank 1508; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all` (pre-edit preflight) | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; preserved read-only |
| `git rev-parse HEAD` and `git rev-parse 'HEAD^{tree}'` | 0 each | base revision and tree recorded above |
| `git blame -L 7113,7118 -- Docs/researches/math_theorems.md` and `git blame -L 7301,7306 -- Docs/researches/math_theorems.md` | 0 | both identical uncited catalog blocks originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| repository crosswalk search for `THM-M-0974`, both catalog blocks, `THM-M-1081`, neighboring concentration targets, and exact-topic Lean terms | 0 | one retained target, one byte-identical source duplicate, distinct neighboring target ownership, and proposition-changing scope choices confirmed; no evidence transferred |
| Crossref and publisher article inspection for DOI `10.1007/BF02699376` | 0 | confirmed Talagrand, title, journal, volume 81, 1995, pages 73-205; inspected the introduction and Section 4.1 source lead; no source acceptance or H0 credit |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake 5.0.0-src+98dc76e; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` and `rev-parse 'HEAD^{tree}'` | 0 each | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | no output; pinned dependency tree remained clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0974/IntakeProbe.lean)` | 0 | six adjacent convexity, Lipschitz, product-measure, and generic sub-Gaussian interfaces elaborated; no target theorem was stated |
| bounded exact-topic `rg` over repository Lean and pinned mathlib | 0; 21 contextual matches | matches were a legacy `T2` transportation interface and an unrelated citation; no source-identical Talagrand convex-Lipschitz declaration was found; not a global absence claim or downstream anchor audit |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, finalized `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 each | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0974-pycache python3 -m py_compile Stage1_Instances/THM-M-0974/check_intake.py` | 0 | scoped validator compiles without writing generated files into the owned path |
| `python3 -B Stage1_Instances/THM-M-0974/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/DAG identity, H1/M4/R4 planned boundary, null target, source hashes, exact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0974/check_intake.py` | 0 | public replay mode passes without requiring the scheduler-only root packet |
| prohibited-construct `rg` over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file `git diff --no-index --check` loop, plus `git diff --check -- Stage1_Instances/THM-M-0974 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics; no-index exit 1 for a new file was treated as a difference, not an error |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0974-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted receipt. Exact source selection and independent review, canonical
Lean elaboration and mutation tests, discovery and obligation freezes, typed graphs, proof,
composition, trust closure, hermetic replay, deterministic release bundle, independent verification,
and master acceptance remain open. They prevent theorem completion but do not invalidate the
planned intake.
