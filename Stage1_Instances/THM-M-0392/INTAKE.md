# THM-M-0392 intake

## Scope map

The authoritative source record says only “integer solutions of `y²=x³+k`”. It does not determine whether `k` is fixed or universally quantified, nor whether the result requested is finiteness or an effective enumeration. Therefore intake freezes the wording and its ambiguity, not an invented exact theorem.

The legacy Lean module suggests the candidate root
`∀ k : Int, k ≠ 0 → Set.Finite {(x,y) | y^2 = x^3 + k}`. The `k ≠ 0` boundary is mathematically material: at `k = 0`, `(t²,t³)` is a solution for every integer `t`. This candidate receives no machine or source-fidelity credit before the statement phase.

## Source-statement crosswalk

| Source field | Source value | Candidate formal component | Intake status |
|---|---|---|---|
| name | 莫德尔方程 | Mordell equation | identified |
| content | `y²=x³+k的整数解` | integer equation `y^2=x^3+k` | literal equation identified |
| proposer/source | Louis Mordell | historical attribution | unverified; not H credit |
| year | 1913 | historical date | unverified; not H credit |
| proposition type | open/conjecture/not fully closed | no exact formal consequence | metadata only |
| machine status | pending | legacy `StatementShape` candidate | not accepted |

No primary mathematical source, edition, page, or theorem number is supplied by the authoritative record. Locating and checking one belongs to anchor audit; consequently human debt remains `H5`.

## Status boundary

This planned dossier establishes membership, provenance, ambiguity, candidate scope, and the open task order only. It does not claim an exact statement, Lean elaboration, proof, source fidelity, audit completion, or theorem completion.

## Intake validation

Run from repository root:

```text
python3 Docs/tools/check_stage1_standard.py
python3 scripts/stage1_target.py check
python3 scripts/stage1_target.py show THM-M-0392
python3 -m json.tool Stage1_Instances/THM-M-0392/instance.json
python3 -m json.tool Stage1_Instances/THM-M-0392/tasks.json
git diff --check -- Stage1_Instances/THM-M-0392
```

All commands exited 0 on 2026-07-12. The standard check reported 1546 uniform-L0 targets; target check reported 1546 unique targets and ranks 1..1546; `show` reported execution rank 2, planned lifecycle, and `theorem_complete: false`. JSON parsing and whitespace validation produced no output.
