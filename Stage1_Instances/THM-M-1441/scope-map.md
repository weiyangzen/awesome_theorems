# Scope map

## Preserved repository scope

- Target ID and name: `THM-M-1441`, `割线法` (secant method).
- Literal purpose/rate gloss: `方程求根的超线性方法`.
- Attribution and period: many mathematicians, twentieth century, as catalog metadata only.
- Broad subject: numerical analysis and equation root finding.

The word `割线法` suggests a two-point divided-difference iteration, but the catalog itself neither
displays a recurrence nor asserts one precise convergence or correctness proposition. The spelling
`弦截法` in a neighboring dossier is treated as an unreviewed synonym, not a second source claim.

## Decisions required before statement freeze

An accountable source and scope review must freeze all of the following before a Lean target can be
selected:

- whether the equation is scalar, a system, or an equation in a more general space, followed by the
  domain/codomain, scalar field when applicable, function, and root;
- the exact recurrence, indexing convention, two starting values, and partial-versus-total handling
  of a zero divided-difference denominator;
- the root's simplicity or multiplicity, the required continuity/differentiability order, and which
  derivative values must be nonzero;
- the neighborhood, basin, invariance, separation, and noncollision conditions that make every
  iterate well-defined;
- whether convergence is assumed or proved, whether it is local or global, and which root is the
  limit;
- the meaning of superlinear convergence: Q-superlinear, R-superlinear, a general order `p > 1`, or
  the classical order equal to the golden ratio;
- the exact ratio, asymptotic, error, iteration-count, residual, stopping, or root-correctness
  conclusion and the uniformity of every constant;
- exact arithmetic versus floating-point arithmetic and the policy for overflow, cancellation,
  rounding, and termination.

No item in this list is decided merely because one formulation is familiar or convenient in Lean.

## Candidate theorem families not selected

- A recurrence well-definedness theorem for
  `x_(n+1) = x_n - f(x_n) * (x_n - x_(n-1)) / (f(x_n) - f(x_(n-1)))`.
- A local convergence theorem near a simple root under differentiability hypotheses.
- A Q-superlinear conclusion such as the next-error/current-error ratio tending to zero.
- An exact convergence-order theorem with order equal to `(1 + sqrt 5) / 2`, potentially requiring
  stronger derivative and nondegeneracy assumptions.
- A globalized or safeguarded hybrid method, regula falsi variant, error-bound theorem, or
  finite-precision algorithm-correctness theorem.

These are a proposition-choice ledger, not alternate encodings or credited results.

## Explicit exclusions

- `THM-M-1440` Newton iteration and its derivative-based quadratic convergence theorem.
- `THM-M-1442` bisection and its bracketing-based linear convergence theorem.
- `THM-M-1443` generic fixed-point iteration or `THM-M-1444` Banach fixed-point theorem used as a
  silent replacement for the two-point secant recurrence.
- A theorem that assumes the desired convergence, rate, root correctness, denominator safety, or
  error estimate as an opaque premise and then restates it.
- A constant/linear toy function, a finite sampled trajectory, a plot, or a floating-point
  experiment presented as a general method theorem.
- Pinned asymptotic, derivative, sequence, division, or golden-ratio APIs without a reviewed
  source-to-target mapping.
- The untrusted catalog label `已验证` as evidence of either a human proof or kernel closure.

## Degenerate and boundary scope

The statement phase must expressly handle equal initial points; an initial point already equal to a
root; equal function values at distinct iterates; zero secant slope; a multiple or absent root;
nondifferentiable functions; iterates leaving the function domain; convergence to an unintended
root; cycles and divergence; a zero asymptotic error denominator; and finite-precision stagnation.
No case is silently excluded at intake.

## Ownership and lifecycle boundary

Only `Stage1_Instances/THM-M-1441` is owned by this item. The dossier is `planned`, has no accepted
state, and exposes no proof body or canonical declaration. The master target manifest, generated
blueprint checklist, and execution DAG remain read-only authorities. The integration lane alone may
accept the provisional receipt or activate the statement phase.
