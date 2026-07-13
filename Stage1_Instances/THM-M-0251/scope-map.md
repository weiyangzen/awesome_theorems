# THM-M-0251 scope map

## Frozen Intake Identity

| Field | Intake value | Boundary |
|---|---|---|
| Theorem ID | `THM-M-0251` | Exact manifest member, execution rank 1261 |
| Catalog title | `内函数-外函数分解` | Result-family label, not a binder-complete statement |
| Catalog gloss | `Hardy空间的内-外分解` | Does not choose one Hardy space or theorem variant |
| Attribution | Arne Beurling, 1949 | Uncited catalog metadata; not an accepted source locator |
| Category | analysis / complex analysis | Classification only |
| Lane | `hard_statement_first_partial_verification` | No proof or elevated assurance follows from the lane |
| Lifecycle | `planned` | No accepted task or proof state |
| Worker-proposed vector | `[H5, M4, R4]` | Catalog target is not stable; this does not refute standard mathematics |

## Candidate Mathematical Family

A common result in this family says that a nonzero analytic function in a Hardy class on the unit
disk can be expressed as a product of an inner factor and an outer factor, with a suitable
uniqueness statement. This sentence is orientation only. It is not the frozen claim because the
repository does not specify the following proposition-changing choices.

| Choice | Unresolved alternatives | Why it changes the target |
|---|---|---|
| Function class | `H^p`, `H^2`, `H^infinity`, Nevanlinna class, Smirnov class | Membership, norm, boundary, and proof premises differ |
| Exponent | finite positive `p`, range below one, `p = infinity`, fixed or quantified | Alters domains, structures, and conclusions |
| Analytic domain | unit disk, half-plane, general simply connected domain, several variables | Requires different carriers, boundaries, and transports |
| Function representation | analytic functions, radial/nontangential boundary values, a.e. classes | Changes equality and measurability semantics |
| Inner predicate | boundary norm one a.e., bounded analytic formulation, selected normalization | Requires precise boundary existence and measure |
| Outer predicate | exponential/integral representation, cyclicity, dense polynomial multiples | These formulations need nontrivial checked equivalences |
| Factor list | a single inner factor, or explicit Blaschke, singular-inner, and outer factors | Splits zeros and singular measure into different obligations |
| Existence and uniqueness | existence only, uniqueness up to a unimodular constant, normalized uniqueness | Changes the conclusion and required binders |
| Zero case | excluded, assigned a special factorization, or separate theorem | The standard nonzero theorem cannot silently cover zero |

No value in this table is selected by intake. Consequently the domain/universe record, ordered
binders, hypothesis list, exact conclusion, alternate encodings, checked transports, and excluded
degenerate cases remain open rather than fabricated.

## Eligibility Boundary For Later Selection

The later source audit must first determine which exact proposition, if any, the catalog intended.
An individual-function factorization, a canonical Blaschke/singular/outer factorization, and a
Beurling-style invariant-subspace result are distinct candidates; none is privileged by this
intake. The selected target must be justified by an approved source and catalog-identity
crosswalk, remain within the catalog's Hardy-space inner/outer subject, map every definition and
premise, and freeze all choices above. If no source-supported identity can be established, the
target must remain H5 or be redirected through an independently approved catalog correction.

## Non-Substitution Boundary

The following do not close or define this target:

- Beurling's invariant-subspace theorem selected solely because the catalog says Beurling/1949;
- the broad neighboring `THM-M-0250` Hardy-space topic;
- the neighboring `THM-M-0249` Mergelyan or `THM-M-0252` Corona targets;
- finite polynomial factorization or function-composition terminology involving inner and outer
  functions;
- one canonical factor or one boundary-norm lemma without a Hardy-space root and all selected
  factorization clauses;
- a record whose fields assume the desired factors, equality, or uniqueness;
- an experiment, numerical boundary sample, truncated product, or unchecked certificate;
- the catalog label `已验证`, a source title, theorem name, or passing infrastructure probe.

## Degenerate And Boundary Cases To Freeze

The exact source statement must decide at least:

1. zero versus nonzero input;
2. the complete exponent range, including endpoints;
3. analytic functions versus almost-everywhere boundary classes;
4. existence and mode of boundary limits;
5. zeros, repeated zeros, and boundary accumulation;
6. finite versus infinite Blaschke products and their convergence;
7. singular inner components and their measure conventions;
8. treatment of the zero function and outer-factor normalization at the origin;
9. literal equality versus equality of boundary representatives;
10. uniqueness modulo a unimodular constant versus a normalized unique pair.

## Pinned Lean Boundary

The intake probe checks `Complex.UnitDisc`, `AnalyticOnNhd`, `MeasureTheory.MemLp`, and the
canonical-factor declarations in `Mathlib.Analysis.Complex.CanonicalDecomposition` at pinned
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. The module's own TODO says that
canonical decomposition remains to be formulated. `MemLp` is generic ambient measure theory, not
a Hardy-space definition. A bounded exact-topic search located no Hardy-space inner/outer root in
repo-local Lean or pinned mathlib. These facts are intake discovery only, not an exhaustive anchor
audit or an absence proof.

## Retry Condition

Select a lawful immutable primary or authoritative source edition and a pinpoint proposition;
audit incorporated definitions, assumptions, proof boundary, corrections, and errata; reconcile
the catalog attribution and date; and obtain independent complex-analysis review. Then freeze a
binder-complete human claim and elaborate the exact Lean target with minimal pinned imports,
expression and environment fingerprints, checked alternate transports, and all four required
mutation classes.
