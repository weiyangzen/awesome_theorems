# THM-M-0871 intake validation

## Scope

This record validates only the `planned` dossier, scope map, source-statement crosswalk, open task
DAG, primary-source leads, and discovery-only pinned Lean API probe. It does not validate an exact
Courcelle proposition, an MSO/CMSO encoding, a treewidth definition, a decision procedure, a
complexity theorem, an accepted receipt, audit completion, or theorem completion.

The worker tree was nonrelease-dirty throughout: the automation-provided canonical `.lake` link was
already untracked, and this intake's owned artifacts plus the root self-test packet were new. No
dependency content, authority file, generated checklist, execution-DAG state, or other target path
was modified. The `.lake` link was used read-only; no `lake update`, `lake build`, dependency clone
or fetch, or other dependency mutation was performed.

## Environment

- Repository base: `748243faadc15828fb087059337fd05b7be9fdeb`
- Base tree: `e46d642646f80980838b6f016f5d69b817bd464d`
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`
- Lake: `5.0.0-src+98dc76e`
- mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- mathlib tree: `bdc39a3123201dae413a9d9be56ec242c19e5c2b`
- Platform: Linux `7.0.0-27-generic`, `x86_64`
- Timezone/date: Asia/Shanghai, 2026-07-13

Complete published scans of Courcelle's 1990 and 1992 articles were observed through bounded HTTP
requests. Their SHA-256 values were
`e5989841626dc08c5acea6fd6bfb8c2413ff86d9c5b16f80aba5c6cfb7f42acd` and
`b73c2e11a5311f6f69ced7815d72ccc1b65cb476c24b4e3b4ac0f58acef08774`. They were
inspected only to identify the theorem family, exact source results, and material variants. They
were not vendored or accepted as H0, and complete correction/proof-node review plus independent
review remain open.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0871` | 0 | rank 1425, planned, L0/rework_required, no legacy slot, theorem_complete false |
| `git status --short --untracked-files=all` at preflight | 0 | only the pre-existing untracked canonical `.lake` link existed before this intake; preserved read-only |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 6383,6388 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded download, hashing, PDF metadata, and text inspection of Courcelle 1990, DOI `10.1016/0890-5401(90)90043-H` | 0 | complete 64-page, 3,341,918-byte scan; Definitions 3.1-3.2, Theorem 4.4, Corollaries 4.8/4.10, and Proposition 4.14 located; primary-source discovery only |
| bounded download, hashing, PDF metadata, and text inspection of Courcelle 1992, DOI `10.1051/ita/1992260302571` | 0 | complete 31-page, 2,737,945-byte scan; logical-language passage, treewidth Definition 2.1, Section 3, and Proposition 3.1 located; primary-source discovery only |
| bounded inspection of Courcelle's author publication index | 0 | no explicit correction link located for the 1990 or 1992 articles; bounded observation only, not proof that no erratum exists |
| bounded word-boundary search for Courcelle, treewidth, tree decomposition, monadic second-order graph logic, and bounded-treewidth model checking over repo-local and pinned Lean | 1 expected | no exact-topic match; bounded search is not a complete anchor audit or global absence proof |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0871/IntakeProbe.lean` | 0 | seven adjacent pinned APIs elaborated; two axiom reports contain only `propext` and `Quot.sound`; no target theorem introduced; exact output SHA-256 `46545b575aee16710a489611c2038586516077463b8c24492139742a7bd0d860` |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON after finalization |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0871-pycache python3 -m py_compile Stage1_Instances/THM-M-0871/check_intake.py` | 0 | scoped validator parses without writing cache files under the owned path |
| `python3 -B Stage1_Instances/THM-M-0871/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/item identity, null target, H1/M4/R4 boundary, source and pin hashes, receipt/packet agreement, exact inventory, and six open tasks agree |
| prohibited-construct `rg` over `IntakeProbe.lean` | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check` plus per-new-file no-index whitespace checks | 0 | no whitespace diagnostics |

The final JSON, invariant, and whitespace results were recorded after receipt and worker-packet
creation.

## Known failures and boundary

Master acceptance is pending. Exact primary-source root selection, complete correction and
proof-node review, graph/logic/decomposition/uniformity/complexity mapping, neighbor-target
reconciliation, and independent source review remain open. So do the canonical Lean target,
minimal imports, expression and environment fingerprints, checked transports, statement mutations,
exhaustive anchor audit, obligation registry, typed graphs, proof, composition, trust closure,
readable reconstruction, hermetic replay, deterministic bundle, and independent verification.

Verdict: `no_state_change`. This self-tested worker proposal may be handed off as `[_]`; it remains
unfinished and unaccepted. `audit_complete=false` and `theorem_complete=false`.
