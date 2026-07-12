# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records the Chinese title `岩泽理论`, attributes it to Kenkichi
Iwasawa in the 1960s, and gives only `分圆域的p-adic L-函数` ("p-adic L-functions of cyclotomic
fields"). Stage0 repeats this metadata and explicitly leaves the definitions, assumptions, proof,
dependencies, axioms, and formal artifact open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted`.

The next source-inventory entry, `岩泽主猜想`, has the distinct gloss "relation between p-adic
L-functions and class groups". This adjacency is useful negative scope evidence: it does not turn
the present topic label into the main-conjecture statement. No supplied record gives a primary
source edition, theorem number/page, exact assumptions, errata, or proof boundary.

## Candidate source work

Iwasawa's original papers and authoritative treatments of cyclotomic fields are candidate
locators, not accepted sources at intake. The source audit must identify an immutable edition and
passage containing the intended theorem, record its exact notation, assumptions, proof boundary
and errata, map every clause to the formal target, and obtain independent review. Assigning a
specific interpolation theorem now would be speculation rather than an `H0` crosswalk.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "cyclotomic fields" | finite fields `Q(zeta_n)` or a cyclotomic `Z_p`-tower | `CyclotomicField`, `IsCyclotomicExtension`, plus a source-selected tower | finite-field API probed; tower open |
| "p-adic" | values in `Q_p`, its integers, or a finite extension | `Padic`, `PadicInt`, embeddings and topology | base APIs probed; codomain open |
| "L-functions" | Kubota-Leopoldt function, measure, or Iwasawa power series | source-specific definition and evaluation map | absent from source record |
| interpolation | values related to Dirichlet L-values/Bernoulli data | `DirichletCharacter`, L-series and exact normalization | complex ingredients probed; formula open |
| "Iwasawa theory" | module/class-group structure or growth theorem | tower, inverse limits, completed group ring, characteristic ideal | candidate only |
| `已验证` | untrusted inventory label | no proposition and no proof credit | explicitly rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe imports cyclotomic-field, p-adic, and Dirichlet-L-series modules and checks their principal
types. A bounded source-tree name search found `Mathlib.GroupTheory.GroupAction.Iwasawa`, but that
module concerns the unrelated group-simplicity criterion. The search found complex Dirichlet
L-series infrastructure but no declaration identified as the source-unspecified cyclotomic p-adic
L-function theorem. This is an intake observation, not the later immutable anchor audit or an
exhaustive negative result.
