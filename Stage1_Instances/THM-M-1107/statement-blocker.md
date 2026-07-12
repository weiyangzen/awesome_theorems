# Exact-statement gate: blocked

Item: `S56-M-1107-STATEMENT`  
Theorem: `THM-M-1107`  
Base revision: `3f82136c3696549591ee6c2bcbea856459213d36`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the accepted material in this clone.
The repository discovery record supplies only `随机矩阵最大特征值的分布` (the distribution of the
largest eigenvalue of a random matrix). That wording does not choose a matrix ensemble, scalar
field, finite-size law, normalization, edge, scaling, limiting distribution, or mode of
convergence.

The intake narrows this provisionally to beta-2 Tracy-Widom fluctuations for normalized GUE and
names Tracy and Widom's 1994 *Level-Spacing Distributions and the Airy Kernel* as a candidate
primary source. The same intake explicitly leaves its theorem/equation/page locators,
normalization, hypotheses, and errata unaudited. More importantly, its crosswalk requires a
separate primary finite-`N` GUE edge-asymptotic source if the 1994 paper presents the limit through
correlation or gap probabilities rather than as the exact normalized-largest-eigenvalue theorem.
No such exact source statement is present in the dossier.

The unresolved choices change the proposition:

- the GUE density or entrywise law, underlying reference measure, and trace convention;
- the matrix-size binder, exclusion of size zero, and Hermitian eigenvalue ordering;
- the limiting edge and every constant in the `N^(2/3)` centering and scaling;
- convergence of CDF values versus weak convergence of probability measures;
- the concrete beta-2 Tracy-Widom measure or CDF;
- the Airy function/kernel, operator on `L2(s, infinity)`, trace-class condition, and Fredholm
  determinant convention;
- whether the selected primary theorem proves the finite-`N` edge limit, the determinant identity,
  or only a result requiring a further checked bridge.

Selecting familiar conventions would broaden the sparse discovery phrase and manufacture a nearby
theorem. Quantifying an arbitrary distribution, determinant function, or GUE law together with
hypotheses asserting convergence and the determinant identity would package the desired conclusion
as an assumption. Both approaches are forbidden by this item's scope and rev-5.6.

## Lean boundary

The pinned environment is available. Pinned mathlib contains real fragments relevant to a future
encoding: `Matrix.IsHermitian`, Hermitian `Matrix.IsHermitian.eigenvalues`,
`ProbabilityTheory.cdf`, and `TendstoInDistribution`. Scoped source searches found no declaration
for Tracy-Widom, the Gaussian unitary ensemble, the Airy function or kernel, trace-class operators,
or a Fredholm determinant. Matches for "Fredholm" are the Fredholm alternative for compact
operators; they do not provide the determinant required by this target.

This is feasibility evidence, not the later anchor audit. Since the proposition itself is not
source-identified, an infrastructure probe would not elaborate the exact target and could not pass
this statement node. There is therefore no honest `lake env lean <canonical target>` command,
expression hash, minimal-import claim, checked transport, or meaningful statement mutation suite.
Machine debt remains `M4`.

## Validation record

Commands ran from this worker clone on 2026-07-12 (Asia/Shanghai). The linked canonical `.lake`
artifacts were read only; no update, build, clone, fetch, or dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1107` | 0 | rank 547, planned, legacy artifacts unaccepted, theorem incomplete |
| `git rev-parse HEAD` | 0 | base `3f82136c3696549591ee6c2bcbea856459213d36` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes recorded in `statement-blocker.json` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| repository `rg` search for the theorem ID, names, and source title | 0 | only sparse catalogue metadata, neighboring dossiers, and this intake; no exact proposition or Lean candidate |
| pinned-mathlib `rg` search for Tracy-Widom, GUE, Airy kernel/function, Fredholm determinant, and largest eigenvalue | 1 for exact terms | no target-specific declaration; separate API checks found only the partial surfaces listed above |
| `python3 -m json.tool Stage1_Instances/THM-M-1107/statement-blocker.json` | 0 | JSON syntax passed |
| `git diff --check -- Stage1_Instances/THM-M-1107` | 0 | no whitespace errors |

## Retry condition

Preserve immutable primary sources for both the finite-size GUE edge limit and Airy-kernel
identification. Record hashes and theorem/equation/page locators; audit every normalization,
premise, conclusion, bridge, and erratum; and obtain independent source approval. Then implement
the missing analytic substrate without assuming the conclusion, freeze and kernel-elaborate the
source-exact proposition with minimal pinned imports, serialize its expression, check transports,
and run all four required mutation classes.

This is the first failed gate. It does not complete the statement node or any later node. The phase
is not genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
