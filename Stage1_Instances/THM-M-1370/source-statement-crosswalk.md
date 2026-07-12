# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:9985-9990` supplies exactly the title
`Kolmogorov-Arnold theorem`, attribution to Andrey Kolmogorov and Vladimir Arnold, the year 1954,
the gloss `KAM理论的原始形式` (`the original form of KAM theory`), importance `high`, and status
`verified`. Git history places all six uncited fields in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:37263-37288` repeats the metadata but explicitly leaves the exact
definitions and premises, proof route, dependencies, equivalent forms, axiom policy,
machine-checked status, and artifact links open. The rev-5.6 target manifest preserves `verified`
only as untrusted metadata and resets this target to `L0 / rework_required`.

The catalog contains no bibliography, theorem or page locator, Hamiltonian, phase space, ordered
binders, hypotheses, conclusion, incorporated definitions, proof boundary, translation
provenance, correction record, or reviewer. Its gloss identifies a theorem family but does not
select one stable proposition.

## Historical source leads

A. N. Kolmogorov's 1954 note is commonly cataloged as *On the Preservation of Conditionally
Periodic Motions Under Small Variations of the Hamilton Function*, *Doklady Akademii Nauk SSSR*
98, no. 4, pages 527-530. Crossref exposes a later English reprint titled *Preservation of
conditionally periodic movements with small change in the Hamilton function*, pages 51-56 in
*Stochastic Behavior in Classical and Quantum Hamiltonian Systems*, DOI
`10.1007/BFb0021737`. These are strong bibliographic leads matching the catalog year and KAM gloss.
Neither locator has been admitted here as a lawful complete original edition with a verified
original-to-translation crosswalk, exact theorem passage, assumption map, correction audit, or
independent review.

V. I. Arnol'd's *Proof of a theorem of A. N. Kolmogorov on the invariance of quasi-periodic motions
under small perturbations of the Hamiltonian*, *Russian Mathematical Surveys* 18(5) (1963), pages
9-36, DOI `10.1070/RM1963v018n05ABEH004130`, is a later primary proof-source lead. Its title
supports the Arnold association while its 1963 publication exposes a material distinction from the
catalog's 1954 date. It may formulate or prove a different-strength contract from Kolmogorov's
announcement. No clause from it is silently merged into the 1954 root.

A Selected Works locator, DOI `10.1007/978-94-011-3030-1_52`, has useful title and page metadata but
Crossref attributes the chapter to V. M. Tikhomirov rather than Kolmogorov. That metadata conflict
must be resolved against the actual edition before it can support provenance. All three locators
remain discovery leads, not `H0` evidence.

## Component crosswalk

| Catalog component | Material interpretations | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "original form" | Kolmogorov's 1954 announcement, a later English translation, or Arnold's 1963 full proof/formulation | one source-versioned canonical proposition | edition and result not selected |
| Hamiltonian | analytic near-integrable Hamiltonian in action-angle coordinates, or another source-specific normal form | scalar function on an action-angle phase space plus derivatives | exact carrier and form absent |
| unperturbed system | integrable Hamiltonian depending only on actions | finite-dimensional action space and frequency map | domain and regularity absent |
| nondegeneracy | invertible Hessian, local frequency-map diffeomorphism, isoenergetic condition, or another twist hypothesis | derivative/Hessian and determinant or equivalence predicate | variant not selected |
| nonresonance | rational independence or a quantitative Diophantine inequality | quantified integer vectors, norm, constants, exponent | constants and convention absent |
| small perturbation | qualitative neighborhood or quantitative analytic-norm estimate | normed function space and explicit threshold | norm and dependency absent |
| retained motion | one invariant torus, a conjugate quasi-periodic flow, or a positive-measure Cantor family | embedding, invariance/conjugacy equation, frequency, measure | conclusion strength absent |
| Kolmogorov/Arnold | 1954 announcement versus later proof and reformulation | source provenance only | authorship/date relation unresolved |
| `verified` | untrusted inventory label | no Lean declaration or proof body | explicitly rejected as evidence |

## Name and neighboring-target boundary

The English title alone is unsafe: "Kolmogorov-Arnold theorem" can refer to the unrelated
representation/superposition theorem about continuous multivariable functions. The ODE category,
1954 date, KAM gloss, and adjacent KAM/Moser entries identify the intended subject as Hamiltonian
perturbation theory, so the representation theorem is excluded rather than adopted.

The adjacent mathematical target `THM-M-1369` is the broader KAM-theory entry; `THM-M-1371` is
Moser's twist theorem. A separate physics record states that most nonresonant tori remain under a
small perturbation, but it belongs to out-of-scope `THM-P-0774`. These records help expose variant
boundaries. They do not add hypotheses to this target or share status, source evidence, or proof
credit.

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake probe
checks `AnalyticAt`, the finite unit torus and its Fourier monomials, the canonical symplectic
matrix, an ODE integral-curve predicate, and flows. The repo-local legacy file for `THM-M-1547`
contains a conservative Liouville-Arnold interface whose invariant-torus and action-angle outputs
remain explicit proposition fields. Neither that interface nor the generic mathlib APIs state the
source-selected perturbation theorem.

A bounded case-insensitive search found no KAM or exact Hamiltonian quasi-periodic persistence
target in repo-local Lean or pinned mathlib. This is discovery only; it is not an exhaustive
external-project audit and cannot prove absence.

## Required source admission

The statement phase must preserve and hash one lawful complete edition, select an exact result and
proof boundary, transcribe every incorporated definition, ordered binder, hypothesis, conclusion,
constant dependency, and boundary case, reconcile the 1954/1963 and author/translator metadata,
audit translations and corrections, and obtain independent review. It must then freeze and
mutation-test the same exact Lean expression. Until then the canonical mathematical and Lean
targets remain null and the source classification remains `H1`.
