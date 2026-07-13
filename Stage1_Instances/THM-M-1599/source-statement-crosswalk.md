# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:11777-11782` records exactly the title `椭圆曲线密码学`,
attribution Victor Miller/Neal Koblitz, year 1985, gloss `基于椭圆曲线的密码`, importance
`高`, and status `已验证`. All six lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. That establishes repository provenance only. The
record contains no bibliography, protocol, formula, definition, ordered binder, hypothesis,
conclusion, security model, proof boundary, correction history, or formal artifact.

`Docs/Stage0_Blueprint.md:43471-43496` repeats the gloss while explicitly leaving the formal system,
foundation, precise definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest retains `已验证` only as untrusted
source metadata and resets the target to `L0 / rework_required`.

## Primary source-family leads

Victor S. Miller, "Use of Elliptic Curves in Cryptography," in *Advances in Cryptology - CRYPTO
'85 Proceedings*, LNCS 218, pages 417-426, Springer (1986), DOI
`10.1007/3-540-39799-X_31`, is a primary historical lead. The publisher PDF was inspected. It
proposes an elliptic-curve analogue of Diffie-Hellman key exchange, reviews elliptic-curve and
discrete-logarithm background, argues why known index-calculus attacks appear unsuitable, and
discusses scalar multiplication, curve and modulus selection, transmitted data, and implementation.
It expressly describes security as resting on unproved assumptions and uses heuristic language
such as "appears" and "unlikely."

Neal Koblitz, "Elliptic curve cryptosystems," *Mathematics of Computation* 48(177), pages 203-209
(1987), DOI `10.1090/S0025-5718-1987-0866109-5`, is a second primary historical lead. The
publisher PDF was inspected. It describes elliptic analogues of Massey-Omura and ElGamal systems,
probabilistic plaintext embeddings, parameter examples, primitive-point questions, heuristic
security comparisons, and a separate page-209 theorem and corollary on nonsmooth cyclic-subgroup
orders. The repository's year 1985 is historical attribution metadata, not a pinpoint locator for
either published text.

Neither lead is admitted as H0. The catalog cites neither work, selects no proposition from either,
and has no accepted local source copy, complete definition/assumption/proof/errata crosswalk, or
independent source review. The observed publisher-file and metadata-response hashes are recorded in
`intake-receipt.json` as discovery evidence only.

## Component crosswalk

| Catalog component | Source-family alternatives | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "cryptography" | key agreement, encryption, signatures, one-way functions, or a hardness/security result | protocol and adversary definitions or an algebraic correctness `Prop` | scheme and claim absent |
| "based on elliptic curves" | finite-field Weierstrass curve, selected subgroup and base point, scalar multiplication, point encoding | finite field, elliptic curve, point group, subgroup/order, scalar action | only generic curve/group substrate exists |
| Miller/Koblitz | separate proposals and several mathematical/algorithmic claims | immutable source IDs and proposition crosswalk | attribution does not select one result |
| protocol correctness | equality of honest outputs, decryption inverse, or signature verification | executable or relational algorithms plus side conditions | no protocol, keys, messages, randomness, or failure cases selected |
| security | ECDLP/CDH/DDH or another assumption; reduction or heuristic attack resistance | adversary, experiment, advantage, resource bound and reduction | model and conclusion absent; heuristics are not theorems |
| `已验证` | untrusted inventory label | no Lean declaration or receipt | no H or M credit |

## Pinned Lean discovery boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.AlgebraicGeometry.EllipticCurve.Projective.Point` exposes `WeierstrassCurve`,
`WeierstrassCurve.IsElliptic`, projective nonsingular points, and
`WeierstrassCurve.Projective.Point.instAddCommGroup`. The intake probe checks those APIs and prints
the imported group instance's axiom dependencies. It declares no protocol or local theorem.

A bounded case-insensitive search over pinned mathlib found no target-level cryptography,
elliptic-curve discrete-logarithm, ECDH, ECDSA, or ElGamal implementation. A negative lexical search
is not an exhaustive formal-candidate audit and cannot prove absence under other names or external
projects. No canonical Lean module, expression, minimal import, or proof body is selected at intake.

## Required source acceptance

Before statement elaboration, accountable reviewers must select one immutable truth-valued source
proposition, justify that it is the intended catalog target, and map every incorporated definition,
ordered binder, assumption, conclusion, proof dependency, security or correctness boundary,
correction, erratum, and degenerate case. An independent source and cryptography-scope review must
approve that mapping. Only then may a statement worker encode the claim, minimize pinned imports,
freeze expression and environment fingerprints, compile checked transports, and run the four
required mutation classes.
