# THM-M-0113: Hodge decomposition theorem

## Intake status

`S56-M-0113-INTAKE` is a planned rev-5.6 instance. The canonical interpretation is the analytic/cohomological Hodge decomposition for compact Kahler manifolds, not algebraic Kahler differentials and not the Hodge conjecture.

The frozen human claim is: for every compact Kahler manifold `X` and degree `n`, `H^n(X; C)` is the internal direct sum of the pieces `H^{p,q}(X)` with `p + q = n`, and complex conjugation swaps the `(p,q)` and `(q,p)` pieces.

## Scope map

| Surface | In scope | Boundary |
|---|---|---|
| Space | finite-dimensional compact Kahler manifold | no claim for arbitrary complex, Hermitian, or noncompact manifolds |
| Cohomology | complex de Rham cohomology in every natural degree | integral and real refinements are not credited |
| Decomposition | internal direct sum by Hodge bidegree | algebraic `KaehlerDifferential` is only nearby infrastructure |
| Symmetry | conjugation exchanges bidegrees | polarization and hard Lefschetz are separate theorems |
| Analytic bridge | harmonic representatives/type decomposition may implement the result | no such bridge is yet formalized or credited |
| Degenerate cases | degree zero and vanishing out-of-range bidegrees remain included | definitions must not silently delete these cases |

## Source-statement crosswalk

| Source record | Source wording | Canonical field | Fidelity status |
|---|---|---|---|
| `Docs/researches/math_theorems.md`, entry “霍奇分解定理” | “Kähler流形的上同调分解”; Hodge; 1941; source status “已验证” | name, subject, broad cohomological decomposition | discovery metadata only (`E5`); it omits compactness, coefficients, bidegrees, and conjugation |
| `Docs/Stage1_Blueprint.md`, `S1-M-025 / THM-M-0113` | same broad claim; requests normalization and Lean audit | theorem identity, Lean backend, debt boundary | generated legacy discovery input; no proof or source credit |
| `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_025.lean` | explicitly selects analytic compact-Kahler cohomological decomposition and distinguishes algebraic differentials | scope choice and candidate statement vocabulary | legacy artifact only; not accepted by rev-5.6 and not used as machine closure |

No versioned primary mathematical source with edition, theorem/page, assumptions, and errata was found in the repository during intake. Consequently human-source debt remains open (at least `H3`), and the historical “已验证” label is not accepted as source or machine evidence. The later source-audit phase must establish a pinpoint primary-source crosswalk and independently review the exact statement.

## Open phase DAG

1. `S56-M-0113-STATEMENT`: define/select the analytic objects and elaborate the exact target with minimal pinned imports.
2. `S56-M-0113-ANCHOR_AUDIT`: audit primary sources, mathlib, and immutable external Lean candidates.
3. `S56-M-0113-OBLIGATION_TREE`: freeze semantic obligations and typed graphs before proof credit.
4. `S56-M-0113-PROOF`: implement or integrate exact proof bodies without placeholders.
5. `S56-M-0113-VALIDATION`: run kernel, trust, provenance, and hermetic checks.
6. `S56-M-0113-RELEASE`: reconcile evidence and obtain independent master acceptance.

## Validation receipt

See [`intake-receipt.json`](intake-receipt.json). Intake validation checks structured JSON, manifest identity, repository standards, and whitespace. It does not run Lean because this phase intentionally has no formal expression or proof claim.

## Status boundary

This dossier does not claim an elaborated statement, `H0`, any `M0` class, proof completion, audit completion, or theorem completion. Lifecycle remains `planned`; only the integration lane can accept the provisional worker result.
