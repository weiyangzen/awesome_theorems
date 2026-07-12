# THM-M-1522 rev-5.6 dossier

This is the `planned` dossier for the Birkhoff pointwise ergodic theorem. The Stage0 slogan
"time average equals space average" is frozen here as the standard ergodic probability-space
specialization, not as an unconditional identity.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Almost-everywhere convergence of orbit Cesaro averages to `integral f dmu` | Only for an integrable real-valued observable on an ergodic measure-preserving probability system |
| General theorem | Limit identified with conditional expectation on the invariant sigma-algebra | A required source/formal bridge, but not silently substituted for the root |
| Definitions | Iterates, finite sums, normalization, measure preservation, ergodicity, integrability, almost-everywhere convergence | Exact mathlib representations and ordered binders remain open |
| Boundary probes | Constant observables, identity map, non-ergodic invariant components, non-integrable observables | Used to test that no hypothesis or qualifier is accidentally erased |
| Machine surface | Lean 4 plus pinned mathlib measure theory, conditional expectation, and dynamics APIs | No module or declaration is credited before the anchor and statement phases |
| Human source | Birkhoff's 1931 pointwise theorem and a modern exact formulation | Pinpoint premise/notation/errata review is incomplete |

The initial architecture is: define the dynamical system and averages; obtain the general
pointwise limit; identify it as invariant conditional expectation; use ergodicity and probability
normalization to make that expectation the constant space integral. This is a scope map, not a
frozen obligation registry or proof tree.

## Statement phase

The intake-selected proposition is now frozen and kernel-elaborated as
`Stage1Instances.THM_M_1522.BirkhoffPointwiseErgodicTarget` in `Statement.lean`. It fixes the
real codomain, probability normalization, mathlib's `Ergodic` predicate, integrability, the
`birkhoffAverage` convention, the almost-everywhere qualifier, and the integral limit. A checked
definitional transport expands the average into its finite orbit sum. Four expression-level
mutations distinguish removed or changed premises and quantifiers.

This completes only the provisional statement deliverable. No pointwise convergence proof or
legacy mean-ergodic wrapper is credited, and master acceptance remains pending.

## Intake verdict

Lifecycle remains `planned`, with provisional root vector `[H1, M3, R3]`. The former exact-statement
blocker now has locally self-tested evidence. The next dependent gate is the formal-anchor audit;
all theorem-completion gates remain open. The theorem is not complete.

## Validation

The intake commands remain in `validation.md`; exact statement commands and results are recorded
in `statement-validation.md`.
