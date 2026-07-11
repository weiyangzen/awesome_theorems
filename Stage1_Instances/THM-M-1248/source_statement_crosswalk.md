# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Weighted interpolation inequality family | L. Caffarelli, R. Kohn, and L. Nirenberg, "First order interpolation inequalities with weights," *Compositio Mathematica* 53 (1984), no. 3, 259-275 | No repo-local or mathlib declaration located during the bounded intake scan | Primary proof source identified; theorem/page-level case transcription and errata audit remain open (`H1`) |
| Weighted target norm | Primary paper, main theorem's left-hand side | weighted `MeasureTheory.Lp`/integral expression on Euclidean space | Representation candidate only; no elaboration or equivalence check |
| Weighted gradient norm | Primary paper, main theorem's first right-hand factor | Fréchet derivative/gradient plus weighted norm | Representation candidate only |
| Lower-order weighted norm | Primary paper, main theorem's second right-hand factor | weighted `Lp`/integral expression | Representation candidate only |
| Scaling and admissible region | Primary paper, hypotheses surrounding its main inequality | arithmetic predicate over real parameters | Exact inequalities, endpoints, origin convention, and case splits must be transcribed before statement freeze |
| Parameter-dependent constant | Primary paper's existential estimate | `exists C : Real, 0 <= C and ...` or a nonnegative-real variant | Exact codomain and finiteness encoding remain open |

Bibliographic discovery anchor: <http://www.numdam.org/item/CM_1984__53_3_259_0/>. This URL is not an
immutable receipt. The statement phase must obtain a stable source copy, record its digest, and
pinpoint the exact theorem and pages; source audit must map every assumption and inspect errata.

The repository-wide text scan found no exact CKN inequality declaration. This negative intake scan
is not the precommitted anchor audit and does not establish nonexistence. In particular, neighboring
`THM-M-1228` concerns CKN partial regularity for Navier-Stokes and is explicitly not a candidate for
this root.

No `H0`, exact-statement, or machine-proof claim is made.
