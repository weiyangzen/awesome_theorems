# Source-statement crosswalk

## Available record

`Docs/researches/math_theorems.md` and `Docs/Stage0_Blueprint.md` provide only the Chinese title,
the gloss "the Euler class of oriented vector bundles", a twentieth-century date, and an untrusted
`已验证` label. They do not give a theorem, authorial source, hypotheses, or conclusion. Thus the
record cannot yet support `H0` or an exact Lean expression.

## Candidate sources

- Hassler Whitney, "On the theory of sphere-bundles", *Proceedings of the National Academy of
  Sciences* 26 (1940). This is a historical primary-source discovery candidate for obstruction and
  characteristic-class formulations. Its exact proposition, terminology, pages, assumptions, and
  corrections have not been inspected here.
- John W. Milnor and James D. Stasheff, *Characteristic Classes*, Annals of Mathematics Studies 76,
  Princeton University Press (1974), the Euler-class material. This is a stable modern source
  candidate for choosing a precise construction and property, but the exact theorem/page,
  definitions, assumptions, and errata remain to be inspected.

These bibliographic anchors are discovery evidence only, not primary-source acceptance or proof
credit. The statement phase must select one exact proposition rather than merge several results.

## Crosswalk

| Repository/source phrase | Candidate mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "oriented vector bundle" | finite-rank real bundle with a coefficient orientation | concrete bundle and orientation structures | included family; category and hypotheses open |
| "Euler class" | class `e(E)` in degree equal to the rank | graded cohomology element with degree bookkeeping | object family identified; coefficients open |
| Thom-class characterization | `e(E)` as zero-section pullback of a Thom class | Thom space/relative cohomology, Thom class, pullback | candidate formulation only |
| naturality | pullback preserves the Euler class | bundle pullback and cohomology functoriality | distinct candidate theorem |
| product formula | Euler class of a direct sum is a cup product | direct sum, cup product, orientation compatibility | distinct candidate theorem |
| obstruction/number results | vanishing or evaluation consequences | section, fundamental class, pairing | explicitly not selected at intake |
| `已验证` | repository status label | no Lean component and no proof credit | untrusted metadata |

## Machine boundary

A scoped repository and pinned-mathlib text search found no topological `EulerClass` declaration or
Euler-class theorem. The only repo-local `EulerClass` name located is in
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_090.lean`, where it denotes arithmetic Euler
system classes and is outside this target's scope. This negative search is not the later immutable
anchor audit and does not establish nonexistence of an encoding under another name.

Before `H0`, an independent reviewer must verify the selected edition, exact theorem/page,
definitions, every assumption, sign/coefficient convention, proof boundary, and errata. Before
statement credit, those components must map row by row to an elaborated Lean target with checked
transports for any alternate encoding.
