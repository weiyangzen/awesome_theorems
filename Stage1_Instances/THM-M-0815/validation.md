# Intake validation

Base revision: `adc87f8ea24dcc7c5e2668c0a5ede0ca5c5f0f55`; base tree:
`3c83596059f716cde0d50a5f6b390ada6ca7c8e1`. Validation date: `2026-07-13`
(`Asia/Shanghai`).

This validation covers target membership, the fail-closed planned dossier, source provenance,
scope and open-task invariants, JSON and Python syntax, a narrow pinned Lean candidate-interface
probe, prohibited-construct hygiene, and whitespace. It does not validate a canonical Hall
proposition or proof because the primary statement and one-side-saturation versus graph-wide-
perfect semantic fork are not frozen.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, or other `.lake` mutation was performed.
The owned intake files and root worker packet make the final tree dirty and nonrelease.

## Source boundary

The six-line repository record was traced to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. Pinned mathlib bibliography, Crossref, and
Semantic Scholar corroborate P. Hall's 1935 article, but the primary PDF routes returned HTTP 403.
No primary proposition, proof, or errata was inspected. The secondary arXiv formalization paper
was inspected and supplies exact standard finite-family, finite-relation, and one-side graph
versions; it is not H0 evidence and cannot resolve the catalog's use of "perfect matching."

## Environment fingerprint

- Platform: Linux x86_64; kernel `7.0.0-27-generic`; timezone `Asia/Shanghai`.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

Commands ran from the repository root unless a `cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0815` | 0 | rank 1374; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 5991,5996 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -L --fail --silent --show-error --max-time 30 'https://api.crossref.org/works/10.1112/jlms/s1-10.37.26'` | 0 | transient 2402-byte metadata response observed with SHA-256 `9ce8715d...251aff`; discovery only, body not retained |
| `curl -L --fail --silent --show-error --max-time 30 'https://api.semanticscholar.org/graph/v1/paper/DOI:10.1112/jlms/s1-10.37.26?fields=title,authors,year,venue,externalIds,openAccessPdf,isOpenAccess,url'` | 0 | matching closed-access record observed; transient response digest recorded in the crosswalk, body not retained |
| `curl -L --fail --silent --show-error --max-time 30 'https://doi.org/10.1112/jlms/s1-10.37.26'` | 22 | expected primary-source blocker: redirect ended at HTTP 403; no primary-text claim made |
| `curl -L --fail --silent --show-error --max-time 30 -A 'Mozilla/5.0' 'https://londmathsoc.onlinelibrary.wiley.com/doi/pdf/10.1112/jlms/s1-10.37.26'` | 22 | expected primary-PDF blocker: HTTP 403 |
| `curl -L --fail --silent --show-error --max-time 30 'https://export.arxiv.org/api/query?id_list=2101.00127'` | 0 | 2317-byte Atom response observed with SHA-256 `9c0c9287...e1d49`; transient discovery only |
| `curl -L --fail --silent --show-error --max-time 60 -o /tmp/hall-paper.pdf 'https://arxiv.org/pdf/2101.00127v1'` | 0 | 284171-byte, 15-page secondary PDF inspected; SHA-256 `3521dd4b...ddb009`; transient and not release evidence |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake agree with the fingerprint; no update or build ran |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | pinned revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0815/IntakeProbe.lean)` | 0 | six interfaces, three definition-level boundary facts, and four axiom reports elaborated; output 2913 bytes, 33 lines, SHA-256 `d4d95cb4fa49e0a1a82de42b3379f66ad5df78e22474dc84af10c0911380ff68` |
| `rg -n -i 'Hall.?s? (marriage\|theorem)\|marriage theorem\|matching' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Combinatorics --glob '*.lean'` | 0 | direct family, relation, one-side graph, and global perfect-matching candidates located; semantic selection remains open |
| `python3 -m json.tool Stage1_Instances/THM-M-0815/instance.json` and the same command for `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| `python3 -c "import ast,pathlib; ast.parse(pathlib.Path('Stage1_Instances/THM-M-0815/check_intake.py').read_text(encoding='utf-8'))"` | 0 | scoped validator parses without generated bytecode |
| `python3 -B Stage1_Instances/THM-M-0815/check_intake.py` | 0 | durable public recipe: target, source pins, H1/M3/R4 boundary, null target, artifacts, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0815/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | scheduler handoff additionally agrees with dossier and provisional receipt |
| prohibited-construct scan over owned Lean | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0815 .stage1-worker-selftest.json` plus per-file `git diff --no-index --check /dev/null` for every new file | 0 aggregate | no tracked or untracked-file whitespace diagnostics |

The two structured actions in `intake-receipt.json` bind their exact start/end times, exits,
covered IDs/declarations, and stdout SHA-256 values. The receipt also binds every non-self-
referential owned artifact, the root packet, and the final worktree inventory; it excludes only
itself to avoid a recursive hash cycle. This remains provisional dirty-worker evidence, not a
content-addressed or master-accepted receipt.

## Known downstream failures

- No primary proposition, theorem/page locator, incorporated definitions, correction history,
  proof boundary, source-to-node mapping, or independent source review is frozen.
- The exact root could be a finite representatives iff, a one-side saturating graph matching, or a
  balanced/global perfect-matching result; graph coverage, balance, finiteness, theorem direction,
  binder order, and boundary cases remain open.
- No canonical Lean expression, minimal imports, expression/environment fingerprint, checked
  alternate encoding, or statement mutation is frozen.
- Candidate interfaces elaborate, but no normalized statement match, terminal-body provenance,
  transitive dependency/axiom audit, wrapper, or proof credit is accepted.
- Obligation registry, typed graphs, proof, composition, readable reconstruction, hermetic replay,
  deterministic bundle, independent verification, release, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze the ambiguity and
open the downstream DAG. Only the integration lane may accept the provisional worker receipt.
