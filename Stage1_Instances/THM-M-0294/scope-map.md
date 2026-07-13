# Scope map

## Frozen catalog boundary

The repository fixes only the name `普朗歇尔定理`, attribution to Michel Plancherel, the year 1910,
the gloss `L^2函数的傅里叶变换等距性`, importance "high," and an untrusted `已验证` status. This
identifies the Plancherel theorem family, but it supplies no citation, formula, definition chain,
ordered binders, assumptions, conclusion, proof boundary, correction record, or reviewer.

Consequently this intake freezes the theorem family and non-substitution boundary, not an exact
claim. No canonical statement, formal expression, credited alternate encoding, or excluded case is
selected.

## Proposition-changing choices

An approved statement must decide all of the following together:

1. The spatial domain: `R`, `R^n`, an arbitrary finite-dimensional real inner-product space, or a
   locally compact abelian group and its dual, with all universe and typeclass assumptions.
2. The scalar or value space: complex scalars, real scalars with a complexified transform, or a
   complex Hilbert-valued function.
3. The Fourier character, sign, `2 * pi` convention, bilinear pairing, and compatible Lebesgue,
   volume, or Haar measures on the source and target.
4. The `L^2` carrier: measurable representatives with a `MemLp` witness, equivalence classes modulo
   almost-everywhere equality, or another source-approved construction.
5. How the transform is extended from an integrable or Schwartz dense subspace, and whether
   density, extension independence, and agreement with the integral transform are root content or
   proof obligations.
6. The conclusion: norm preservation only, inner-product preservation, a linear isometry, a unitary
   equivalence, inversion, surjectivity, or a source-selected conjunction of these.
7. Exact ordered binders, hypotheses, constants, equality conventions, foundation/TCB/computation
   profiles, and every alternate encoding with its checked relationship.

These choices can change both the proposition and the proof boundary. They belong to the statement
phase after primary-source and duplicate-target review.

## Candidate family, not credited

A conventional Euclidean reading says that the correctly normalized Fourier transform extends to
an isometry of complex-valued `L^2(R^n)` and hence preserves norms and inner products. Pinned mathlib
uses finite-dimensional real inner-product domains, volume measure, and the character giving the
kernel `exp(-2 * pi * i * <v,w>)`; its transform is a complex linear isometry equivalence. This is a
high-quality candidate scope, not the canonical claim supplied by the sparse catalog record.

## Degenerate and boundary cases

Source review must explicitly dispose of dimension zero and one; the zero function; null-modified
representatives; functions not initially in `L^1`; Schwartz and `L^1 intersection L^2` dense
subspaces; real versus complex inputs; scalar versus Hilbert-valued outputs; sign reversal; measure
rescaling; normalization constants; and whether inverse-transform and surjectivity cases are part
of the root. No case is silently excluded at intake.

## Excluded substitutions

- `THM-M-0342`, its selected Euclidean statement, artifacts, receipts, or debt vector cannot be
  merged into this target without an accepted identity and ownership decision.
- Parseval identities only for Fourier series, an orthonormal basis, a torus, a finite group, or a
  Schwartz subspace do not by themselves establish the requested all-`L^2` Fourier-transform root.
- The `L^1` to `L^infinity` bound, Hausdorff-Young, Fourier inversion, Riemann-Lebesgue, or Poisson
  summation cannot replace norm isometry merely because they are adjacent Fourier results.
- A transform with an unexplained normalization constant, a one-dimensional-only special case, or
  a broader LCA-group or Hilbert-valued theorem cannot silently replace a source-selected scope.
- A structure field, hypothesis, axiom, oracle, numerical experiment, or unchecked certificate
  that assumes isometry supplies no existence or preservation proof.
- A theorem name, passing API probe, catalog `已验证` label, or sibling wrapper supplies no H or M0
  credit for the unfrozen root.

## Neighbor and collision boundaries

`THM-M-0342` is a likely semantic duplicate under `分析学 / 调和分析`; it remains separate pending
integration review. `THM-M-0295` owns the neighboring Hausdorff-Young `L^p` estimate, and
`THM-M-0341` owns Fourier inversion. A future proof may use related nodes, but proximity grants no
scope, evidence, or state.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, module `Mathlib.Analysis.Fourier.LpSpace` defines the
`L^2` Fourier transform as a linear isometry equivalence and proves norm and inner-product
preservation. The discovery probe checks those declarations and a complex scalar Euclidean
specialization without declaring a theorem. The sibling `THM-M-0342` path contains a provisional
exact target and proof wrapper, but those artifacts cannot identify this catalog record's missing
source clauses or transfer proof credit before duplicate review and a checked target transport.
