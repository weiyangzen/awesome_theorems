# Scope map

## Preserved catalog scope

The repository fixes target `THM-M-0939`, title `Kemperman定理`, attribution Johannes Kemperman,
year 1960, and the gloss `阿贝尔群上子集和的结构`. It supplies no bibliography, formula,
definition, binders, hypotheses, conclusion, theorem locator, correction history, or formal
artifact. Importance `高` and status `已验证` are inventory metadata only.

The same gloss is attached to neighboring `THM-M-0938` (Kneser theorem), so the prose cannot by
itself distinguish a structural classification from a lower-bound theorem. The attribution and
year strongly point toward Kemperman's 1960 classification of small sumsets, but do not select its
original pair statement, a modern equivalent formulation, or an explicitly checked package.

## Candidate roots, not canonical

The primary bibliographic candidate is J. H. B. Kemperman, *On small sumsets in an abelian group*,
*Acta Mathematica* 103 (1960), 63-88, DOI `10.1007/BF02546525`.

Two inspected modern roots sharpen the likely scope:

- Boothby-DeVos-Montejano Theorem 4.5: every maximal nontrivial critical trio `Upsilon_1` in an
  abelian group `G_1` admits a finite descending chain of ambient subgroups and continuations;
  every nonterminal trio is an impure beat or impure chord, and the terminal trio is a pure beat or
  pure chord.
- Lev Theorem C, citing Kemperman [K60, Theorem 5.1]: finite nonempty `A,B` in a nontrivial
  abelian group satisfy the small-sumset inequality together with Kemperman's aperiodic-or-unique-
  representation condition exactly when they admit elementary residual subsets and a nonzero
  subgroup satisfying four quotient/coset conditions.

Neither formulation is canonical at intake. The statement phase must either admit one exact root
and prove or source-map all required equivalences, or select a source-approved structured package
that preserves rather than weakens the intended classification.

## Proposition-changing decisions

1. Choose the original 1960 theorem, Lev's pair variant, Boothby-DeVos-Montejano's trio variant, or
   a reviewed package with explicit checked equivalences; fix exact edition, theorem/page, proof
   boundary, correction history, and independent review.
2. Fix whether the ambient object is an arbitrary abelian group or a finite abelian group, and
   whether the classified objects are finite pairs, finite/cofinite trios, or both with transports.
3. Fix sumset, translation, negation, complement, quotient-map, coset, subgroup-order, stabilizer/
   period, `H`-stable, and generated-subgroup conventions.
4. Fix criticality and deficiency for pairs and trios, including the cardinal arithmetic used when
   a trio contains a cofinite set and the definition of trivial versus nontrivial.
5. Fix pure pairs, superpairs, trios, supertrios, maximality, similarity under permutation and
   compensating translations, and the pair-to-maximal-trio bridge.
6. If the recursive trio root is chosen, transcribe closure `[A]`, quotient `R`-sequences, pure and
   impure beats, pure and impure chords, continuation, strict subgroup descent, and termination.
7. If the pair root is chosen, transcribe representation counts, `mu(A,B)`, Kemperman's condition,
   all four elementary-pair types, residual subsets, quotient images, coset-union conditions, and
   uniqueness in the quotient sum.
8. Fix ordered binders, universes, finiteness witnesses, decidability/classical-choice requirements,
   equality versus inequality normalizations, and every checked transport between `Set` and
   `Finset` encodings.

## Boundary cases

No case is silently discarded at intake. Source review must decide the trivial ambient group;
finite versus infinite ambient groups; empty `A`, `B`, or `C`; singleton sets; `A+B = G`; finite
and cofinite trio members; zero deficiency and deficiency one; periodic and aperiodic sumsets;
trivial and whole stabilizers; zero, proper, finite, and infinite subgroups; singleton and full
cosets; a one-term descending chain (`m = 1`); complements in infinite groups; arithmetic
progressions wrapping around a finite cyclic quotient; duplicate descriptions among elementary
types; and whether similarity preserves all selected encodings definitionally or only by proof.

## Neighbor and substitution exclusions

- `THM-M-0938` owns Kneser's theorem. Its stabilizer-sensitive cardinality bound is an ingredient
  and reduction tool, not Kemperman's recursive classification.
- `THM-M-0937` owns Vosper's theorem. Prime cyclic groups and the singleton/progression outcomes
  are a special case, not the arbitrary-abelian-group theorem.
- `THM-M-0936` owns Cauchy-Davenport. Its lower bound in `ZMod p` neither classifies general
  critical pairs nor supplies the beat/chord recursion.
- The Kemperman-Scherk inequality `|A+B| >= |A| + |B| - mu(A,B)` is a distinct representation-
  count result. Name overlap cannot substitute it for Kemperman's structure theorem.
- Kneser's theorem plus a statement that critical pairs exist, a single elementary pair, one pure
  beat/chord branch, a finite-group-only special case, or a hypothesis storing the desired chain is
  not the full classification.
- A DOI, source PDF, theorem name, API probe, or the catalog's `已验证` label grants no human-source
  or kernel proof credit.

## Downstream boundary

The statement phase must admit and independently review one exact root before freezing a Lean
module, canonical expression, environment fingerprint, transports, or mutations. Anchor audit,
obligation registry, proof architecture, implementation, validation, and release remain separate
open tasks.
