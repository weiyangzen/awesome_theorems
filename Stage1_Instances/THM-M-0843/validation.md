# Intake validation

Validation date: `2026-07-13` (`Asia/Shanghai`). Base revision:
`d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`.

This validates target membership, the planned dossier and open task DAG, source and dependency
pins, JSON and cross-file invariants, and a narrow exact-type probe against existing pinned
mathlib. The pre-existing canonical `.lake` link and artifacts were used read-only. No dependency
update, build, clone, fetch, or other mutation was run.

The Lean probe establishes only that the named candidate and definitions elaborate in the pinned
environment. It does not choose the canonical source variant, serialize the target expression, run
statement mutations, audit the terminal proof body's provenance or axioms, or grant proof credit.

## Commands and results

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0843` | exit 0; rank 1032, planned, no legacy slot, legacy artifacts unaccepted, theorem_complete false |
| `git status --short --untracked-files=all` | preflight exit 0; only the automation-provided untracked `Formalizations/Lean/.lake` link existed before the intake |
| `git rev-parse HEAD 'HEAD^{tree}'` | exit 0; base commit `d502dd6f3d278ca9cb0ead8cbdc5f16c0e1fd8c9`, tree `829a47c47ae831cada4f8acc6c2c00ba5883215e` |
| `git blame -L 6187,6192 -- Docs/researches/math_theorems.md` | exit 0; all six catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --max-time 30 -A 'Mozilla/5.0' -sS 'https://drops.dagstuhl.de/storage/00lipics/lipics-vol237-itp2022/LIPIcs.ITP.2022.9/LIPIcs.ITP.2022.9.pdf' -o /tmp/srl-itp.pdf` | exit 0; retrieved the DOI-publisher copy outside the repository |
| `file /tmp/srl-itp.pdf && wc -c /tmp/srl-itp.pdf && sha256sum /tmp/srl-itp.pdf && pdfinfo /tmp/srl-itp.pdf` | exit 0; PDF 1.5, 771321 bytes, 19 pages, SHA-256 `9907f0304a3c19a019fb199c189c196d28567fd0b19a79a2d698c27616295e72` |
| `pdftotext -layout /tmp/srl-itp.pdf /tmp/srl-itp.txt` | exit 0; text extraction completed outside the repository |
| `rg -n -C 15 'Theorem 1|theorem szemeredi_regularity|Regular partitions of graphs' /tmp/srl-itp.txt` | exit 0; Theorem 1 at article page 9:3, the effective Lean display at page 9:10, and the 1975 primary-source citation located; source lead only, no H0 |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | exit 0; Lean 4.29.0 commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake 5.0.0-src+98dc76e |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | exit 0; revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | exit 0; empty output |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0843/IntakeProbe.lean)` | exit 0; exact types for pair uniformity, partition uniformity, equipartition, explicit bound, and `szemeredi_regularity` elaborated |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and the root worker packet | exit 0 for each after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0843-pycache python3 -m py_compile Stage1_Instances/THM-M-0843/check_intake.py` | exit 0; validator compiled without generated files in the owned path |
| `python3 -B Stage1_Instances/THM-M-0843/check_intake.py --worker-packet .stage1-worker-selftest.json` | exit 0; manifest/DAG identity, H1/M3/R4 boundary, source and mathlib pins, exact artifact inventory, receipt/packet, and six open tasks agree |
| prohibited Lean construct scan over the owned probe | exit 1 as expected for no match; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped per-new-file whitespace checks and `git diff --check` | exit 0; no whitespace errors |

## Known open gates

The exact source variant, incorporated definitions and exceptional-pair convention, primary 1975
source and errata, checked relationship of the effective equitable theorem to the catalog claim,
and independent source review remain open. So do the normalized canonical Lean expression and
environment fingerprint, checked transports, all four mutation classes, exhaustive anchor and
proof-body provenance audit, obligation/discovery freezes, typed graphs, proof/composition and
trust evidence, readable reconstruction, hermetic replay, deterministic bundle, independent
verification, and master acceptance. These boundaries prevent audit and theorem completion but do
not invalidate a truthful self-tested `planned` intake.
