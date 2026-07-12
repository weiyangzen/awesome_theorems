# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `极小模型`, attributes it to "many
mathematicians", dates it only to the twentieth century, and states `极小模型的性质` ("properties
of minimal models"). Stage0 repeats this metadata. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted`. No definition, theorem, hypotheses, conclusion, proof source, edition,
page, or formal artifact is supplied.

The adjacent entries for prime models and strongly minimal theories help locate the subject area but
do not disambiguate the proposition. Adjacency is not source evidence.

## Candidate source work

Standard model-theory monographs are candidate locators for the competing notions, but no edition
or passage has been accepted during intake. The source audit must locate a primary or authoritative
reference that actually uses the intended term, record edition, definition/theorem and page,
assumptions, proof boundary, and errata, then obtain independent review. Until then, assigning a
named theorem or historical author would be speculation rather than an `H0` crosswalk.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "model" | a structure satisfying a first-order theory | `Language`, `Theory`, `Theory.Model` or `Theory.ModelType` | pinned API probed; exact domain open |
| "minimal" | no proper model-substructure | `Language.Substructure`, model satisfaction, properness | candidate only |
| "minimal" | no proper elementary substructure | `Language.ElementarySubstructure`, properness | candidate only |
| "minimal" | finite/cofinite parameter-definable unary sets | `Set.Definable`, finiteness, complement | candidate only |
| "properties" | existence, uniqueness, characterization, or consequence | a concrete proposition and all hypotheses | absent from source record |
| `已验证` | untrusted inventory label | no Lean proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports `Mathlib.ModelTheory.Bundled` and `Mathlib.ModelTheory.Definability`. It checks the
types of bundled models, substructures, elementary substructures, their elementarity predicate,
and definability. These are encoding ingredients only. No declaration named for a general
"minimal model" theorem was identified by the bounded repository/mathlib name search, which is not
a substitute for the later immutable anchor audit.
