# Scope map

## Included subject boundary

- Adams-type spectral sequences constructed from a resolution with respect to a homology or
  cohomology theory.
- For the classical mod-`p` form: the Steenrod algebra, an `Ext`-group `E_2` page, differentials,
  filtration, and an abutment involving a completed or localized stable homotopy group.
- Stable maps of spectra (or the sphere-spectrum specialization), with all connectivity, finite
  type, nilpotence/completeness, and convergence hypotheses made explicit.
- Indexing conventions, edge maps, multiplicative structure, and strong versus conditional
  convergence are statement-relevant rather than presentational details.

## Required source decision

The metadata phrase "calculation of stable homotopy groups" does not determine a theorem. The
statement phase must select exactly one source theorem, for example:

1. the classical mod-`p` Adams spectral sequence for stable maps, with an `Ext` `E_2` page and a
   precisely stated convergence target;
2. its sphere-spectrum specialization used to compute stable stems;
3. a generalized Adams spectral sequence for a chosen ring spectrum or homology theory.

It must also freeze prime/coefficient field, source and target spectra, grading convention,
category, convergence mode, completion/localization, and the meaning of the abutment. It must not
replace the construction theorem by a finite table of computed stems or combine variants.

## Explicit exclusions

- The slogan that the sequence "computes stable homotopy groups" as though it were a proposition.
- The Serre, Atiyah-Hirzebruch, Adams-Novikov, or Bockstein spectral sequence as a substitute.
- A spectral-sequence definition with convergence assumed as a hypothesis or an abstract `Prop`
  whose desired conclusion is assumed.
- Any legacy wrapper, metadata label `已验证`, or adjacent mathlib homology API as proof credit.

The statement phase must freeze universes, categorical models, grading and differential signs,
imports, declaration type, environment fingerprint, checked transports, and hypothesis mutations.
