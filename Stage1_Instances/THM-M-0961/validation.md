# Intake validation

Base revision: `a3b18eec39bf04be025b1641cae02f4d44fdf11a`; base tree:
`fdfff18dea4c6798c5b322b6088dfe556109c134`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, primary-paper and secondary-source discrimination, JSON and scoped invariants, a narrow
pinned Lean substrate probe, bounded repository/mathlib search, prohibited-construct hygiene, and
whitespace. It does not validate a canonical theorem statement or proof.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

The DOI landing record, Crossref response, and CORE abstract metadata identify Meshulam's JCTA 71
(1995), pages 168-172 paper. CORE says the ambient group has odd order and reports a direct-sum
bound, but the exposed formula is damaged by text conversion, so its parentheses, factor
hypotheses, and exact proposition were not frozen. The complete article was unavailable through the
inspected unauthenticated interfaces. No remote source was added to the repository.

Bateman-Katz arXiv `1101.5851v2` was inspected as a secondary disambiguation lead. It reports
Meshulam's `F_3^N` cap-set density bound as order `1 / N` and distinguishes its own later
`1 / N^(1 + epsilon)` improvement. It is not the primary source. No immutable H0 admission,
theorem/page transcription, complete definition/assumption/proof/errata mapping, or independent
review is claimed.

Liu-Spencer-Zhao's 2011 publisher-version paper was also inspected. Printed pages 258-259 attribute
the exact bound `D3(G) <= 2|G|/c(G)` to Meshulam's Theorem 1.2 and define `c(G)` through the
nontrivial invariant factors of finite odd-order `G`. Its 230,742-byte, seven-page PDF has SHA-256
`cae43200...fded4`. This repairs the abstract formula as a high-confidence retrospective statement
lead, but it is not direct inspection or independent acceptance of the primary theorem.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a different
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0961` | 0 | rank 1495; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree shown above |
| `git blame -L 7015,7020 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| DOI/Crossref/CORE metadata inspection for DOI `10.1016/0097-3165(95)90024-1` | 0 | matching author, title, journal, volume, issue, date, and pages; CORE abstract narrows domain to finite odd-order abelian groups but its inequality is text-damaged; DOI, Crossref, and CORE response hashes recorded in `instance.json`; mutable discovery inputs, not replay-stable recipes |
| download and text inspection of `https://arxiv.org/pdf/1101.5851v2` | 0 | 38-page secondary paper; introduction reports Meshulam density `O(1/N)` for `F_3^N`, Section 3 reviews the argument; PDF SHA-256 `e78cf5cc...18a6b`; not H0 evidence |
| download and text inspection of Liu-Spencer-Zhao (2011), DOI `10.1016/j.ejc.2010.09.008` | 0 | printed pages 258-259 identify Meshulam Theorem 1.2, exact `2|G|/c(G)` bound, odd-order domain, and invariant-factor definition; PDF SHA-256 `cae43200...fded4`; retrospective source lead, not direct H0 evidence |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `651c8acc...85b1d2` and `321626c8...2d81` as recorded in structured artifacts |
| `(cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0961/IntakeProbe.lean)` | 0 | seven adjacent 3AP, extremal-cardinality, finite-abelian decomposition, and Roth APIs elaborated; complete output SHA-256 `2ae26455...0d720`; no target statement or proof credit |
| bounded case-insensitive Meshulam/cap-set/finite-abelian-3AP search over pinned mathlib, repo-local Lean, and target instances | 0 | only the new probe comment plus an unrelated Fermat exponent string matched; no source-identical quantitative Meshulam declaration; intake discovery only |
| `python3 -m json.tool` on `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0961-pycache python3 -m py_compile Stage1_Instances/THM-M-0961/check_intake.py` | 0 | scoped validator compiles without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0961/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H1/M4/R4 boundary, source hashes, null target, artifact inventory, packet agreement, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0961/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited-construct scan over `IntakeProbe.lean` | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0961 .stage1-worker-selftest.json` | 0 | tracked-diff command emitted no diagnostics; untracked new-file coverage comes from the preceding no-index checks |

## Status boundary

This is provisional worker self-test evidence for `S56-M-0961-INTAKE` only. It supports a truthful
`planned` dossier, not an accepted node receipt. Exact primary-source transcription and independent
review, canonical Lean elaboration and statement mutations, complete anchor audit and discovery
freeze, obligation registry, typed graphs, proof, composition, trust closure, hermetic replay,
deterministic release bundle, and independent verification remain open. These failures prevent
statement, audit-completion, and theorem-completion claims, but they do not invalidate the planned
intake.
