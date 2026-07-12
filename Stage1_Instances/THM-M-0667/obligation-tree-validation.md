# THM-M-0667 obligation-tree validation

Item: `S56-M-0667-OBLIGATION_TREE`. Base revision:
`19b021541c1d729b760216e067b3e2ac951aaead`.

## Frozen result

Registry version 1 contains 16 unique semantic obligations with denominator SHA-256
`38c974225c7543cc8789f00f991a4fb1a46361c0763dfb03877ce451996409af`. Seven separate typed graph
families contain 36 directed edges, including reciprocal `proof_requires` and `composes` edges.
All machine-required obligations are reachable from the root through proof or refinement edges.

The scoped Lean validator creates a temporary `Statement.olean`, adds only that temporary directory
to the Lake-derived `LEAN_PATH`, and elaborates `ObligationTree.lean` with the pinned Lean binary.
The temporary output is removed automatically; no dependency or repository build artifact is
written. `root_of_domination` assumes `DominationPackage`, so this is composition evidence only.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0667/build_obligation_artifacts.py` | 0 | deterministically wrote 16 obligations and both graph artifacts; denominator hash above |
| `python3 Stage1_Instances/THM-M-0667/check_obligation_tree.py` | 0 | hashes, schemas, denominators, reciprocal edges, DAG reachability, cut set, and scoped Lean elaboration passed; 36 edges |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered rework-required targets passed |
| `python3 scripts/stage1_target.py show THM-M-0667` | 0 | rank 711, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0667/obligation-registry.json` | 0 | registry parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-0667/typed-graphs.json` | 0 | graph bundle parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-0667/obligation-tree-receipt.json` | 0 | worker receipt parsed |
| `git diff --check -- Stage1_Instances/THM-M-0667 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The Lean output named `root_of_domination` and contained no `sorryAx`. The architecture deliberately
does not invoke the imported root theorem and contains no `sorry`, `admit`, axiom declaration,
unsafe definition, or substituted target.

## Status boundary

The phase is self-tested pending master acceptance. Root debt remains `M3`; the cut set is
`M0667-N-DOMINATION`, `M0667-X-FOUNDATION`, and `M0667-X-SOURCE`. Proof integration, complete trust
and source review, validation, release, and theorem completion remain open.
