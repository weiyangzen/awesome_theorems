# THM-M-1486 intake validation

## Scope

This record validates only the `planned` dossier, scope map, source-statement crosswalk, open task
DAG, inspected source/formal leads, and discovery-only pinned Lean API probe. It does not validate
an exact mathematical statement, a neural-network definition, a universal-approximation or
expressiveness theorem, a training or generalization theorem, a proof, an accepted receipt, audit
completion, or theorem completion.

The worker tree was nonrelease-dirty throughout: the canonical `.lake` link was already untracked,
and this intake's owned artifacts plus the root self-test packet were new. No dependency content,
authority file, generated checklist, execution-DAG state, or other target path was modified.

## Environment

- Repository base: `e552e0758e29de307cf357a703e6ecd16e40fb69`
- Base tree: `492b45021fb6ce4973452d8173d32fe2c212a877`
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`
- Lake: `5.0.0-src+98dc76e`
- mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- mathlib tree: `bdc39a3123201dae413a9d9be56ec242c19e5c2b`
- Platform: Linux `7.0.0-27-generic`, `x86_64`
- Timezone/date: Asia/Shanghai, 2026-07-13

The existing canonical pinned `.lake` artifacts were read only. No `lake update`, `lake build`,
dependency clone/fetch, or other dependency mutation was run.

## Source observations

The following bounded observations are discovery evidence, not vendored release inputs or H0/M0
evidence:

| Observation | SHA-256 | Boundary |
|---|---|---|
| official Deep Learning book index | `913a461983b8872994a9d2512f2d72dd31aa232940982acd79fe92e9647f83d2` | field-definition lead only |
| official book Chapter 6 HTML | `14d53b99e734892233699b5814588592cb38a24c5437e811a012b135ba510ad2` | describes feedforward models and depth; no catalog-selected theorem |
| Crossref metadata for Nature DOI `10.1038/nature14539` | `89c9ba306c71474de94505acbf9e940d9e8cdb658d3c3e13d507741c879d5235` | broad review metadata only |
| official PMLR Cohen-Sharir-Shashua page | `525c24103741308e96c7fe4a3084697a6f23b3d1b5d9a3144bf49e10e3abbb1a` | bibliographic and abstract lead |
| official PMLR paper PDF | `f72bd2a1b3e10dde0da24a71b4a8d59dbeeb96e92af63d3c481a2a9fe84c4b58` | exact source theorem inspected, but not selected as this root |
| official AFP entry page | `b013d3436009a087dbad4630b035e839efad045f17b80c25f29e4c02acee08a1` | external Isabelle formal-candidate lead |
| dated AFP 2026-02-06 release archive | `018557d0041584239d603a7eb3700d07ed7eb2a2ca48f694820072003ebf430d` | immutable archive inspected, not Isabelle-built locally |
| AFP terminal source module | `3b88662fc0e3d07c0c0e16af7e74aa0aa3239826aee7dae98eea93a36e8bb0ab` | contains `fundamental_theorem_network_capacity_v3`; target mismatch remains |

Repeated downloads in the same worker matched the PMLR PDF, Crossref response, AFP entry page, and dated
AFP release archive byte for byte. A duplicate request for the 4.3 MB book chapter timed out after
receiving a partial response; this known observation failure does not affect the catalog ambiguity
or the locally self-tested intake.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1486` | 0 | rank 1163, planned, L0/rework_required, no legacy slot, theorem_complete false |
| `git status --short --untracked-files=all` at preflight | 0 | only the pre-existing untracked canonical `.lake` link existed before this intake; preserved |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 10861,10866 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| bounded official-source observations, hashes, duplicate downloads, and pinpoint inspection | 0 | historical discovery observation only; the original exact retrieval argv/URLs were not preserved, so the hashes are not claimed as replayable validation receipts; field definitions, Cohen Theorem 1/Corollary 2, and AFP `fundamental_theorem_network_capacity_v3` remain uncredited leads |
| bounded deep-learning/neural-network search over pinned mathlib and repo-local Lean | 0 | historical discovery observation only; the original exact search argv was not preserved, so the output hash is not a replayable receipt; no global absence or anchor-audit claim follows |
| `git -C` pinned mathlib `rev-parse HEAD 'HEAD^{tree}'` and `status --short` | 0 | pinned revision/tree recorded above; package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-1486/IntakeProbe.lean` | 0 | seven adjacent pinned APIs elaborated; three axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem introduced |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-1486-pycache python3 -m py_compile Stage1_Instances/THM-M-1486/check_intake.py` | 0 | scoped validator parses without writing cache files under the owned path |
| `python3 -B Stage1_Instances/THM-M-1486/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/item identity, null target, H5/M4/R4 boundary, source/pin hashes, receipt/packet agreement, exact inventory, and six open tasks agree |
| prohibited-construct `rg` over `IntakeProbe.lean` | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check` plus per-new-file no-index whitespace checks | 0 | no whitespace diagnostics |

The final structural and whitespace results are recorded after receipt and worker-packet creation.
The scoped checker executes the Lean recipe and verifies its exact combined-output hash, but it does
not enforce operating-system network isolation; this remains nonhermetic worker evidence and the
recipe's denied-network policy must be enforced independently before acceptance.
The Lean probe's exact combined-output SHA-256 is
`ddffe5aa8b59fc112c713e5e44ddd3f3c435043c4941bc4d61e8918a4c597ded`.

## Known failures and boundary

Master acceptance is pending. The catalog label still lacks a selected exact proposition. The AFP
candidate is an exact Isabelle result but remains propositionally unselected, non-Lean, outside the
dependency closure, and not locally replayed. Source admission, independent source/deep-learning
review, formal target and mutation certificate, exhaustive Lean anchor audit, obligation registry,
typed graphs, proof, composition, trust closure, readable reconstruction, hermetic replay,
deterministic bundle, and independent verification remain open.

Verdict: `no_state_change`. This self-tested worker proposal may be handed off as `[_]`; it remains
unfinished and unaccepted. `audit_complete=false` and `theorem_complete=false`.
