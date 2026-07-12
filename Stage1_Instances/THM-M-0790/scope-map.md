# Scope map

## Included topic boundary

- A source-selected definition of a supercompact cardinal `kappa` in a fixed set-theoretic
  foundation.
- The exact source-selected property, characterization, or equivalence, with all cardinal bounds.
- If using elementary embeddings: the domain universe/model, target model, critical point,
  transitivity, and closure condition at each `lambda >= kappa`.
- If using ultrafilters: the carrier `P_kappa(lambda)` and exact completeness, fineness, normality,
  and nonprincipality requirements.
- Checked transports between formulations only in directions actually proved.

## Decisions required at statement freeze

1. Identify a primary or authoritative source theorem rather than the topic phrase "properties".
2. Fix whether the target is a definition equivalence, an implication such as supercompact implies
   strongly inaccessible, a compactness theorem, or another named consequence.
3. Fix the ambient object theory (for example ZFC), metatheory, model coding, universes, and the
   distinction between internal and external cardinal arithmetic and powersets.
4. Freeze all ordered binders, especially `kappa`, every `lambda >= kappa`, the embedding or
   ultrafilter witnesses, and all hypotheses.
5. Decide boundary cases and conventions for finite/zero cardinals, proper classes, target-model
   closure, critical points, and universe lifting.

## Explicit exclusions

- Strong compactness, measurability, Woodinness, or mere strong inaccessibility as substitutes.
- The bare existence assertion "there is a supercompact cardinal" unless an exact source selects it.
- A structure that assumes the requested property as a field and proves it by projection.
- A generic elementary embedding between arbitrary first-order structures without encoded
  membership models, critical point, transitivity, and closure.
- An ordinary ultrafilter without the source-required completeness, fineness, and normality.
- The repository label `已验证` or nearby cardinal APIs as source or proof evidence.

No canonical Lean proposition is frozen at intake because the repository does not state one.
