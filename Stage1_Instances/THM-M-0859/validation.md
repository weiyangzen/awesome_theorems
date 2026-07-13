# Intake validation

Base revision: `464759128569180ab640c412cd80bc5dd2c3b44a`; base tree:
`8da3c9130640d08d4e179450a0418368d0454745`.

This validation covers target membership, the planned dossier and open task DAG, repository and
source-lead provenance, JSON and scoped invariants, a narrow pinned Lean substrate probe, a bounded
repo-local and mathlib search, prohibited-construct hygiene, and whitespace. It does not validate a
canonical theorem statement or proof because the primary-source variant and exact Lean encoding
belong to the downstream statement phase and remain open.

The initial worktree contained only the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. It was used read-only. No
`lake update`, `lake build`, dependency clone or fetch, network-triggering Lake operation, or other
`.lake` mutation was performed. The owned intake files and root worker packet make the final tree
dirty and nonrelease.

## Source discovery boundary

The permanent Encyclopedia of Mathematics revision `51407`, "Vizing theorem," was inspected. It
defines finite undirected loopless multigraphs, maximum parallel-edge multiplicity `mu(G)`,
chromatic index `chi'(G)`, and maximum degree `Delta(G)`, and states
`Delta(G) <= chi'(G) <= Delta(G) + mu(G)`, with the simple-graph specialization
`Delta(G) <= chi'(G) <= Delta(G) + 1`. Its API response SHA-256 is
`297d62ed131d0525be872a166fab52dc58076390c1d5108c0fc45ab3d9a667dc`.

The entry cites V. G. Vizing, "On an estimate of the chromatic class of a p-graph," *Diskret.
Anal.* 3 (1964), 25-30 (Russian). Crossref metadata for the related paper "The chromatic class of a
multigraph," DOI `10.1007/BF01885700`, confirms that citation; the observed response SHA-256 is
`f181278eff02d585bc149fdb8975097c438480e3721b9143ba9bd0862bcd4f69`.
The primary 1964 text was not obtained or inspected. Its exact theorem/proof boundary, definitions,
translation, corrections, and the catalog's multigraph-versus-simple intent remain open, so this is
`H1` source evidence rather than `H0`.

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
| `python3 scripts/stage1_target.py show THM-M-0859` | 0 | rank 1413; planned; no legacy slot; legacy artifacts unaccepted; theorem_complete false |
| initial `git status --short --untracked-files=all` | 0 | only `?? Formalizations/Lean/.lake`; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree shown above |
| `git blame -L 6299,6304 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| Encyclopedia of Mathematics API query for permanent revision `51407` plus `sha256sum` | 0 | secondary definitions, general bound, simple specialization, and 1964 bibliography inspected; digest above; no primary-source or H0 claim |
| Crossref query for DOI `10.1007/BF01885700` plus `sha256sum` | 0 | related 1965 metadata and its 1964 reference confirmed; digest above; primary full text not inspected |
| `(cd Formalizations/Lean && lake env lean --version && lake --version)` | 0 | Lean and Lake versions agree with the fingerprint; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned mathlib revision/tree above; package worktree clean |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0859/IntakeProbe.lean)` | 0 | seven adjacent edge-set, line-graph, coloring, and degree APIs plus the prospective simple proposition elaborated; output SHA-256 `08181e2e2c404cf8f738cf6f97f75f21cc5fd170f6492317ed667c944e42bffd`; no canonical target declaration |
| exact-topic `rg` search over pinned mathlib and repo-local Lean | 0 | only two `EdgeLabeling` documentation occurrences; they explicitly distinguish arbitrary labels from proper edge coloring; no Vizing or chromatic-index declaration; intake discovery only |
| `python3 -m json.tool` on all structured owned artifacts and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| Python `compile` of `Stage1_Instances/THM-M-0859/check_intake.py` | 0 | scoped validator parses without writing bytecode |
| `python3 -B Stage1_Instances/THM-M-0859/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target identity, planned H1/M4/R4 boundary, null target, source and dependency pins, exact inventory, worker packet, and six open tasks agree |
| `python3 -B Stage1_Instances/THM-M-0859/check_intake.py` | 0 | public replay mode passes without the scheduler-only packet |
| prohibited Lean proof-escape scan over the API probe | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| scoped byte checks plus `git diff --check` | 0 aggregate | final newlines present; no invalid bytes, trailing whitespace, or diff diagnostics |

## Known downstream failures

- The 1964 primary Russian source is not inspected or immutably admitted; its translation,
  definitions, premises, theorem and proof nodes, correction state, and independent review remain
  open.
- The catalog does not choose the loopless-multigraph `Delta + mu` theorem or the finite-simple-
  graph `Delta + 1` specialization. Graph/multiplicity representation, proper edge-coloring and
  chromatic-index definitions, lower-bound composition, binder order, and degenerate cases are not
  frozen.
- No canonical Lean expression, minimal-import certificate, expression/environment fingerprint,
  checked direct/line-graph transport, or required statement mutation exists.
- Exhaustive formal anchor audit, discovery and obligation freezes, typed graphs, proof,
  composition, readable reconstruction, trust closure, hermetic replay, deterministic bundle,
  independent release verification, and master acceptance remain open.

These failures prevent statement, audit-completion, and theorem-completion claims. They do not
invalidate a truthful, self-tested `planned` intake whose purpose is to freeze scope and open the
downstream DAG. Only the integration lane may accept the provisional worker receipt.
