# Scope map

## Repository claim

The authoritative target metadata supplies the title `模型配方法`, the gloss `非标准分析的基础`,
Abraham Robinson, and 1966. It supplies no formula, theorem number, page, language, theory, model
class, embedding, or conclusion. The intake freezes those literal facts and the ambiguity itself;
it does not turn a subject label or historical significance claim into a theorem.

## Candidate mathematical families

One plausible reading of the title is the model-companion/model-completion method: for a
first-order theory `T`, characterize or construct a companion `T*`, often by equality of universal
consequences together with model completeness and an embedding property. Another plausible reading
of the gloss is a foundational nonstandard-analysis result, such as transfer, an ultrapower
construction, an elementary extension, or saturation. These have different binders, hypotheses,
and conclusions. They are discovery families only, not alternate formulations accepted by intake.

## Decisions required before statement freeze

- Select an immutable primary source, exact edition, theorem/page, wording, and errata disposition.
- Establish a defensible translation of `模型配方法` and reconcile it with the 1966 nonstandard-
  analysis gloss rather than treating either as authoritative mathematics.
- Fix the first-order language, theories, consistency assumptions, model classes, morphisms, and
  whether the result concerns companions, model completions, elementary extensions, transfer,
  ultrapowers, or saturation.
- Fix every cardinality, completeness, quantifier-elimination, amalgamation, embedding, and choice
  hypothesis, including binder order and universe levels.
- Specify the exact conclusion and its degenerate cases, including inconsistent or empty theories,
  empty model classes, finite structures, and principal filters where relevant.
- Freeze the foundation, classical-choice, computation, TCB, and minimal-import profiles before
  any statement or proof credit is considered.

## Explicit exclusions

- Model completeness (`THM-M-0671`) or Los's ultraproduct theorem (`THM-M-0673`) as substitutes.
- A generic transfer principle, compactness theorem, saturation theorem, or existence of an
  elementary extension chosen solely because mathlib already exposes a nearby API.
- A structure that assumes the desired companion, completion, embedding, transfer, or saturation
  property as a field.
- A special theory such as algebraically closed fields or dense linear orders unless the selected
  source theorem itself has exactly that scope.
- The untrusted `已验证` metadata label as human-source or machine-proof evidence.

No canonical Lean target is frozen by this intake. The statement phase must either map one inspected
source proposition to concrete model-theory interfaces or record a precise missing-API blocker.
