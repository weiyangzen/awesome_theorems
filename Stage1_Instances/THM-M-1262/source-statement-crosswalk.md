# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` names "microlocal analysis", attributes it to Lars Hörmander in
the 1970s, and glosses it as "local and frequency analysis of PDEs". `Docs/Stage0_Blueprint.md`
repeats that gloss. Neither entry contains a proposition, citation, assumptions, or conclusion.
The `source_status_untrusted` value "verified" in the target manifest is metadata and receives no
H or M credit.

## Primary-source candidates

- Lars Hörmander, *The Analysis of Linear Partial Differential Operators I: Distribution Theory
  and Fourier Analysis*, Springer. This is a relevant primary monograph candidate for wavefront-set
  foundations; edition, theorem number, page, exact wording, and errata remain uninspected.
- Lars Hörmander, *The Analysis of Linear Partial Differential Operators III:
  Pseudo-Differential Operators*, Springer. This is a relevant primary monograph candidate for
  microlocal operator theorems; edition, theorem number, page, exact wording, and errata remain
  uninspected.

These are discovery anchors only, not `H0` evidence.

## Crosswalk

| Repository text | Mathematical information | Lean requirement | Intake result |
|---|---|---|---|
| "microlocal analysis" | names a field/method | no proposition can be elaborated | unresolved |
| "local" | localization in base variables | topology/domain and local regularity predicate | unspecified |
| "frequency" | cotangent or Fourier directions | cotangent/frequency space and zero-section convention | unspecified |
| "analysis of PDEs" | intended application domain | distribution and differential/operator interfaces | unspecified |
| "verified" | untrusted catalog status | kernel receipt for an exact declaration | absent |

## Statement gate

An independent source inspection must select one proposition, justify that selection against the
catalog intent, and record stable edition, theorem/page, definitions, assumptions, nearby context,
and errata. Until that happens, any concrete Lean theorem would be an invented substitution. Repo
search found no Lean declaration or module mentioning `wavefront` or `microlocal`; this negative
result is discovery evidence only and must be repeated against the pinned dependency during anchor
audit.
