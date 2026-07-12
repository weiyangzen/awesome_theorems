# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:9733-9738` supplies exactly the title
`柯西-科瓦列夫斯卡娅定理`, attribution "Augustin Cauchy/Sofia
Kovalevskaya", 1875, the gloss `解析ODE的解析解`, importance "high", and status
`已验证`. All six lines entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. That commit is repository
provenance, not a mathematical source revision.

`Docs/Stage0_Blueprint.md:36291-36316` repeats the gloss while explicitly
leaving precise definitions and premises, proof route, dependencies,
equivalent formulations, axioms, machine state, and artifact links open. The
rev-5.6 manifest preserves `已验证` only as `source_status_untrusted` and resets
the target to `L0 / rework_required`.

## Literal crosswalk

| Repository phrase | Mathematical component to freeze | Prospective Lean surface | Intake result |
|---|---|---|---|
| "Cauchy-Kovalevskaya theorem" | one exact ODE or PDE theorem and its source definitions | one elaborated proposition with checked alternate transports | famous theorem-family name; exact root open |
| "analytic ODE" | autonomous or nonautonomous vector field, scalar field, dimension, open domain, and analytic predicate | `AnalyticAt`, `AnalyticOnNhd`, or a source-faithful alternate encoding | all choices open |
| "analytic solution" | local existence, solution equation and initial condition, analyticity on an interval, and possibly uniqueness | `IsIntegralCurveAt` or interval derivative predicate plus analytic regularity | conclusion bundle and uniqueness scope open |
| Cauchy/Kovalevskaya, 1875 | historical identity | immutable primary edition, locator, assumption and proof map | no citation or passage supplied |
| ODE category | catalog scope guard | ODE rather than PDE types unless an approved correction says otherwise | conflicts with the usual historical PDE namesake |
| `已验证` | untrusted inventory metadata | no Lean declaration or proof object | explicitly rejected as H or M evidence |

## Modern ODE source lead inspected

Shane Kepley and Tianhao Zhang, *A constructive proof of the
Cauchy-Kovalevskaya theorem for ordinary differential equations*,
arXiv:`1912.03836v3` (15 December 2020), is an exact-topic ODE source lead.
The immutable PDF retrieved from `https://arxiv.org/pdf/1912.03836v3` has
SHA-256 `f5edbddab5f7a1da7591a82dca7c5a1038b5ca0fe96e8f326a2c4d3ddf4a9b36`.

Theorem 1 on PDF page 2 states that if `V` is an open subset of `R^n` and
`f : V -> R^n` is analytic, then the initial-value problem `x' = f(x)`,
`x(0) = x0 in V` has a unique solution analytic on some open interval
containing zero. Theorem 11 begins on PDF page 20 (its proof continues on page
21) and states the same named theorem after the constructive development. The
introduction explicitly distinguishes this ODE setting from the general PDE
theorem.

This is strong candidate-source evidence, but it does not prove that the
uncited 1875 catalog record intended this modern autonomous formulation.
Theorem 1 and Theorem 11 also differ in how explicitly they state the local
interval, and their incorporated definitions and proof dependencies have not
received independent review. The source therefore supports `H1`, not H0, and
does not authorize a canonical Lean target at intake.

## Historical source lead

The historical bibliographic candidate is Sophie von Kowalevsky, *Zur Theorie
der partiellen Differentialgleichung*, *Journal fuer die reine und angewandte
Mathematik* issue 80 (1875), pages 1-32, DOI
`10.1515/crll.1875.80.1`. Crossref confirms the title, date, journal, issue,
pages, and DOI. The publisher full text was blocked in this environment and was
not inspected. More importantly, it is a partial differential equation source,
so it cannot silently identify the repository's ODE target.

## Human-source boundary

The provisional `H1` classification records that complete published proofs
are known and a precise ODE candidate has been inspected, while the exact
catalog statement, assumptions, historical relationship, proof boundary,
errata, and source-to-Lean map remain unaudited. Before H0, an independent
qualified reviewer must approve an immutable source edition and pinpoint
theorem; transcribe every incorporated definition, binder, hypothesis,
conclusion, and boundary case; reconcile the ODE/PDE mismatch; inspect proof
dependencies and errata; and approve the row-by-row statement map.

## Lean boundary

The pinned environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740` with mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. `IntakeProbe.lean` checks only
the generic `IsIntegralCurveAt`, analytic, Picard-Lindelof, and Euclidean-space
surfaces. A bounded exact-topic search found no Cauchy-Kovalevskaya declaration
in the repository or pinned mathlib. `Mathlib/Analysis/ODE/PicardLindelof.lean`
does prove local Lipschitz ODE existence and finite/`C-infinity` regularity, but
line 555 explicitly records a TODO to extend the relevant Picard regularity
argument to the analytic case. This does not establish global absence or an
anchor-audit result, but it prevents crediting that module as the requested
analytic theorem at intake.

The canonical module, proposition, expression hash, environment fingerprint,
checked transports, and mutation certificate remain null. No source lead,
generic API, or TODO is proof credit. No H0, M0, R0, audit completion, theorem
completion, accepted receipt, or master acceptance is claimed.
