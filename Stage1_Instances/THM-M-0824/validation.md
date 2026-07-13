# THM-M-0824 intake validation

## Scope

This record validates only the `planned` dossier, scope map, source-statement crosswalk, open task
DAG, bibliographic source-lead metadata, and discovery-only pinned Lean API probe. It does not
validate an exact mathematical statement, an implementation of Prim's algorithm, termination,
spanning-tree validity, minimum-weight optimality, complexity, a proof, an accepted receipt, audit
completion, or theorem completion.

The worker tree was nonrelease-dirty throughout: the canonical `.lake` link was already untracked,
and this intake's owned artifacts plus the root self-test packet were new. No dependency content,
authority file, generated checklist, execution-DAG state, or other target path was modified. The
automation-provided canonical `.lake` link was used read-only; no update, build, clone, fetch, or
other dependency mutation was performed.

## Environment

- Repository base: `902d9ce008e88a35a2307c85355560a230cc33c2`
- Base tree: `dfc20d8141f18f6b09a03e818acfff408e836714`
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`
- Lake: `5.0.0-src+98dc76e`
- mathlib: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- mathlib tree: `bdc39a3123201dae413a9d9be56ec242c19e5c2b`
- Platform: Linux `7.0.0-27-generic`, `x86_64`
- Timezone/date: Asia/Shanghai, 2026-07-13

Crossref and Unpaywall metadata for DOI `10.1002/j.1538-7305.1957.tb01515.x` were observed through
bounded HTTP requests. Their response SHA-256 values were, respectively,
`1f28b63b15a3a31a716dc13a2db0e0fc5431a163136b5134871e5f9632d79d05` and
`12f7aae5095796d655d9406b93427f5a51a6645339cbfd752dc030bc359b9b34`. The former identifies
Prim's 1957 paper and the latter reports closed access with no open location. No external source
was vendored. These are mutable, nonrelease discovery observations.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0824` | 0 | rank 1382, planned, L0/rework_required, no legacy slot, theorem_complete false |
| `git status --short --untracked-files=all` at preflight | 0 | only the pre-existing untracked canonical `.lake` link existed before this intake; preserved |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | base revision and tree recorded above |
| `git blame -L 6054,6059 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `git blame -L 170,170 -- Docs/researches/cs_theorems.md` | 0 | related correctness wording originates in the same corpus commit; discovery metadata only |
| bounded Crossref and Unpaywall metadata observations for DOI `10.1002/j.1538-7305.1957.tb01515.x` | 0 | matching R. C. Prim 1957 source lead identified; article reported closed; no primary text credited |
| OpenAlex DOI metadata observation | 22 | HTTP 429; no metadata or source body was received or credited from this endpoint |
| Internet Archive title search | 28 | request timed out; no source body was received or credited |
| bounded exact-topic search over pinned mathlib and repo-local Lean | 1 expected | no named Prim/minimum-spanning-tree correctness declaration matched; bounded search is not an absence proof |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned revision and tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package worktree clean |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0824/IntakeProbe.lean` | 0 | six adjacent pinned APIs elaborated; two axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`; no target theorem introduced; exact output SHA-256 `bc531cbb8d28a50e48f0465276955cf6b32ee3af75f44c61dc083350e2aa4cba` |
| `python3 -m json.tool` on the three owned JSON files and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0824-pycache python3 -m py_compile Stage1_Instances/THM-M-0824/check_intake.py` | 0 | scoped validator parses without writing cache files under the owned path |
| `python3 -B Stage1_Instances/THM-M-0824/check_intake.py --worker-packet .stage1-worker-selftest.json` | 0 | target/item identity, null target, H5/M4/R4 boundary, source and pin hashes, receipt/packet agreement, exact inventory, and six open tasks agree |
| prohibited-construct `rg` over `IntakeProbe.lean` | 1 expected | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check` plus per-new-file no-index whitespace checks | 0 | no whitespace diagnostics |

The final structure and whitespace results were recorded after receipt and worker-packet creation.

## Known failures and boundary

Master acceptance is pending. The catalog label still lacks a selected exact proposition. Primary
source admission, pinpoint statement/proof/correction mapping, independent graph-algorithms review,
formal target and mutation certificate, exhaustive anchor audit, obligation registry, typed graphs,
proof, composition, trust closure, readable reconstruction, hermetic replay, deterministic bundle,
and independent verification remain open.

Verdict: `no_state_change`. This self-tested worker proposal may be handed off as `[_]`; it remains
unfinished and unaccepted. `audit_complete=false` and `theorem_complete=false`.
