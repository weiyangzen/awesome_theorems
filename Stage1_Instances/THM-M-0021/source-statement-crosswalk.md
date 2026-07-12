# Source-statement crosswalk

## Repository source

The earliest retained inventory record is `Docs/researches/math_theorems.md:170-175`. It gives the
Chinese title `布饶尔-西格尔定理`, the attribution Richard Brauer/Carl Siegel, the year 1945, and
only `数域类数的渐近估计` ("asymptotic estimates of number-field class numbers"). An identical
six-line record appears at `Docs/researches/math_theorems.md:3103-3108` under algebraic number
theory. Both records originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; their identical line-excerpt SHA-256 is
`77fa0bfe8cfab362c881c21156d425215d160e5b7b19e4472c5d0a5ab76949fb`.

`Docs/Stage0_Blueprint.md:690-715` retains the first record as `THM-M-0021` and explicitly leaves
the exact definitions and assumptions, proof route, equivalent statements, axiom use,
machine-checked status, and artifact links pending. Its excerpt SHA-256 is
`5d9cf2b2d16e6886d3398b575684bcc35f84a4f10453d4f00407aa77e0b200ad`.
The rev-5.6 manifest carries `已验证` only in `source_status_untrusted`; it is not human-proof or
kernel evidence. The duplicate supplies no stronger statement and shares no separate proof credit.

## Primary-source candidates

Historical primary-source leads are Richard Brauer, "On the Zeta-Functions of Algebraic Number
Fields," *American Journal of Mathematics* 69(2) (1947), 243-250, DOI `10.2307/2371849`, and its
Part II, *American Journal of Mathematics* 72(4) (1950), 739-746, DOI `10.2307/2372290`. These
bibliographic leads are recorded only to direct the statement/source-audit phase. This intake has
not pinned or inspected immutable copies, determined which part and passage matches the intended
variant, verified the relationship to Siegel's contribution, transcribed definitions and
assumptions, audited corrections or errata, or obtained an independent review. They therefore
supply no `H0` record and do not select a canonical variant.

## Crosswalk

| Repository/source element | Theorem-family interpretation | Required Lean component | Intake status |
|---|---|---|---|
| number fields | fields varying in a source-selected family | bundled `NumberField` carriers plus a sequence/family encoding | family and equality convention open |
| class number | cardinality of the ideal class group | `NumberField.classNumber` with coercion into the analytic codomain | adjacent pinned definition checked; role open |
| regulator | standard companion invariant in common formulations | `NumberField.Units.regulator` | absent from catalog gloss; adjacent pinned definition checked only |
| discriminant | scale measuring arithmetic complexity | `NumberField.discr`, absolute value, logarithm, and selected normalization | normalization and growth premise open |
| asymptotic estimate | relation along varying fields | exact filter plus `Tendsto`, asymptotic relation, or quantified bounds | conclusion kind not selected |
| degree restriction | controls the field family in standard variants | `Module.finrank` and a source-mapped growth predicate | absent from repository source |
| 1945 / Brauer-Siegel | historical catalog metadata | no proposition or proof credit | retained but not independently verified |
| `已验证` | untrusted inventory status | no source, statement, or kernel evidence | explicitly rejected as credit |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`IntakeProbe.lean` elaborates adjacent definitions, positivity facts for class number and regulator,
discriminant nonzeroness, and the generic `Filter.Tendsto` type. A bounded name search finds no
`Brauer-Siegel`-named declaration in pinned mathlib. Mathlib also contains ideal-counting
asymptotics for one fixed number field and the Dirichlet class-number formula; neither is an exact
Brauer-Siegel candidate and neither receives root credit here.

These observations are intake-only substrate discovery, not the comprehensive repo-local and
external candidate audit assigned to `S56-M-0021-ANCHOR_AUDIT`. Before statement credit, an
independently reviewed source passage must map every material domain, binder, hypothesis,
normalization, boundary case, and conclusion row to one elaborated Lean expression.
