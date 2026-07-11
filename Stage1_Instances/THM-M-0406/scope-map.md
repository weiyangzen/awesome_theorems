# THM-M-0406 scope map

## Frozen intake boundary

- Manifest identity: `THM-M-0406`, execution rank 19, legacy slot `S1-M-019`.
- Metadata name: `科利特-埃弗特斯定理` (`Corvaja/Evertse` in the Stage0 record).
- Metadata gloss: `曲线上整点的退化性` (degeneracy of integral points on curves), dated 2004.
- Eligible system: Lean 4 plus mathlib. The lifecycle is `planned`; all historical artifacts are discovery inputs only.
- Exact claim: **not frozen at intake**. The author pairing, object dimension, and gloss do not uniquely identify a published theorem.

## Included discovery material

The legacy file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_019.lean` proposes Pietro Corvaja and Umberto Zannier's 2004 surface theorem as a candidate correction. It contains checked planning declarations, but its abstract predicate fields are not an exact formalization and it receives no rev-5.6 proof credit.

## Excluded until statement audit

- A generic claim about arbitrary curves or surfaces.
- The Evertse--Ferretti projective-variety inequality.
- Corvaja--Zannier results merely sharing integral-point or Subspace-Theorem terminology.
- Any theorem obtained by replacing divisors, intersection inequalities, integrality conditions, or the exceptional-set conclusion with opaque propositions.

## Open scope decisions

1. Resolve whether `Evertse` is a metadata error for `Zannier` using a primary bibliographic source.
2. Transcribe the exact numbered theorem, including field, surface/curve, divisor, intersection, and integrality hypotheses and its precise non-density/curve-containment conclusion.
3. Only in the statement phase, select concrete Lean objects, ordered binders, universes, imports, degenerate cases, and a checked expression fingerprint.

Current vector: `[H1, M4, R4]`. This intake does not establish audit or theorem completion.
