# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10488-10493` supplies exactly the title `重整化理论`, the
attribution "many mathematicians," the period "twentieth century," the gloss
`动力系统的尺度变换`, importance "high," and status `已验证`. The complete six-line block has
SHA-256 `0bb268ed333f3f26043f5c53e0a31dc8b2a071b25236f4a1871d96f905463d5b`.
All six lines entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; they contain no citation or proposition.

`Docs/Stage0_Blueprint.md:39050-39075` repeats the gloss and explicitly leaves the background,
exact definitions and premises, proof route, dependencies, equivalent forms, axioms, machine
status, and artifact links open. Its generic tree and 100-step language is planning boilerplate,
not mathematical source evidence. The rev-5.6 manifest carries `已验证` only as
`source_status_untrusted` and resets this target to `L0 / rework_required`.

## Literal crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `重整化理论` | an umbrella research program with several operator and theorem families | no single `Prop` or declaration follows from a theory name | not a stable proposition |
| "dynamical systems" | interval, circle, complex, rational, polynomial-like, flow, or higher-dimensional dynamics | exact carrier, map class, structure, regularity, and combinatorial data | all open |
| "scale transformations" | iterate/restrict/return, then conjugate or normalize by a coordinate rescaling | a total typed operator, domains, return time, coordinate maps, normalization, and well-definedness | all open |
| "theory" | fixed points, hyperbolicity, bounds, convergence, rigidity, or universality | one exact truth-valued conclusion with ordered binders and hypotheses | no conclusion supplied |
| many mathematicians / twentieth century | a broad historical boundary | immutable source identity and theorem/page provenance | no author, edition, theorem, page, proof, or errata |
| `已验证` | untrusted inventory metadata | accepted human-source and Lean kernel receipts would be required | no H or M credit |

## Variant and neighboring-target boundary

Even within one-dimensional dynamics, defining a period-doubling renormalization operator is not
the same proposition as proving a fixed point exists; uniqueness, hyperbolicity, convergence, real
or complex bounds, rigidity, and universality are further distinct claims. Interval-map, analytic-
germ, and polynomial-like formulations also require nontrivial transports rather than a shared
name.

The repository immediately follows this entry with Feigenbaum universality, Lanford's proof, and
Lyubich's proof. That context suggests a one-dimensional or complex-dynamics topic, but it is
affirmative evidence against silently selecting one of those separately named roots. The preceding
McMullen entry and other complex-dynamics targets likewise do not identify this claim.

## Bibliographic discovery boundary

Publisher metadata identifies Mitchell J. Feigenbaum, "Quantitative universality for a class of
nonlinear transformations," *Journal of Statistical Physics* 19(1), 25-52 (1978), DOI
`10.1007/BF01020332`, and Curtis T. McMullen, *Complex Dynamics and Renormalization*, Princeton
University Press (1994/1995), DOI `10.1515/9781400882557`. These are materially different
bibliographic leads, not a source crosswalk accepted for this target. The catalog cites neither,
selects no theorem or page, and separately names Feigenbaum and McMullen-related entries. No
primary text, incorporated definitions, proof boundary, corrections, errata, immutable copy, or
independent review is frozen here, so neither lead receives H credit.

## Source gate

Before this target can leave `H5`, an accountable owner must approve a corrected truth-valued root,
preserve and hash an immutable primary source, identify an exact theorem and every incorporated
definition, transcribe all ordered binders, hypotheses, conclusion, normalization and exceptional
cases, inspect its proof dependencies and corrections or errata, and justify why the proposition
represents `THM-M-1436` rather than a neighboring target. A second qualified reviewer must approve
the source-to-canonical-statement mapping.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe
elaborates generic APIs including `Function.iterate_succ_apply`, `Function.Semiconj.iterate_right`,
`Function.IsFixedPt`, `Function.IsPeriodicPt`, `Homeomorph.trans`, and `ContinuousMap.comp`. A
bounded target-name search over repo-local and pinned-mathlib Lean sources found no dynamical
renormalization, Feigenbaum, unimodal-map, or quadratic-like-map declaration. The only relevant
English-token matches were unrelated analytic renormalizations of peak functions.

Generic iteration and change-of-coordinate ingredients neither define a renormalization operator
nor supply any candidate theorem. The canonical module, expression, expression hash, checked
transports, and statement mutations remain null. No H0, M0, readable-proof closure, audit
completion, or theorem completion is claimed.
