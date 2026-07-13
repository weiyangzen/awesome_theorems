# Source-statement crosswalk

## Repository record and provenance

`Docs/researches/math_theorems.md:3539-3544` supplies exactly the title `切比雪夫估计`, attribution
Pafnuty Chebyshev, year 1850, gloss `素数分布的上下界估计`, importance `高`, and status `已验证`.
All six uncited lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no formula, definition,
bibliographic work, edition, theorem or page, constants, threshold, assumptions, proof, correction
history, or formal artifact.

`Docs/Stage0_Blueprint.md:13217-13242` repeats those fields while explicitly leaving precise
definitions and premises, proof process, dependencies, equivalent forms, axioms, machine status,
and artifact links open. Its generic assertion that a closed result is known is planning metadata,
not source evidence. Rev-5.6 retains `已验证` only as `source_status_untrusted` and resets this target
to `L0 / rework_required`.

## Primary-source lead, not accepted H0 evidence

NUMDAM catalogs P. L. Tchebichef, *Memoire sur les nombres premiers*, *Journal de mathematiques
pures et appliquees*, first series, volume 17 (1852), pages 366-390. The article says it was
presented to the Imperial Academy of Saint Petersburg in 1850, reconciling the catalog year with
the later publication year. The preserved NUMDAM PDF observed during intake has SHA-256
`cb1534bcfbf7a2356af67532592ffa917ac8b5db7bf5c59b64a14af3476db796`.

The introduction defines the subject broadly: bounds for the sum of logarithms of primes below a
limit, consequences for intervals containing primes, and approximate prime counts with error
bounds. Later sections display multiple inequalities. This dossier has not selected and
independently reviewed one formula plus all incorporated definitions as the exact catalog root,
audited the French transcription and mathematical notation, mapped every premise and conclusion,
or completed a correction/errata search. The memoir is therefore a strong primary-source lead but
not accepted `H0` evidence.

## Component crosswalk

| Catalog component | Candidate mathematical meanings | Pinned Lean surface | Intake result |
|---|---|---|---|
| `prime distribution` | `pi(x)`, `theta(x)`, `psi(x)`, or a linked package | `Nat.primeCounting`, `Chebyshev.theta`, `Chebyshev.psi` | object choice open |
| `upper estimate` | explicit/eventual upper bound with source constants and threshold | `Chebyshev.theta_le_log4_mul_x`, `Chebyshev.psi_le`, `Chebyshev.psi_le_const_mul_self`, `Chebyshev.eventually_primeCounting_le` | adjacent checked APIs only; no root credit |
| `lower estimate` | positive linear lower bound or lower prime-counting estimate | no exact catalog-selected declaration located in the bounded search | open; pinned Chebyshev module records this as a TODO |
| `estimate` | exact inequalities, asymptotic comparison, Big-O, or Theta | real order and `Asymptotics` infrastructure through the imported module | relation and quantifiers open |
| argument | natural cutoff or real cutoff with `floor` | `Nat.primeCounting`; real `theta` and `psi` use a natural floor | domain and endpoint transport open |
| source year | presentation in 1850 versus publication in 1852 | not a Lean component | historical metadata reconciled provisionally, exact root still open |

## Pinned formal boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.NumberTheory.Chebyshev` defines `theta` and `psi`, proves explicit upper bounds, and relates
`theta` to prime counting. Its module documentation explicitly lists `Prove Chebyshev's lower
bound` as a TODO. `IntakeProbe.lean` elaborates the relevant definitions and upper-bound theorem
types. It declares no target theorem and provides no evidence that the catalog's unidentified
two-sided statement is closed.

The search performed here is deliberately bounded intake discovery, not the downstream exhaustive
anchor audit. Repo-local legacy files concerning the explicit formula or Riemann hypothesis are
different targets and transfer no statement identity, proof body, or status.

## Fidelity boundary

Choosing a conventional pair of bounds from memory would manufacture constants, thresholds,
domains, binders, and a conclusion absent from the repository record. Until an immutable exact
source proposition and its definitions are selected, mapped, and independently reviewed, the
received target remains provisionally `H5`, the canonical statement remains null, and no source or
formal candidate receives closure credit.
