# Intake validation

Base revision: `3ef3a6bf4f2f9b86930beb27693f7429fea3e63a`; base tree:
`c9eba4c65f6e228f9cefc8bdf62136b7fb69426a`.

This validation covers target membership, the planned dossier and open task DAG, catalog and
primary-source provenance, JSON and scoped invariants, a narrow pinned Lean substrate probe, a
bounded repo-local and mathlib search, prohibited-construct hygiene, and whitespace. It does not
validate a canonical theorem statement or proof because the source-approved historical-to-modern
transport and exact Lean encoding belong to the downstream statement phase and remain open.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

The AMS-hosted primary article was inspected: Hassler Whitney, *Non-separable and planar graphs*,
Transactions of the American Mathematical Society 34(2) (1932), 339-362, DOI
`10.1090/S0002-9947-1932-1501641-2`. Article pages 339-343 define the historical finite graph,
chain, suspended chain, circuit, non-separability and related qualifications. Pages 349-350 prove
Theorem 18; page 350 states Theorem 19's circuit-plus-successive-arcs-or-suspended-chains
construction and the following converse. The observed 24-page PDF SHA-256 is
`dc5b3da59a06b4b6f21bd424add1d28576b059143a470f2593257a0073d14fa5`.

Crossref confirmed the author, year, volume, issue, pages, and DOI, and identified the 1931 PNAS
outline. The PDF was not added to the repository. Immutable source admission, the complete
definition/premise/proof-node/correction map, transport from Whitney's loop/parallel-arc model and
non-separability to the catalog's modern 2-connected wording, and independent review remain open.
This is `H1` source evidence rather than `H0`.

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
| `python3 scripts/stage1_target.py show THM-M-0863` | 0 | rank 1417; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6327,6332 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `curl -A 'Mozilla/5.0' -L --fail --silent --show-error --max-time 30 -o /tmp/whitney1932-ams.pdf 'https://www.ams.org/journals/tran/1932-034-02/S0002-9947-1932-1501641-2/S0002-9947-1932-1501641-2.pdf?active=current'`, followed by `sha256sum`, `pdfinfo`, and `pdftotext -layout` on that file | 0 | primary definitions, Theorems 5-8 and 18, Theorem 19 and its converse inspected; observed PDF digest recorded above; no repository source admission or H0 claim |
| `curl -L --fail --silent --show-error --max-time 30 'https://api.crossref.org/works/10.1090/S0002-9947-1932-1501641-2'` | 0 | published bibliographic identity confirmed; a title query separately identified the earlier 1931 PNAS outline lead |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0863/IntakeProbe.lean)` | 0 | nine adjacent connectivity, path, cycle, induced-subgraph, vertex-deletion and walk-to-subgraph APIs elaborated; complete output SHA-256 `fb9e46a5268e0922d4e3691657e756d5e8324f700f823b4f9d0275fa5dbdf7cf`; no target declaration |
| `rg -n -i --glob '*.lean' '\bear([ _-]decomposition|[ _-]decomp|Decomposition|Decomp)\b|\bopen[ _-]ear\b|\bsuspended[ _-]chain\b|\bnon[ _-]?separable[ _-]graph\b|\bbiconnected\b|\bvertex[ _-]?(2|two)[ _-]?connect|\btwo[ _-]?vertex[ _-]?connect' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | 1 (expected no match) | no ear-decomposition, suspended-chain, non-separable-graph, biconnected, or named vertex-2-connectivity declaration; intake discovery only |
| four separate `python3 -m json.tool <path>` invocations for `instance.json`, `task-dag.json`, `intake-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| `python3 -c "from pathlib import Path; compile(Path('Stage1_Instances/THM-M-0863/check_intake.py').read_text(), 'check_intake.py', 'exec'); print('python AST compile: ok')"` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0863/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H1/M4/R4 boundary, null formal target, source and dependency pins, exact inventory, worker packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0863/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited Lean proof-escape scan over the API probe | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| for every new file, `git diff --no-index --check -- /dev/null <path>` with status 1 accepted only when diagnostic output is empty; then `git diff --check -- Stage1_Instances/THM-M-0863 .stage1-worker-selftest.json` | 0 aggregate | no whitespace diagnostics |

## Known downstream failures

- The source is not yet an accepted immutable repository record, and its definitions, premises,
  proof nodes, correction state, source-model transport, and independent review remain open.
- The catalog does not choose the construction direction, converse, or biconditional. Whitney's
  non-separable finite graph with loops/parallel arcs has not been transported to an exact modern
  simple-graph 2-vertex-connectivity predicate with all small-case qualifications.
- Exact initial-cycle, ear, endpoint, internal-vertex, partial-union, coverage, finite graph,
  ordered-binder, and boundary-case encodings are not frozen.
- No canonical Lean expression, minimal-import certificate, expression/environment fingerprint,
  checked alternate encoding, or required statement mutation exists.
- Exhaustive formal anchor audit, discovery and obligation freezes, typed graphs, proof,
  composition, readable reconstruction, trust closure, hermetic replay, deterministic bundle,
  independent release verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze scope and open the
downstream DAG. Only the integration lane may accept the provisional worker receipt.
