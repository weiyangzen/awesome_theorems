# THM-M-1526 obligation-tree validation

Item: `S56-M-1526-OBLIGATION_TREE`. Base revision:
`6afdcb2c5487434cce7acf7aeb8ed471faf92666`.

## Frozen result

Registry version 1 contains 17 unique semantic obligations and has denominator SHA-256
`95dd65417c8ea80862fb89be73705db1995ada78e80cd2b96f039aa471fcae6a`. The seven separate graph
families contain 34 directed typed edges, including reciprocal `proof_requires`/`composes` pairs.
All machine-required nodes are reachable from the root through proof or refinement edges. Every
node carries the rev-5.6 schema and a substantive ledger no larger than 100 steps or an explicit
`split-required` marker.

The Lean validator creates a temporary `Statement.olean` outside the repository using the pinned
Lean binary and Lake-derived `LEAN_PATH`, then elaborates `ObligationTree.lean` against it. The
temporary directory is removed automatically; no `.lake` dependency or repository build artifact
is changed. `root_of_factorization` conditionally composes the exact factorization identity into
both conjuncts of the frozen root, and its axiom print contains no `sorryAx`.

## Commands and results

Commands ran on 2026-07-12 inside this worker clone.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1526/build_obligation_artifacts.py` | 0 | Deterministically wrote 17 obligations and both JSON artifacts; denominator hash above. |
| `python3 Stage1_Instances/THM-M-1526/check_obligation_tree.py` | 0 | Registry/schema/eligibility/hash, reciprocal edges, graph reachability and acyclicity, cut set, and scoped Lean composition passed; 34 typed edges. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered rework-required targets passed. |
| `python3 scripts/stage1_target.py show THM-M-1526` | 0 | Rank 194, planned, L0/rework-required, theorem incomplete. |
| `python3 -m json.tool Stage1_Instances/THM-M-1526/obligation-registry.json` | 0 | Frozen registry parsed as JSON. |
| `python3 -m json.tool Stage1_Instances/THM-M-1526/typed-graphs.json` | 0 | Typed graph bundle parsed as JSON. |
| `python3 Stage1_Instances/THM-M-1526/check_statement.py` | 0 | Exact expression and statement-file hashes revalidated. |
| `python3 Stage1_Instances/THM-M-1526/check_anchor_audit.py` | 0 | Target binding, clean pinned mathlib revision, twelve probes, and external-support classification revalidated. |
| `rg -n '\b(sorry\|axiom)\b' Stage1_Instances/THM-M-1526/ObligationTree.lean` | 1 | Expected no-match exit; no prohibited proof token occurs in the composition module. |
| `git diff --check -- Stage1_Instances/THM-M-1526 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

An initial direct `lake env lean ../../Stage1_Instances/THM-M-1526/ObligationTree.lean` invocation
exited 1 because sibling import `Statement` requires a compiled `.olean` on `LEAN_PATH`; it did not
create a repository artifact. The final validator explicitly compiles that prerequisite into an
ephemeral directory and passed.

## Status boundary

This self-tests only the obligation-tree phase. The checked composition assumes the complete
factorization package. The remaining root cut set is `M1526-N-PRODUCT` and
`M1526-L-SLASH-SQUARE`; root debt stays `M3`. There is no factorization proof, accepted master
receipt, H0 source claim, validation/release evidence, or theorem-completion claim.
