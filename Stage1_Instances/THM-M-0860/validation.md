# Intake validation

Base revision: `464759128569180ab640c412cd80bc5dd2c3b44a`; base tree:
`8da3c9130640d08d4e179450a0418368d0454745`.

This validation covers target membership, the planned dossier and open task DAG, repository-source
provenance, bibliographic source-family discrimination, JSON and scoped invariants, a narrow pinned
Lean substrate probe, bounded local discovery, prohibited-construct hygiene, and whitespace. It
does not validate a canonical theorem statement or proof.

The preflight worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

Crossref metadata for DOI `10.1002/sapm1949281148` confirmed Shannon's article title, author,
journal, April 1949 date, volume 28, issue 1-4, and pages 148-152. The normalized record has
SHA-256 `36b60a49...d48920`. Unpaywall reported closed access and no repository copy; the normalized
access record has SHA-256 `95c3516d...8678954`. The publisher theorem text was unavailable and is
not credited.

The open 2022 secondary paper *Vizing's and Shannon's Theorems for Defective Edge Colouring* was
inspected only to discriminate the family. It defines finite undirected loopless multigraphs and
identifies the ordinary `d = 1` case as the classic bound
`chi'(G) <= floor (3 * Delta(G) / 2)`. Its observed PDF SHA-256 is
`05805185...8b1242`. This secondary formulation is not an H0 source or canonical statement.

## Environment fingerprint

- Platform: Linux 7.0.0-27-generic, x86_64.
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`; package worktree clean.
- `Formalizations/Lean/lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `Formalizations/Lean/lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Commands and results

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless `cwd` is
shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0860` | 0 | rank 1414; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| `git status --short --untracked-files=all` (preflight) | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6306,6311 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Crossref API query for `10.1002/sapm1949281148`, normalized with `jq`, then `sha256sum` | 0 | primary bibliographic identity confirmed; normalized SHA-256 `36b60a49...d48920` |
| Unpaywall API query for the same DOI, normalized with `jq`, then `sha256sum` | 0 | closed access and no repository copy confirmed; normalized SHA-256 `95c3516d...8678954` |
| 2022 secondary-source download plus `sha256sum`, `pdfinfo`, and `pdftotext` | 0 | modern family statement inspected; 13-page PDF SHA-256 `05805185...8b1242`; secondary evidence only |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0860/IntakeProbe.lean)` | 0 | ten adjacent multigraph-incidence, subgraph, edge-labeling, and simple-degree APIs elaborated; complete output SHA-256 `a0748324...298e6`; no target declaration |
| exact-topic `rg` search over pinned mathlib and repo-local Lean | 1 (expected no match) | no Shannon edge-colouring, chromatic-index, edge-chromatic, or proper edge-colouring declaration; intake discovery only |
| bounded `rg` search over pinned `Mathlib/Combinatorics/Graph` for degree, maximum degree, chromatic index, or edge colouring | 1 (expected no match) | explicit-edge multigraph directory contains substrate only; not a complete anchor audit |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0860-pycache python3 -m py_compile Stage1_Instances/THM-M-0860/check_intake.py` | 0 | scoped validator compiles without adding generated files to the owned path |
| `python3 -B Stage1_Instances/THM-M-0860/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H1/M4/R4 boundary, null formal target, exact inventory, worker packet, source hashes, dependency pins, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0860/check_intake.py` | 0 | public replay mode passes without the scheduler-only worker packet |
| prohibited-construct scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` for every owned file and the worker packet | 0 aggregate | no whitespace diagnostics; no-index exit 1 for each new file is only the expected new-file difference |
| `git diff --check -- Stage1_Instances/THM-M-0860 .stage1-worker-selftest.json` | 0 | no tracked whitespace diagnostics |

## Known downstream failures

- The matching primary publication is bibliographically identified but its theorem text was
  inaccessible; exact definitions, assumptions, formula, proof boundary, sharpness clause,
  correction state, lawful immutable preservation, and independent review remain open.
- Finite and loopless multigraph scope, parallel-edge identity, incidence and degree conventions,
  maximum degree, proper edge colouring, chromatic index, natural-number rounding, ordered binders,
  and degenerate cases are not frozen as one Lean proposition.
- No canonical Lean expression, minimal-import certificate, expression/environment fingerprint,
  checked alternate encoding, or required statement mutation exists.
- Exhaustive formal anchor audit, discovery and obligation freezes, typed graphs, proof,
  composition, readable reconstruction, trust closure, hermetic replay, deterministic bundle,
  independent release verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze the received scope
and open the downstream DAG. Only the integration lane may accept the provisional worker receipt.
