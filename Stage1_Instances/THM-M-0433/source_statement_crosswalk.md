# Source-statement crosswalk

Statement-phase status: blocked. This crosswalk does not select or elaborate a canonical Lean
target, and the provisional intake sentence must not be treated as an exact proposition.

| Claim component | Human source anchor | Lean discovery surface | Intake assessment |
|---|---|---|---|
| Global correspondence for `GL_r` over a function field | L. Lafforgue, *Chtoucas de Drinfeld et correspondance de Langlands*, Invent. Math. 147 (2002), 1-241, especially the global correspondence stated in Théorème VI.9 | No terminal local declaration identified | Primary proof source located; edition, exact French statement, assumptions and errata require independent audit (`H1`) |
| Irreducible continuous l-adic representations with determinant of finite order | Same theorem and its Galois-side definitions | `LafforgueGaloisParameter` and `LafforgueGaloisWeilSide` in the legacy module | Abstract predicates expose intended fields but are not a checked translation |
| Cuspidal automorphic representations of `GL_r` with central character of finite order | Same theorem and automorphic-side definitions | `LafforgueAutomorphicSide` | Automorphic representation and full adelic quotient are abstract, not mathlib objects |
| Compatibility away from ramification | Same theorem; compare its local Euler/Frobenius normalization | `FrobeniusHeckePolynomialMatches` | Polynomial equality has a useful shape, but source normalization and concrete constructions remain open |
| Function-field and finite-place substrate | Source curve/function-field conventions | `FunctionFieldFinitePlace`, `FunctionFieldFiniteAdeleRing`, `FunctionFieldFiniteAdeleGLn` | Concrete mathlib-adjacent candidates; only finite affine places/adeles are represented |

## Exact premise and boundary mapping

| Required statement component | Current evidence | Statement-gate result |
|---|---|---|
| Base field, curve/function field, and rank binder | The intake says a global function field and rank `n`; no immutable transcription fixes the curve encoding, constants, or precise positivity binder | Open; no ordered Lean binder is credited |
| Galois or Weil parameter domain | The intake alternates between absolute-Galois and Weil formulations; the legacy module supplies only abstract packages | Open; no checked equivalence or transport exists |
| Coefficients and parameter equivalence | The coefficient field/closure, topology, embeddings, and isomorphism-class convention are not source-frozen | Open; choosing them would change the proposition |
| Continuity, irreducibility, ramification, and determinant | The legacy fields are arbitrary `Prop` data and the determinant/twist convention is unresolved | Open; abstract fields are interface scaffolding only |
| Automorphic representation domain | No full function-field adele ring, adelic quotient, smooth admissible representation, cuspidality, or isomorphism-class API exists in the pinned closure | Open; finite adeles and `GL_n` are adjacent substrates only |
| Central-character restriction | The finite-order convention and its relationship to the Galois determinant are not source-frozen | Open |
| Unramified local compatibility | Arithmetic versus geometric Frobenius, excluded places, Satake/Hecke normalization, and characteristic-polynomial direction are unresolved | Open; no local compatibility expression is credited |
| Correspondence strength | The source theorem is expected to give a bijection on equivalence classes, while the legacy `StatementShape` exposes only an abstract realization interface | Open; existence in the abstract interface is not a correspondence theorem |
| Rank-one and other boundary cases | No reviewed source crosswalk fixes the rank-one specialization, zero-rank exclusion, or ramified boundary | Open; no boundary mutation is meaningful yet |

Discovery link: <https://doi.org/10.1007/s002220100174>. This URL is not an immutable evidence
receipt. Before `H0`, the audit must retain a content hash or edition identifier, transcribe the
exact theorem and definitions, map every premise and conclusion, check corrections/errata, and
obtain independent review.

The English sentence in `intake.json` is deliberately provisional. In particular, it does not
choose arithmetic versus geometric Frobenius, identify Weil-group and absolute-Galois formulations,
or assert that equality of one chosen polynomial convention is already the source's exact local
condition. Those choices belong to the statement phase and require checked transports.

The target-owned `Statement.lean` therefore probes only the pinned adjacent interfaces. Its absence
of a canonical declaration and expression fingerprint is intentional fail-closed evidence. The
statement phase validator must report `phase_accepted=false`; neither the catalog's historical
"verified" label nor the elaborating legacy module transfers statement or proof credit.
