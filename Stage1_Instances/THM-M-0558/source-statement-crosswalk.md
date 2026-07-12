# Source-statement crosswalk

## Source anchors

- Allen Hatcher, *Algebraic Topology*, Cambridge University Press (2002), Section 4.2, Theorem
  4.32 (the Hurewicz Theorem), printed page 366. This modern source is the pinpoint candidate for
  the selected first/absolute form. Exact wording, surrounding definitions, edition identity, and
  errata still require independent inspection before `H0`.
- Witold Hurewicz, "Beitrage zur Topologie der Deformationen. IV. Aspharische Raume," *Nederl.
  Akad. Wetensch. Proc.* 39 (1936), 215-224. This is a historical primary-source candidate, but no
  claim is made here that its formulation directly matches the modern root.

These anchors support `H1`, not `H0`. In particular, the repository's untrusted Chinese label
`已验证` and the Stage0 attribution/year are discovery metadata, not source acceptance.

## Crosswalk

| Repository/source component | Frozen interpretation | Required Lean component | Intake status |
|---|---|---|---|
| "relation between homotopy and homology groups" | first nonzero homotopy and homology comparison | one exact proposition, not a slogan | selected; formal target open |
| `(n-1)`-connected | path-connected and lower `pi_i` vanish | pointed connectivity predicate or explicit family | convention/source audit open |
| lower homology vanishes | reduced integral homology is zero below `n` | quantified vanishing of homology groups | included |
| Hurewicz homomorphism | canonical map induced from sphere representatives to singular cycles | concrete group homomorphism | API open |
| isomorphism in degree `n` | the canonical map, not an unrelated group equivalence | `IsIso`, bijectivity, or explicit equivalence with checked transport | encoding open |
| `n >= 2` | higher-degree theorem with abelian homotopy group | natural-number bound | included |
| `n = 1` clause | abelianization of the fundamental group | separate boundary statement | excluded from root |

## Fidelity risks to resolve

The statement phase must not silently add a CW hypothesis merely because it eases formalization,
nor omit one if the selected source needs it. It must distinguish reduced from unreduced degree-zero
homology, prove any transport between connectivity encodings, and retain the canonical map. The
historical paper, Hatcher theorem, and any Lean candidate must receive separate row-level mappings;
similar theorem names do not establish statement identity.
