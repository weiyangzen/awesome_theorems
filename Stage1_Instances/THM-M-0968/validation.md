# Intake validation

Base revision: `fcabbf1e0ad9507eebe91663bccabfa87d22813e` (tree
`873e589c594454b7f263c7ed2342089a4d15e842`).

Commands were run from the repository root on 2026-07-13 (Asia/Shanghai), except where the table
gives another working directory. The automation-provided `Formalizations/Lean/.lake` symlink was
present before this work and was used read-only. No `lake update`, `lake build`, dependency clone or
fetch, network-triggering Lake operation, or `.lake` mutation was performed. This dirty worker
snapshot is nonrelease evidence.

## Source and statement inspection

The catalog supplies the conflicting title `Erdős盒原理` (literally an Erdős box principle), Paul
Erdős, 1965, and the gloss `超图中的匹配` (matchings in hypergraphs), but no citation or proposition.
Ordinary pigeonhole is separately owned by `THM-M-0914`. An institutional scan of Erdős's 1965
paper *A problem on independent r-tuples* strongly matches the attribution, date, and gloss, but
its page-94 sufficiently-large-`n` theorem differs materially from its page-95 unrestricted formula
(9), which the paper presents as an elusive problem. No independent source review selects either
candidate. Intake therefore leaves the mathematical and Lean targets null and proposes
`[H5, M4, R4]` only for the received unstable record.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0968` | 0 | rank 1502; planned; intake score 86; L0; no legacy slot; theorem incomplete |
| `git status --short --untracked-files=all` | 0 | initially only the pre-existing automation `.lake` symlink was untracked |
| `git rev-parse HEAD HEAD^{tree}` | 0 | base revision and tree above |
| `git blame -L 7071,7076 -- Docs/researches/math_theorems.md` | 0 | all six uncited target lines originate in catalog-introduction commit `bcf3f9fa...` |
| institutional PDF inspection and hashing | 0 | four scan pages, 413744 bytes, SHA-256 `56e7147c...09bf`; article pages 93-95 plus volume index |
| zbMATH Open record `3221072` / `Zbl 0136.21302` inspection | 0 | bibliographic match and equation-(8) correction lead found; no source admission or H0 credit |
| bounded case-insensitive `rg` over pinned mathlib and repo-local Lean for Erdős matching/box, matching conjecture, independent r-tuples, and hypergraph matching | 1 | expected no-match discovery result; not an exhaustive anchor audit or global absence claim |

## Environment

- Linux `7.0.0-27-generic`, x86_64; timezone Asia/Shanghai.
- Lean `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake `5.0.0-src+98dc76e`.
- Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; source tree clean.
- Toolchain and dependency manifest SHA-256 values are `651c8acc...b1d2` and
  `321626c8...2d81`. The exact values and adjacent mathlib source hashes are frozen in
  `instance.json` and checked by `check_intake.py`.

## Scoped validation

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0968/IntakeProbe.lean` | 0 | seven adjacent finite-family/disjointness APIs elaborated; complete stdout SHA-256 `1211f248...f1e` |
| `python3 -m json.tool` on all structured owned JSON and the worker packet | 0 | all JSON parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0968-pycache python3 -m py_compile Stage1_Instances/THM-M-0968/check_intake.py` | 0 | scoped validator compiled without adding an owned cache |
| `LC_ALL=C TZ=UTC python3 -B Stage1_Instances/THM-M-0968/check_intake.py` | 0 | public replay validates target identity, source hashes, planned boundary, exact inventory, and six open tasks |
| `LC_ALL=C TZ=UTC python3 -B Stage1_Instances/THM-M-0968/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | worker packet's exact seven-key schema and receipt agreement also pass |
| scoped Lean regex scan for `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declarations | 1 | expected no-match; the API probe contains no prohibited declaration |
| per-file `git diff --no-index --check /dev/null <new-file>` for all nine owned files and the worker packet | 1 each | expected new-file diff status with no whitespace diagnostics |
| `git diff --check -- Stage1_Instances/THM-M-0968 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics; the no-index commands cover untracked files |

The exact structure and Lean recipes in `intake-receipt.json` deny network access as a receipt
policy, freeze `LC_ALL=C` and `TZ=UTC`, and bind their inputs and stdout by SHA-256. This worker did
not claim OS-level network isolation or release-grade hermeticity.

## Boundary

These checks self-test only the `S56-M-0968-INTAKE` planned dossier proposal. They do not select an
exact theorem, establish source fidelity, elaborate a canonical target, create proof evidence, or
close any dependent node. Master acceptance, the six downstream tasks, audit completion, and
theorem completion remain open.
