# Exact-statement gate: blocked

Item: `S56-M-1562-STATEMENT`  
Theorem: `THM-M-1562`  
Base revision: `be50e4fee4a4eab420300310f355cd6b1ed3336a`

## Decision

The exact Lean 4 target cannot yet be truthfully frozen or elaborated. The repository discovery
record supplies only `随机矩阵与KPZ` (random matrices and KPZ). The intake makes the useful but
explicitly provisional choice of a conjunction: a normalized-GUE largest-eigenvalue limit and a
narrow-wedge KPZ one-point long-time limit, sharing the beta-2 Tracy-Widom law defined by an
Airy-kernel Fredholm determinant. It also records that exact source theorem/equation/page locators,
normalizations, bridges, and errata remain open. Thus it does not provide a reviewed exact
mathematical proposition from which ordered Lean binders can be transcribed.

The unresolved choices change the theorem rather than merely its notation:

- the GUE density or entrywise law, reference measure, trace convention, spectral edge, and every
  centering and `N^(2/3)` scaling constant;
- positive matrix-size indexing, Hermitian eigenvalue ordering, and the precise convergence mode;
- the coefficients and white-noise normalization of KPZ, the narrow-wedge solution concept, height
  sign, deterministic centering, `T^(1/3)` scale, and the relation to the continuum polymer;
- the concrete Airy function, Airy kernel, `L2(s, infinity)` realization, trace-class theorem,
  Fredholm determinant convention, and whether the cited sources supply all required bridges;
- whether both branches are expressed as pointwise CDF convergence or weak convergence of laws,
  and the hypotheses needed to transport between those encodings.

Choosing familiar constants would manufacture a nearby theorem. Quantifying abstract GUE, KPZ,
or Tracy-Widom packages whose fields assume either convergence or the determinant identity would
instead package the conclusion as a hypothesis. Both are prohibited substitutions. The nearby
`THM-M-1107` dossier reaches the same conclusion for the GUE-only branch and is discovery evidence,
not an accepted source transcription or proof credit for this two-branch target.

## Lean boundary

The pinned environment is available at Lean 4.29.0 with mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. A scoped pinned-mathlib search found no declaration for
Tracy-Widom, the Airy kernel, a Fredholm determinant, KPZ, or space-time white noise. Mathlib does
contain general fragments such as probability CDFs, convergence in distribution, and Hermitian
matrix infrastructure, but these fragments neither identify the source-exact claim nor supply its
missing analytic and SPDE objects. The Fredholm-alternative module is not a Fredholm-determinant
API.

Consequently there is no honest canonical target file on which to claim minimal imports,
elaboration, expression serialization, checked alternate transports, or removed-hypothesis,
changed-domain, binder-scope, and boundary mutation tests. The first failed gate is rev-5.6 section
5 exact source-statement identification. Machine debt remains `M4`; the statement node and every
later node remain open.

## Validation record

Commands ran from this worker clone on 2026-07-12 (Asia/Shanghai). The canonical `.lake` artifacts
were read only; no update, build, clone, fetch, or dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1562` | 0 | rank 573, planned, legacy artifacts unaccepted, theorem incomplete |
| repository `rg` search for the theorem ID, names, and discovery wording | 0 | found only sparse catalogue metadata, this intake, and neighboring dossiers; no exact proposition or Lean target |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | SHA-256 values `651c8a...b1d2` and `321626...2d81` |
| pinned-mathlib `rg` search for Tracy-Widom, Airy kernel, Fredholm determinant, KPZ, and space-time white noise | 1 | no target-specific declarations |

## Retry condition

Preserve immutable primary sources for the finite-size GUE edge theorem, the Airy-kernel
identification, and the narrow-wedge KPZ theorem. Record exact theorem/equation/page locators and
content hashes, audit every normalization and bridge, check errata, and obtain independent source
approval. Then implement or import the missing definitions without assuming either limit, freeze
the exact Lean proposition, minimize its imports, serialize the elaborated expression, check all
credited transports, and run all four mutation classes.

No statement acceptance, proof credit, audit completion, or theorem completion is claimed. No
`.stage1-worker-selftest.json` is emitted because the assigned phase is blocked rather than
genuinely self-tested.
