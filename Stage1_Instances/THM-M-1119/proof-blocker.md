# THM-M-1119 proof-phase blocker

Item: `S56-M-1119-PROOF`  
Base revision: `54912addae847c8bb166d0ef6a8ec7b0abb53004`  
Attempt date: 2026-07-12 (Asia/Shanghai)

## Verdict

The proof phase is blocked and is not self-tested as complete. No proof body was added, no frozen
obligation was marked closed, and no worker self-test manifest was written.

The exact root is `Stage1Instances.THM_M_1119.KestenTarget`: the critical parameter for
independent bond percolation on the nearest-neighbor square lattice is `1/2`, with the critical
parameter defined from positive probability that the origin has an unbounded open cluster. The
existing `ObligationTree.lean` proves only conditional composition by antisymmetry. Its two
arguments are the still-open inequalities
`(1 / 2 : NNReal) <= criticalProbability` and
`criticalProbability <= (1 / 2 : NNReal)`; it does not construct either argument.

The first unresolved mathematical cut is the frozen percolation development:

- `M1119-N-MONOTONE` and `M1119-C-RECTANGLES`: monotone coupling, the infimum reduction, finite
  crossing events, pivotal bonds, dual circuits, and their measurability;
- `M1119-L-DUALITY` and `M1119-L-RSW`: planar crossing duality, the self-dual identity at `1/2`,
  and uniform Russo-Seymour-Welsh estimates;
- `M1119-L-RUSSO` and `M1119-L-SHARP`: Russo's derivative formula and the finite-size sharp
  threshold estimates;
- `M1119-T-SUBCRITICAL` and `M1119-T-SUPERCRITICAL`: the two exact threshold inequalities consumed
  by the checked root composition.

Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies Bernoulli product
measures, graph reachability, and order infima, but the accepted anchor inventory found no exact
Kesten theorem. A fresh scoped source search likewise found no percolation, RSW, Russo, pivotal,
or sharp-threshold implementation in pinned mathlib. The only exact target occurrences are this
dossier's statement and conditional architecture. Consequently there is no eligible local or
pinned terminal body to import or wrap.

Implementing Kesten's planar-percolation proof and its missing probability infrastructure from
scratch is not a truthful bounded proof-phase change. Replacing any branch with an assumption,
`sorry`, an axiom, or a theorem about a different lattice, site model, or critical endpoint would
violate the frozen target and registry.

## Validation evidence

All commands ran in the worker clone. The existing canonical `.lake` symlink was reused; no
update, build, clone, fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique ordered targets with ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-1119` | 0 | Confirmed rank 559, `planned`, `L0 / rework_required`, and `theorem_complete: false`. |
| `rg -n -i 'KestenTarget\|criticalProbability\|bond percolation\|square.?lattice.*percolation\|percolation.*square.?lattice\|critical probability' --glob '*.lean' Stage1_Instances Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | Exact-name and subject matches occur only in this dossier's `Statement.lean` and `ObligationTree.lean`; no terminal proof declaration was found. |
| `rg -n -i 'Russo\|Russo.Seymour\|sharp threshold\|pivotal\|percolation\|RSW' --glob '*.lean' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | The only textual hits are unrelated identifiers such as `isMVarSwap` and pivotal monoidal categories; no percolation infrastructure was found. |
| temporary isolated copies, then `cd Formalizations/Lean && lake env lean -R "$TMP" -o "$TMP/Statement.olean" "$TMP/Statement.lean"` and `LEAN_PATH="$TMP:$(lake env printenv LEAN_PATH)" lake env lean -R "$TMP" "$TMP/ObligationTree.lean"` | 0 | The exact statement and conditional two-bound composition elaborated. `#print axioms` reported `[propext, Classical.choice, Quot.sound]`; neither threshold bound was inhabited. Temporary files were removed. |
| `python3 Stage1_Instances/THM-M-1119/check_obligation_tree.py` | 0 | Passed the 15-obligation freeze, five typed graphs, step budgets, and exact conditional composition checks. |
| `rg -n '^\s*(sorry\|admit\|axiom)(\s\|$)' Stage1_Instances/THM-M-1119 --glob '*.lean'` | 1 | No prohibited Lean declaration token occurs; exit 1 means no match. |

The pre-existing untracked `Formalizations/Lean/.lake` symlink makes this nonrelease evidence.

## Reopen condition

Resume this proof item only after placeholder-free Lean bodies are implemented for the frozen
finite-event, planar-duality, RSW, Russo, sharp-threshold, and infinite-volume threshold
obligations, or an immutable compatible dependency providing those exact bodies is pinned and
exact-type checked. Until then the root remains `M4`, `root_closed=false`, and
`theorem_complete=false`; this item cannot truthfully receive `[_]` proof-phase credit.
