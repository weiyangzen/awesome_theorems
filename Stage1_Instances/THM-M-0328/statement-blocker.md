# Statement gate blocker

Item: `S56-M-0328-STATEMENT`

Base revision: `b47b40ff4929fab3be62b6ae17bcd97a4f3e4f66`

## Verdict

The exact Lean 4 target cannot truthfully be frozen from the repository inputs. The intake identifies
only the broad claim that a nuclear factor makes completed projective and injective topological
tensor products agree, possibly together with a dual representation. It explicitly leaves open the
primary-source theorem/page, scalar field, separation and completeness assumptions, choice of
completion, dual topology, and whether the conclusion is equality of topologies, a homeomorphism,
or a topological vector-space equivalence. Those choices change the mathematical proposition; none
may be invented at the statement gate.

The only source record is the short phrase "topological tensor products of nuclear spaces" in
`Docs/researches/math_theorems.md`. The intake lists Grothendieck's 1955 memoir and Treves as
uninspected candidates, not exact anchors. Accordingly the canonical claim remains `M4`, and no
expression fingerprint, alternate-form transport, or semantic mutation suite can honestly be
issued.

## Lean boundary

`StatementInfrastructure.lean` uses the narrowest directly relevant pinned import and checks
`PiTensorProduct.injectiveSeminorm_le_projectiveSeminorm`. This is a comparison on a finite
algebraic tensor product of seminormed spaces. It does not define nuclear locally convex spaces,
completed locally convex tensor products, or the terminal Grothendieck duality claim and receives
no statement or proof credit.

A repository-local search of pinned mathlib found no occurrences of "nuclear space", "nuclear
locally convex", "completed projective", "completed injective", or "topological tensor product".
The Grothendieck hits concern unrelated results such as Ax-Grothendieck, Grothendieck topologies,
and Grothendieck groups.

## Commands and results

Commands ran in this worker clone on 2026-07-12. Lean commands ran from `Formalizations/Lean`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0328` | 0 | rank 213; planned; L0/rework-required; theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0328/StatementInfrastructure.lean` | 0 | finite algebraic seminorm comparison elaborated with no warnings or errors |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'nuclear space\|nuclear locally convex\|completed (projective\|injective)\|topological tensor product' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matches |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-0328/StatementInfrastructure.lean` | 1 | expected untracked-file difference status; empty output, hence no whitespace errors |
| `git diff --no-index --check /dev/null Stage1_Instances/THM-M-0328/statement-blocker.md` | 1 | expected untracked-file difference status; empty output, hence no whitespace errors |
| `rg -n '\bsorry\b|\baxiom\b|placeholder' Stage1_Instances/THM-M-0328/StatementInfrastructure.lean` | 1 | no prohibited proof construct found |

## Unblock condition

Inspect a primary source and select an exact theorem with edition, theorem/page, assumptions, and
errata. Then either identify pinned concrete Lean definitions for every object in that theorem or
first implement those definitions under a separately accepted obligation. Only then can this node
freeze binders, elaborate the exact proposition, fingerprint it, and run semantic mutations.

This node is blocked and is not self-tested completion. No `.stage1-worker-selftest.json` is
created, and no downstream node or theorem-completion claim is made.
