# THM-M-0651 proof-phase attempt

Item: `S56-M-0651-PROOF`  
Date: `2026-07-12` (`Asia/Shanghai`)  
Base revision: `f489f107e7abbb49376144c22d5e41ece02d20ea`

## Verdict

`blocked`: the exact simultaneous countable omitting-types target has no eligible proof body in the
repository or pinned dependency closure. The frozen root remains `M4`; its machine cut set is
`M0651-L-ENUM`, `M0651-L-DENSE`, `M0651-L-HENKIN`, and `M0651-L-OMIT`. The first unavailable
mathematical body is the dense nonprincipality extension lemma `M0651-L-DENSE`.

`ObligationTree.lean` contains the real proof body `root_compose`, but it proves the root only after
`ConstructionInterface` and `AvoidanceInterface` are passed as premises. It discharges neither.
Moreover, the frozen `Candidate` structure contains only a countable model, whereas
`AvoidanceInterface` asserts that every such candidate omits every specified type. Nonprincipality
does not make arbitrary countable models omit the type. A viable architecture must carry avoidance
invariants in the constructed candidate or combine construction and omission in one theorem.

The prerequisite anchor audit found no exact pinned declaration. Its external
`FirstOrder.Language.omitting_types` candidate uses separate `Lomega1omega` syntax and semantics,
unary types, different hypotheses, Lean 4.32.0-rc1, and another mathlib revision. Importing it
without checked transports would broaden or substitute the theorem. Assuming the open local
interfaces would be a placeholder. No `Proof.lean` or receipt is therefore fabricated, and because
the assigned proof phase is incomplete, `.stage1-worker-selftest.json` is deliberately absent.

## Narrow validation evidence

All commands ran in this worker clone and reused the canonical pinned Lake artifacts. No dependency
update, build, clone, fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0651` | 0 | rank 697; planned; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0651/check_obligation_tree.py` | 0 | 11 obligations and 21 typed edges passed; root open at M4 with the four-leaf cut set |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0651/Statement.lean` | 0 | exact canonical target, omission transport, and mutation probes elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0651/ObligationTree.lean` | 0 | conditional composition elaborated; `root_compose` reports only `propext` and `Quot.sound` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| scoped `rg` for omitting types, partial types, and nonprincipality | 0 | hits were confined to this dossier; pinned `Mathlib/ModelTheory` supplied no proof candidate |
| `sha256sum` on statement, conditional composition, registry, and statement record | 0 | `39b09536...d38ea`; `2317873f...c2df`; `9a87b090...142f`; `cf4e441e...3c5b` |
| `git diff --check -- Stage1_Instances/THM-M-0651` | 0 | no whitespace errors before these two blocker artifacts were added |

## Reopen condition

Resume after refining the construction interface to retain avoidance invariants and implementing
the four open proof packages without placeholders, or after locating an immutable, compatible exact
Lean 4 proof with checked transports into the frozen target.
