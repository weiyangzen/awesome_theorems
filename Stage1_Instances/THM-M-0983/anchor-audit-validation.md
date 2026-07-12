# Anchor-audit validation record

Item: `S56-M-0983-ANCHOR_AUDIT`  
Base revision: `46f3323eb334a00da17b0f37524a13c107cabf27`

## Result

Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the terminal theorem
`ProbabilityTheory.strong_law_ae_real` in `Mathlib.Probability.StrongLaw`. Its conclusion is the
frozen empirical average converging almost surely to the reference expectation. The only bridges
needed are `iIndepFun.indepFun`, which projects family independence to the pairwise hypothesis, and
the frozen equation `mu[X 0] = p`. The `0/1` hypothesis is not needed because mathlib proves the
strictly more general integrable real IID result. `AnchorAudit.lean` independently copies the frozen
proposition and kernel-checks this complete route; the validator checks its five material clauses
against `Statement.lean` before elaboration.

The bounded external search found `facebookresearch/atlas-lean@34ffed3...`, whose real SLLN wrapper
delegates to the same mathlib theorem, and `lean-hansen-econometrics@b05e2b8...`, whose WLLN is only
convergence in measure. Neither merits a new dependency: Atlas adds no independent terminal body,
and Hansen is weaker than the frozen target. Authenticated GitHub code search was unavailable due to
rate limiting, so no global-absence claim is made.

This audit therefore identifies an `M0-L` candidate already inside the immutable Lake closure. It
does not accept the downstream obligation-tree, proof, provenance, trust, or validation nodes and
does not claim theorem completion.

## Commands and results

Commands ran on 2026-07-12. No Lake update, build, dependency clone, or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0983/AnchorAudit.lean` | 0 | Four pinned declarations and the exact target bridge elaborated; axioms were `propext`, `Classical.choice`, and `Quot.sound`, with no `sorryAx` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0983/Statement.lean` | 0 | Frozen statement and checked expansion re-elaborated |
| `python3 Stage1_Instances/THM-M-0983/check_anchor_audit.py` | 0 | Target clauses, probes, status boundary, manifest pin, and installed mathlib HEAD agreed |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `curl ... Sourcegraph ...` | 0 | 38 bounded matches in four repositories; response SHA-256 `f3d5423aabdc4bdbb409706f10820a15b45429b0cb63fb0cce891222f6e98521` |
| `curl ... atlas-lean@34ffed3.../StrongLaw.lean` | 0 | Immutable source inspected; SHA-256 `f9f12468552f9ca08c842860744c6173e15790a0459fc8965e98e3457c8e19e2` |
| `curl ... lean-hansen-econometrics@b05e2b8.../AsymptoticUtils.lean` | 0 | Immutable weaker WLLN source inspected; SHA-256 `5c0ebb54087d8b4bffafd7d252b7f666540c5d117e38f0abfc49ce9000887a93` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0983` | 0 | rank 263, planned, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0983` | 0 | no whitespace errors |

## Status boundary

The anchor node is self-tested pending master acceptance. The exact theorem remains publicly
incomplete until every downstream rev-5.6 gate, including independent kernel evidence, is accepted.
