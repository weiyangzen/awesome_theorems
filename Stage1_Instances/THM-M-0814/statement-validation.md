# THM-M-0814 statement validation

Item: `S56-M-0814-STATEMENT`

Base revision: `3ef3a6bf4f2f9b86930beb27693f7429fea3e63a`

Base tree: `c9eba4c65f6e228f9cefc8bdf62136b7fb69426a`

## Frozen target

`Stage1Instances.THM_M_0814.MaxFlowMinCutTarget` formalizes Section 1, Theorem 1 of Ford
and Fulkerson's 1956 paper in the paper's undirected path-decomposed form. A chain has distinct
vertices and arcs and connects the distinguished source to the sink. A flow is a finitely supported
collection of nonnegative real chain weights. Its load on every graph arc is bounded by that arc's
strictly positive capacity. A disconnecting set contains graph arcs and meets every such chain.
The conclusion witnesses a maximum feasible flow and minimum disconnecting set and equates their
values.

The formal coefficient domain is `NNReal`, encoding the source's nonnegative chain weights and
positive capacities without a separate nonnegativity premise. The paper says only "number," so the
historical codomain mapping remains an H1 review boundary. `Graph` permits loop arcs; they are inert
because an injective-vertex chain cannot use them, but the source's loop convention also remains
part of the H1 transport review. No directed conservation-flow or partition-cut encoding receives
credit.

The direct imports are exactly `Mathlib.Algebra.BigOperators.Finsupp.Basic`,
`Mathlib.Combinatorics.Graph.Basic`, and `Mathlib.Data.NNReal.Defs`. Deleting any one makes the
module fail. No proof-bearing max-flow module or target theorem is imported. The checked
`maxFlowMinCutTarget_iff_expanded` witness only respells the same source-shaped target.

## Commands and results

All commands ran in this worker clone on 2026-07-13 (`Asia/Shanghai`). Lean reused the
automation-provided canonical pinned `.lake` artifacts read-only. No update, build, clone, fetch,
or dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, and execution skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0814` | 0 | rank 1373; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0814/Statement.lean` | 0 | helper definitions, root, direct respelling, four expected equality rejections, axiom report, and explicit target elaborated |
| `cd Formalizations/Lean && python3 -B ../../Stage1_Instances/THM-M-0814/check_statement.py` | 0 | exact helper-bundle/root fingerprints, four distinct mutations, all three import-deletion failures, and pinned toolchain/mathlib identity passed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0814/IntakeProbe.lean` | 0 | historical six-API substrate probe still elaborates; it is not canonical statement evidence |
| `python3 -B Stage1_Instances/THM-M-0814/check_intake.py` | 1 | historical intake-only checker is superseded: it expects the pre-integration intake state and null-target nine-file inventory, so it is not statement evidence |
| `lake env lean --version`; `lake --version` | 0 | Lean 4.29.0 commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'`; package status | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`, clean package worktree |
| JSON validation, Python syntax checks, prohibited-construct scan, and scoped whitespace checks | 0 overall | structured artifacts and validators parse; no forbidden Lean construct or whitespace diagnostic |

## Mutation and evidence boundary

The four mutations remove only positive capacity, change the capacity domain to natural numbers,
select one network existentially, or exclude networks with no source-to-sink chain. Lean rejects
definitional equality with the canonical target, and the checker independently compares fully
explicit serializations. These are identity tests, not claims that every changed proposition is
false.

The checked direct respelling reports only `propext`, `Classical.choice`, and `Quot.sound`. No
custom axiom, `sorryAx`, unsafe declaration, oracle, or target proof is present. The exact source
acceptance, formal-anchor and terminal-body audit, obligation registry, proof, composition,
readable reconstruction, hermetic replay, independent verification, release, and master acceptance
remain open. This worker proposal supplies no H0, M0, R0, audit completion, theorem completion, or
release credit.
