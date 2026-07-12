# Source-statement crosswalk

## Available record

The repository record in `Docs/researches/math_theorems.md` says only: Gennadi Kasparov, 1980,
"bivariant K-theory of operator algebras". `Docs/Stage0_Blueprint.md` repeats that gloss and leaves
the definitions, proof path, assumptions, axioms, and machine artifact open. Its `已验证` label is
untrusted metadata under rev-5.6 and gives neither human-source nor kernel credit.

## Primary-source candidates

- G. G. Kasparov, *The operator K-functor and extensions of C*-algebras*, originally published in
  Russian in 1980, with an English translation in *Mathematics of the USSR-Izvestiya* 16 (1981).
  This is a primary candidate for the foundational nonequivariant theory and Kasparov product.
- G. G. Kasparov, *Equivariant KK-theory and the Novikov conjecture*, *Inventiones Mathematicae*
  91 (1988). This is a primary candidate only if the selected target is explicitly equivariant.

These are bibliographic discovery anchors, not `H0` evidence. The papers, exact theorem numbers and
pages, original/translation differences, definitions, assumptions, and errata have not been
independently inspected in this intake. The later source audit must not merge the ordinary and
equivariant statements.

## Crosswalk

| Repository/source phrase | Provisional mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "operator algebras" | C*-algebras and Hilbert C*-modules | concrete C*-algebra, graded algebra, Hilbert-module, adjointable/compact operator APIs | domain family identified; hypotheses open |
| "bivariant" | contravariant first and covariant second variable | two-variable `KK` object with functorial maps | variance identified; exact category open |
| "K-theory" | homotopy classes/groups of Kasparov cycles | cycles, degeneracy, homotopy, equivalence relation, quotient/group construction | construction family identified; encoding open |
| Kasparov product | composition through an intermediate algebra | well-defined bilinear map `KK(A,D) x KK(D,B) -> KK(A,B)` | provisional central claim; exact theorem open |
| categorical structure | associativity and identity KK-classes | checked equality laws and unit witnesses | possible conclusion package; source boundary open |
| 1980 / Kasparov | historical locator | no formal component and no proof credit | primary candidate identified only |

## Statement and machine boundary

A repository-wide text search found no theorem-specific Lean artifact for `THM-M-0591`; the only
other occurrence in an instance dossier is an exclusion/cross-reference from another target. This
is a local intake observation, not an exhaustive mathlib or external-project anchor audit. No Lean
declaration, exact type, terminal body, immutable external revision, or environment closure is
credited.

Before `H0`, an independent domain reviewer must approve a pinpoint edition/theorem/page crosswalk,
all definitions and hypotheses, the proof boundary, translations/corrections, and errata. Before
statement credit, the approved rows must map to one elaborated Lean expression with checked
transports for every alternate form. The present theory label is too broad for that gate.
