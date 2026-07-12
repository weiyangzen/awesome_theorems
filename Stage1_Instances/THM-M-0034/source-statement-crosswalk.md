# Source-statement crosswalk

## Repository record

The six-line record at `Docs/researches/math_theorems.md:263-268` was introduced at commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. It names the Quillen-Suslin theorem, attributes it to
Daniel Quillen and Andrei Suslin, gives 1976, and describes it only as `塞尔猜想的证明` (proof of
Serre's conjecture). The adjacent record at lines 256-261 glosses that conjecture as projective
modules over a polynomial ring being free. Stage0 repeats the same information while leaving exact
definitions, premises, proof route, alternate statements, axioms, and machine artifact open.

| Received component | Mathematical information | Missing exactness |
|---|---|---|
| Quillen-Suslin theorem | recognizable classical result family | no proposition or definition chain |
| proof of Serre's conjecture | links the result to the adjacent conjecture gloss | does not say whether the target is the module theorem, a proof-existence claim, or one proof route |
| projective modules | prospective premise | coefficient ring, handedness, finite generation, presentation, and universe omitted |
| polynomial ring | prospective scalar ring | coefficient class and variable set omitted |
| are free | prospective conclusion | basis cardinality, rank, stable versus actual freeness, and degenerate cases omitted |
| Quillen/Suslin, 1976 | historical attribution | no edition, theorem/page, proof split, translation, or errata data |
| verified | scheduling metadata | no H or M evidence |

## Primary publication leads

- Daniel Quillen, *Projective modules over polynomial rings*, *Inventiones Mathematicae* 36(1),
  167-171 (1976), DOI `10.1007/BF01390008`. Crossref metadata was inspected and confirms the
  title, author, venue, volume, pages, and December 1976 publication date.
- A. A. Suslin, *Projective modules over a polynomial ring are free*, *Doklady Akademii Nauk
  SSSR* 229(5), 1063-1066 (1976), MathNet `dan40545`, MR0469905. The four-page primary Russian
  scan was inspected. Its opening asks whether every projective `k[X1,...,Xn]`-module is free and
  says the answer is affirmative; its convention `P(A)` means finitely generated projective
  `A`-modules. Theorem 3* on page 1066 states that every finitely generated projective module over
  `C[X1,...,Xn]` is extended from a Dedekind ring `C`, and is free when `C` is a principal ideal
  domain. A field specializes this result to the familiar claim. A footnote says Theorems 1 and 3
  were independently obtained by Quillen. MathNet records receipt on February 26, 1976.

The Quillen metadata is a bibliographic discovery record, not a theorem passage. The Springer
full-text endpoint returned an HTML access page rather than the article PDF. Suslin's scan supplies
a pinpoint primary statement and assumptions, but it has not received an independent translation,
errata review, complete proof-to-node mapping, or reviewer acceptance. These leads support `H1`,
never `H0`.

## Selected component map

| Source component | Selected Lean component | Statement status | Remaining review |
|---|---|---|---|
| coefficient field `k` | `[Field k]` | field specialization of the PID clause selected | independent source approval open |
| named variables `X1,...,Xn` | `MvPolynomial (Fin n) k` and `0 < n` | finite ordered variables frozen | zero-variable extension uncredited |
| unital projective module `P` | additive group, module, and `Module.Projective` instances | commutative left-module encoding frozen | definition-chain review open |
| finitely generated `P` | `Module.Finite` | premise frozen from Theorem 3* | independent translation open |
| `P` is free | `Module.Free` | conclusion frozen | exact basis terminology review open |
| independent Quillen proof | no statement field or proof credit | not part of target identity | Quillen full text and crosswalk open |

The fully explicit elaborated expression is frozen in `statement.json` with SHA-256
`d80cc9860ed5a53c81a0851b4dc8e702aa5a23d448f373ae6d68ed0c9b5604b1`. No alternate encoding,
checked transport, or proof body is credited.

## Pinned formal-source boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, bounded searches for
Quillen-Suslin, Serre's conjecture, and projective modules over polynomial rings found no target
declaration. The relevant files define projective and free modules and make multivariable
polynomial rings free over their coefficient ring. They do not prove that a finitely generated
projective module over a polynomial ring is free. The nearby theorem
`Module.Projective.of_free` proves the reverse direction and cannot close the target.

This is bounded intake discovery, not the dependency-ordered anchor audit and not proof of global
absence. A later audit must search repo-local Lean, all pinned mathlib declarations and terminal
bodies, and credible immutable external Lean 4 projects under a precommitted protocol.

## Remaining source gate

The worker has proposed and self-tested the exact field specialization. Master acceptance still
requires an accountable reviewer to ratify the immutable Suslin scan, independently translate and
review Theorem 3*, check corrections and errata, reconcile Quillen's formulation, and approve the
target as the claim owned by `THM-M-0034` rather than `THM-M-0033`. Until then this remains H1 and
provisional; the Lean expression does not establish H0 source fidelity.
