# Scope map

## Preserved catalog boundary

The repository fixes target identity `THM-M-0258` and supplies four untrusted descriptive fields:
the title `沃尔夫-登乔定理`, the attribution Hartmut Wolf/Ken'ichi Ohshika, the year 1990, and
the gloss "boundary of Teichmuller space." Intake preserves all four without pretending they form
one proposition.

## Competing readings not credited

1. **Classical Denjoy-Wolff dynamics.** A holomorphic self-map of the unit disc or another
   hyperbolic domain, under a source-specific non-elliptic or no-interior-fixed-point condition, has
   a distinguished boundary point to which iterates converge. The exact hypotheses, domain,
   exceptional automorphisms, convergence mode, and conclusion depend on the selected formulation.
2. **A Teichmuller compactification theorem.** A finite-type Teichmuller space embeds into a
   compact space and has a boundary identified with projective measured foliations, laminations,
   quadratic differentials, or other source-specific data. Thurston, Bers, Gardiner-Masur,
   Weil-Petersson, and horofunction boundaries are not interchangeable.
3. **A harmonic-map degeneration or boundary-description theorem.** A family or ray in
   Teichmuller space has a limit described using harmonic maps, quadratic differentials,
   measured foliations, or trees. No such input family or conclusion appears in the catalog.
4. **A Kleinian-group boundary theorem associated with Ohshika.** Bers boundary, ending
   laminations, deformation spaces, and compactification results require different objects and
   assumptions. The catalog supplies no source allowing one to be selected.

No candidate is the canonical claim at intake.

## Statement-phase decisions

An independently reviewed target correction must freeze:

- the theorem identity, correct authors, date, primary source, exact locator, and incorporated
  definitions;
- whether the domain is a unit disc, another complex domain, a Teichmuller space, a deformation
  space, or a family of marked surfaces;
- for a dynamics reading, the holomorphic-map regularity, fixed-point and automorphism exclusions,
  iterate convention, distinguished point, and pointwise, locally uniform, or other convergence;
- for a Teichmuller reading, the surface genus, punctures and boundary components, finite-type and
  stability assumptions, markings, equivalence, metric, and mapping-class-group conventions;
- the exact compactification or boundary construction, its topology, embedding, boundary subset,
  equivalence relation, and whether the claim is existence, identification, convergence,
  continuity, compactness, density, or classification;
- all universes, ordered binders, hypotheses, conclusion clauses, foundation/TCB/computation
  profiles, alternate encodings with checked transports, and statement mutations.

## Boundary cases to resolve

For a Denjoy-Wolff reading: constant maps, the identity, elliptic automorphisms, maps with an
interior fixed point, boundary fixed points with different angular derivatives, non-disc domains,
and the distinction between pointwise and locally uniform convergence.

For a Teichmuller reading: genus zero and one, unstable or empty surface types, punctures and
boundary components, labeled versus unlabeled markings, finite versus infinite type, compact
versus noncompact sequences, nonunique projective representatives, and dependence on the chosen
compactification.

No case is excluded before a source-selected proposition exists.

## Explicit exclusions

- Do not silently replace the catalog target by the classical Denjoy-Wolff theorem merely because
  the Chinese title resembles its reversed name.
- Do not silently replace it by the Thurston, Bers, Gardiner-Masur, Weil-Petersson, or horofunction
  boundary of Teichmuller space.
- A theorem about one compactification, one surface type, one ray, or one degeneration does not
  prove a universal or differently encoded boundary theorem.
- `THM-M-0255` quasiconformal mapping theory, `THM-M-0256` Teichmuller theory, and `THM-M-0257`
  Ahlfors-Bers complex structure remain separate targets and grant no inherited credit.
- The generic one-point compactification, a unit-disc API, Schwarz lemma, a quotient, manifold,
  group action, or convergence lemma is not the requested theorem without a checked source-faithful
  bridge.
- A structure or hypothesis storing the desired boundary, limit, compactification, or
  identification supplies no proof.
- Numerical pictures, finite samples, theorem names, citations, `#check` output, and the untrusted
  catalog label `已验证` supply no H or M credit.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery probe authenticates generic complex
unit-disc, Schwarz, manifold, and one-point-compactification interfaces. It deliberately does not
declare a target. The bounded exact-topic search is scoped discovery evidence, not an exhaustive
anchor audit or a proof of global absence.
