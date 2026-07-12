# Scope map

## Included theorem family

- Finite-dimensional smooth manifolds `M` and `N`, of dimensions `m` and `n` respectively.
- A smooth map `f : M -> N`.
- The critical-point locus where the tangent map `d f_x : T_x M -> T_(f x) N` is not
  surjective, and its image, the set of critical values.
- The conclusion that the critical-value set is null for the target's `n`-dimensional smooth
  measure class, equivalently chartwise Lebesgue null after conventions are proved compatible.

The repository wording says "smooth", so the intake does not weaken the target to a finite
differentiability special case. The sharp `C^k` theorem is a possible alternate encoding only
after its relation to the smooth claim is source-checked and represented by a checked implication.

## Decisions required at statement freeze

The statement phase must select and inspect an immutable primary-source edition and freeze:

- manifolds over the real scalars, their Hausdorff/second-countable assumptions, and whether
  boundary or corners are admitted;
- the dimensions and their encoding, including dimension-zero and empty-manifold cases;
- smoothness versus a finite `C^k` hypothesis and the exact threshold (classically
  `k > max (m - n) 0`);
- the derivative definition and the exact surjectivity predicate on tangent maps;
- whether critical values are expressed as the image of critical points or by an existential;
- the target null-set notion, its chart invariance, and any selected volume measure;
- ordered binders, universes, implicit typeclass assumptions, and measurability obligations.

The Euclidean theorem and the manifold theorem must not be conflated: if the selected primary
statement is Euclidean, chart reduction and countable-atlas assembly are proof obligations rather
than silently imported wording.

## Explicit exclusions

- Morse's lemma, Morse-Sard genericity, transversality, the regular-value theorem, or the inverse
  function theorem alone.
- A claim merely that critical values have empty interior, are meagre, or have lower dimension.
- A statement about the measure of critical *points* in the source.
- A special case for scalar-valued functions, polynomials, analytic maps, or Euclidean spaces as a
  substitute for the scoped smooth-manifold claim.
- A structure or hypothesis containing the desired null-set conclusion as data.
- The repository's `已验证` label as human-proof or kernel evidence.

No Lean target is frozen at intake. A later formal statement must expose concrete manifold,
derivative, rank/surjectivity, image, and null-set interfaces without assuming Sard's conclusion.
