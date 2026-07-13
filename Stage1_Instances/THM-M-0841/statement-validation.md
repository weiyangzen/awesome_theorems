# Statement validation

Item: `S56-M-0841-STATEMENT`
Base revision: `a3b18eec39bf04be025b1641cae02f4d44fdf11a`

## Frozen target

`Stage1Instances.THM_M_0841.ErdosStoneTarget` formalizes the unnumbered theorem printed on page
1087 of Erdos and Stone's 1946 paper. For `0 < epsilon < 1` and `r >= 2`, it preserves the source's
explicit `exists n0 > 0, forall n > n0` order and strict edge threshold. Its conclusion selects
some positive natural `k` at least `sqrt(l_(r-1)(n))` and contains
`completeEquipartiteGraph r k` in the graph
complement. Non-induced containment is intentional: it requires every cross-group pair to be a
nonedge of the original graph and makes no claim about within-group pairs.

`iteratedLog` is natural iteration of `Real.log`. `ExpandedSourceTarget` expands only that local
notation, and `erdosStoneTarget_iff_expandedSourceTarget` is the checked `iff`. No fixed-ceil
pruning, page-1088 dense complement transport, modern fixed-forbidden-graph density formula, or
minimum-degree strengthening is credited.

## Commands and results

All commands ran inside this worker clone on 2026-07-13 Asia/Shanghai. Lean used the existing
canonical pinned Lake artifacts read-only. No dependency update, build, clone, or fetch command was
run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0841` | 0 | rank 1398; planned; legacy artifacts unaccepted; theorem incomplete |
| `lake env lean ../../Stage1_Instances/THM-M-0841/Statement.lean` from `Formalizations/Lean` | 0 | exact target, unfolding transport, four expected mutation rejections, five boundaries, axiom report, and explicit expression elaborated |
| `python3 -B ../../Stage1_Instances/THM-M-0841/check_statement.py` from `Formalizations/Lean` | 0 | expression SHA-256 `ed4a8b422615bfafc69ab9f770dc99b77d308d78bca30e67790206426799a733`; environment SHA-256 `ec81286c0a60baa4a23af792af268e7efe87bed50264292a02f5646443bd276d`; all mutations distinct; deleting either import fails; pins agree |
| `python3 -B Stage1_Instances/THM-M-0841/check_statement_artifacts.py --worker-packet .stage1-worker-selftest.json` | 0 | fresh elaboration, statement metadata, receipt, authority, provisional state, and worker packet agree |
| Lean/Lake version and pinned mathlib revision/tree queries | 0 | Lean 4.29.0 commit `98dc76e3...`; Lake 5.0.0; mathlib `8a178386...`, tree `bdc39a31...`; mathlib tree clean |
| JSON, Python syntax, prohibited-construct, newline, and whitespace checks | 0 overall | structured artifacts parse; checker compiles; no prohibited Lean declaration or whitespace error |

## Mutation and boundary policy

Lean rejects definitional equality with mutations that remove `epsilon < 1`, change `epsilon` from
`Real` to `Rat`, choose one threshold before `epsilon` and `r`, or admit the source-excluded case
`r = 1`. The checker also compares their fully explicit expression fingerprints. Kernel-checked
boundary declarations establish the zero/one iterated-log conventions and exclusion of `r = 1`,
`epsilon = 0`, and `epsilon = 1`. These are identity checks, not proofs of Erdos-Stone.

The historical intake checker binds the earlier nine-file intake snapshot. Statement artifacts
necessarily supersede that inventory, so it is not used as statement evidence. The intake receipt
remains historical evidence for its own snapshot; its `current_unsuperseded` label and owned-file
hashes describe that old snapshot and are not claims about the current dossier.

This is statement-only evidence pending dependency-ordered master acceptance. It provides no
formal-anchor or proof credit, H0/R0, obligation tree, audit completion, release validation, or
theorem completion.

The provisional receipt is intentionally not content-addressed release evidence. Master acceptance
must recapture immutable dirty inputs, owned-artifact and validator hashes, and complete logs.
