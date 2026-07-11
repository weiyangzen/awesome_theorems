# Source-statement crosswalk

## Available source record

`Docs/researches/math_theorems.md` supplies only the Chinese title "Struwe compactness lemma",
Michael Struwe, 1984, the phrase "an alternative to the Palais-Smale condition", importance high,
and the untrusted label `已验证`. `Docs/Stage0_Blueprint.md` repeats these fields while marking exact
definitions, hypotheses, proof history, dependencies, foundations, and machine status as missing.
No bibliography, title, edition, theorem number, page, quotation, or errata record is attached.

Consequently this intake asserts no primary-source candidate. The words are compatible with
multiple inequivalent forms of Struwe's monotonicity trick and its applications; selecting one now
would invent missing mathematics. The metadata label is screening input and earns no H status.

## Crosswalk

| Source element | Information fixed | Information still required | Intake result |
|---|---|---|---|
| "Struwe compactness lemma" | attribution/name family | exact publication and theorem | unresolved |
| Michael Struwe / 1984 | author and approximate date | bibliographic identity and edition | unresolved |
| "alternative" | replaces some use of compactness | exact logical conclusion and quantifiers | unresolved |
| "Palais-Smale condition" | variational compactness context | functional, level, sequence, topology | unresolved |
| PDE category | likely application domain | equation, space, boundary/data assumptions | unresolved |
| `已验证` | untrusted repository label | source proof and kernel receipts | no credit |

## Existing Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_172.lean` selects
`abstractMonotonicityTrick` and defines a `StatementShape` producing a Palais-Smale/entropy sequence
from abstract proposition-valued hypotheses. The file explicitly states that this is not a terminal
proof and that concrete min-max, PDE-estimate, and Palais-Smale compactness obligations remain.
Accordingly it is a useful vocabulary and candidate map, not the canonical source statement.

The first downstream gate is primary-source identification and independent verification of an
edition/theorem/page/assumption/errata crosswalk. Only afterward may the statement phase decide
whether any legacy definitions faithfully encode the source theorem.
