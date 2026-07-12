# THM-M-1247 proof-phase blocker

Item: `S56-M-1247-PROOF`  
Theorem: `THM-M-1247`  
Base revision: `11e7ace1a3eba66e560393864e23d09e8aaf1273`  
Run date: `2026-07-12`

## Verdict

The proof phase is blocked and is not self-tested as complete. No proof receipt
or worker self-test manifest was emitted.

The frozen root is the sharp multidimensional Rellich inequality in
`Statement.lean`. The accepted inputs expose only a conditional transport from
`ExpandedTarget` to that root. They contain no proof body for the substantive
premise. The pinned dependency search recorded by the preceding anchor audit
found no Rellich or Hardy-Rellich theorem. A fresh source search of the pinned
Lake packages likewise found no matching Lean declaration.

The first failed proof gate is `M1247-L-IBP`: there is no kernel-checked,
weighted multidimensional integration-by-parts identity for the singular
weight in the current closure. `M1247-L-HARDY` is independently open: there is
no sharp weighted first-derivative Hardy estimate with the required constant.
Consequently `M1247-L-CORE` and `M1247-ROOT` cannot be constructed without
inventing an unproved premise. The local Laplacian and Schwartz-space
integration-by-parts declarations found in mathlib do not state either missing
weighted estimate and receive no proof credit.

## Commands and results

All commands ran in this worker clone and reused the existing pinned Lake
artifacts. No update, build, clone, fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1247` | 0 | rank 427; lifecycle `planned`; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1247/check_statement.py` | 0 | exact statement fingerprint and mutation checks passed |
| `python3 Stage1_Instances/THM-M-1247/check_anchor_audit.py` | 0 | pinned substrate audit passed; terminal result remains open |
| `python3 Stage1_Instances/THM-M-1247/check_obligation_tree.py` | 0 | 13 obligations and 34 typed edges; root open at M3 |
| `rg -n -i 'rellich\|hardy[-_ ]?rellich' Formalizations/Lean/.lake/packages --glob '*.lean'` | 1 | no matching Lean source in the pinned package closure |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1247/Statement.lean` | 0 | the exact canonical target elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1247/ObligationTree.lean` | 1 | expected direct-import failure: local module `Statement` is not on this invocation's Lean path |

The obligation-tree record already documents its successful scoped invocation:
compile `Statement.lean` to a temporary local `Statement.olean`, add the target
directory to `LEAN_PATH`, and elaborate `ObligationTree.lean`. That check proves
only the conditional transport, whose explicit `core : CoreRellichEstimate`
premise remains open.

## Retry condition

Resume proof execution only after either:

1. an immutable Lean 4 declaration closing the exact expanded target is pinned,
   imported, exact-type checked, and provenance audited; or
2. exact typed formal targets are supplied and local proof bodies are completed
   for `M1247-L-IBP` and `M1247-L-HARDY`, followed by checked composition through
   `M1247-L-CORE` and the existing root transport.

Until then the machine classification remains `M3`; validation, release,
master acceptance, and theorem completion remain open.
