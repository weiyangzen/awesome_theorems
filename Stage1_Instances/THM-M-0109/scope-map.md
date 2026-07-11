# Scope map

## Frozen repository inputs

The manifest identifies `THM-M-0109` as `周炜良引理`, conventionally rendered
"Chow's lemma," in algebraic geometry. The repository research catalog dates it
to 1949 and gives only the gloss `代数簇的坐标环性质` (properties of the
coordinate ring of an algebraic variety). This phrase does not determine a
proposition: it names no ring property, base, finiteness/separation hypothesis,
or conclusion.

Accordingly the intake freezes the ambiguity rather than a fabricated root.
The exact objects, ordered binders, hypotheses, conclusion, universe levels,
degenerate cases, and foundation profile remain unresolved and must be fixed by
the statement phase from an authoritative source.

## Candidate interpretations, not accepted scope

1. The standard scheme-theoretic Chow lemma concerns a proper morphism (under
   hypotheses that vary by formulation) and a projective modification/model.
2. The catalog gloss could instead intend a finite-generation, quotient, or
   Noetherian property of an affine coordinate ring.

These are materially different statements. The intake does not assert that
either is intended and grants neither statement nor proof credit.

## Explicit exclusions

- Do not substitute finite-type algebras being quotients of polynomial rings.
- Do not substitute finite-type algebras over a field being Noetherian.
- Do not replace projectivity by properness or claim the converse.
- Do not accept an abstract witness structure whose crucial projectivity field
  is encoded only as `AlgebraicGeometry.IsProper`.
- Do not infer source fidelity from the untrusted `已验证` metadata label.

## Statement-phase obligations

Identify an authoritative source and exact locator; transcribe its claim and
assumptions; determine whether the catalog name or gloss is erroneous; freeze
the native Lean object model; and mutation-test every necessary finiteness,
properness, separatedness, reducedness/integrality, base, and projectivity
hypothesis actually present in the resolved source. If the conflict cannot be
resolved, the statement node must remain blocked rather than broaden or
substitute the theorem.
