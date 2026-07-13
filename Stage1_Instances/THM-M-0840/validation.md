# Intake validation

Base revision: `be8701e88e791545c16a262edd1909486d5cef4b`; base tree:
`78b0a751473bf6d71f453a6aad18b130268a3428`.

This validation covers target membership, the planned dossier and open task DAG, catalog and
primary-source provenance, JSON and scoped invariants, a narrow pinned Lean substrate probe, a
bounded repo-local and mathlib search, prohibited-construct hygiene, and whitespace. It does not
validate a canonical theorem statement or proof because the exact source-approved Lean encoding
belongs to the downstream statement phase and remains open.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

The journal-hosted primary article was inspected: Maria Chudnovsky, Neil Robertson, Paul Seymour,
and Robin Thomas, *The strong perfect graph theorem*, Annals of Mathematics 164(1) (2006), 51-229,
DOI `10.4007/annals.2006.164.51`. Article pages 51-52 define finite simple graphs, holes,
antiholes, Berge graphs, and perfect graphs and state Theorem 1.2, perfect if and only if Berge. The
observed PDF SHA-256 is
`f70115028dea55dec5a97f3a50af82686782821a612ca672ad666a19c0eba4c2`.

Crossref confirmed the authors, publication date, volume, issue, pages, and DOI. ArXiv metadata for
`math/0212070v1` identified the earlier 2002 version with matching authors and theorem abstract.
The PDF was not added to the repository. Immutable source admission, published/arXiv delta,
definition/premise/proof-node/errata mapping, lawful preservation, and independent review remain
open, so this is `H1` source evidence rather than `H0`.

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

All repository commands ran at the repository root on 2026-07-13 Asia/Shanghai unless a different
`cwd` is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0840` | 0 | rank 1397; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6166,6171 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| journal PDF download plus `sha256sum`, `pdfinfo`, and `pdftotext` | 0 | primary definitions and Theorem 1.2 inspected; 179-page observed PDF digest recorded above; no repository source admission or H0 claim |
| Crossref query for DOI `10.4007/annals.2006.164.51` and arXiv query for the title | 0 | published bibliographic identity and earlier `math/0212070v1` lead confirmed |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0840/IntakeProbe.lean)` | 0 | seven adjacent induced-graph, complement, cycle, chromatic-number, and clique-number APIs elaborated; complete output SHA-256 `c1793ea8f8d4f57060e4dfe03aea92186362c24a2d96116ba52592f14df8e43b`; no target declaration |
| exact-topic `rg` search over pinned mathlib and repo-local Lean | 1 (expected no match) | no strong-perfect-graph, Berge-graph, odd-hole/antihole, or perfect-graph declaration; intake discovery only |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| Python `compile` of `Stage1_Instances/THM-M-0840/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0840/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H1/M4/R4 boundary, null formal target, source and dependency pins, exact inventory, worker packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0840/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited Lean proof-escape scan over the API probe | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-new-file no-index whitespace checks plus `git diff --check` | 0 aggregate | no whitespace diagnostics |

## Known downstream failures

- The source is not yet an accepted immutable repository record, and its definitions, premises,
  proof nodes, correction state, published/arXiv delta, and independent review remain open.
- Exact perfectness and Berge predicates, induced-subgraph quantifier, hole/antihole encoding,
  chordlessness, parity and length convention, complement transport, finite graph presentation,
  `ENat`/`Nat` coercion, binder order, and degenerate cases are not frozen.
- No canonical Lean expression, minimal-import certificate, expression/environment fingerprint,
  checked alternate encoding, or required statement mutation exists.
- Exhaustive formal anchor audit, discovery and obligation freezes, typed graphs, proof,
  composition, readable reconstruction, trust closure, hermetic replay, deterministic bundle,
  independent release verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze scope and open the
downstream DAG. Only the integration lane may accept the provisional worker receipt.
