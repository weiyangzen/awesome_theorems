# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:9796-9801` supplies exactly the title `李雅普诺夫直接法`,
attribution to Aleksandr Lyapunov, the year 1892, the gloss `李雅普诺夫函数的稳定性判据`,
importance "high", and status `已验证`. Git history attributes all six uncited lines to repository
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The entry contains no equation, definition,
binder, hypothesis, conclusion, bibliography, source edition, theorem or page locator, proof
boundary, correction record, or formal artifact.

`Docs/Stage0_Blueprint.md:36534-36559` repeats the gloss while explicitly leaving exact definitions
and premises, proof process, dependencies, equivalent formulations, axioms, machine status, and
artifact links open. The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted` and
resets the target to `L0 / rework_required`.

An adjacent catalog record, `Docs/researches/physics_theorems.md:6801-6807`, says "use a Lyapunov
function to determine stability of an equilibrium." It corroborates only the broad topic. It has no
source locator or exact proposition and belongs to distinct target `THM-P-0796`, so it is neither
the authoritative source nor a substitute for `THM-M-1343`.

## Component crosswalk

| Repository element | Possible mathematical component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "direct method" | infer stability without solving or linearizing the system, using a scalar auxiliary function | definitions over solutions or integral curves | theorem-family label only |
| "Lyapunov function" | continuous or differentiable `V`, often positive near the stability object | a function to an ordered scalar space plus `ContinuousAt`, `HasFDerivAt`, or source-selected alternatives | domain, codomain, regularity, and positivity condition absent |
| "criterion" | hypotheses on `V` and its change along trajectories | derivative paired with a vector field, derivative along `IsIntegralCurveOn`, or another checked encoding | orbital derivative and solution model absent |
| "stability" | Lyapunov, uniform, asymptotic, exponential, local, or global stability | a future exact stability predicate with quantified solutions, times, and neighborhoods | conclusion not selected |
| Aleksandr Lyapunov / 1892 | historical attribution | provenance metadata only | not an edition, theorem/page locator, or reviewed source |
| `已验证` | untrusted catalog status | no Lean declaration or proof object | explicitly rejected as evidence |

## Proposition boundaries

Weak nonincrease of a positive-definite Lyapunov function, strict decay, and properness or radial
unboundedness are not interchangeable premises. Nor are Lyapunov stability, asymptotic stability,
and global asymptotic stability interchangeable conclusions. A statement also changes when it
switches between autonomous and nonautonomous systems, equilibria and invariant sets, finite- and
infinite-dimensional spaces, or local and global solution existence. The source chooses none of
these options, so intake cannot truthfully fill ordered binders, hypotheses, or a conclusion.

The neighboring math records are material scope boundaries: `THM-M-1342` covers general Lyapunov
stability theory and `THM-M-1344` covers the indirect or linearization method. This intake borrows
no source or proof credit from either.

## Source and Lean boundary

No primary or authoritative theorem source is identified at intake. The statement phase must
select and preserve an immutable source edition, record a stable identifier and exact
definition/theorem/section/page locator, transcribe all premises and the complete conclusion, audit
dependent definitions and errata, reconcile neighbor scope, and obtain independent source review.
Only then may it freeze universes, ordered binders, boundary cases, minimal pinned imports, an
elaborated expression and environment fingerprint, checked alternate transports, and mutation
tests.

The provisional human-source status is `H5`: the supplied catalog wording is not one stable
proposition. This does not claim that standard Lyapunov direct-method theorems are false or
mathematically open. It records that selecting one without an accountable source decision would
broaden or substitute the target. The required target decision is to redirect this theorem-family
label to a corrected, source-selected exact direct-method proposition before ordinary statement or
proof execution.

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake probe
checks integral-curve, derivative, continuity, and convergence APIs. A bounded local search found
no obvious named Lyapunov direct-method theorem under the searched terms. These facts are
feasibility inputs only, not the later exhaustive formal-candidate audit, an absence claim about
external projects, or exact-statement/proof evidence.
