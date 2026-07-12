# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:10397-10402` supplies exactly the title `耦合方法`, the
attribution `众多数学家`, the period `20世纪`, the gloss `随机系统的同步`, importance "high," and
status `已验证`. All six lines were introduced by repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, stable source
ID, formula, definition, theorem statement, or proof.

`Docs/Stage0_Blueprint.md:38699-38724` repeats these fields and explicitly leaves the exact
definitions and premises, proof process, dependencies, equivalent forms, axioms, machine status,
and artifact links open. Its generic closed-result and leaf-audit wording is generated planning
metadata, not source evidence. The rev-5.6 manifest carries `已验证` only as
`source_status_untrusted` and resets this target to `L0 / rework_required`.

## Crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `耦合方法` | a technique or a family of joint constructions | no single `Prop` follows from a method name | not a stable proposition |
| "random system" | Markov process/kernel, random map/flow/cocycle, or stochastic equation | probability/noise and state types, time, measurable/topological structures, dynamics, initial data | all open |
| "coupling" | joint law/process with marginals, common noise, co-adapted or successful coupling | product law or joint process, marginal equations, measurability, adaptedness, coupling construction | meaning open |
| "synchronization" | finite coalescence, distance convergence, common random point, or singleton attractor | equality or convergence predicate, metric/filter, convergence mode/rate, initial-state and null-set quantifiers | all open |
| `众多数学家` / `20世纪` | generic historical metadata | source provenance only | no author, work, edition, theorem/page, assumptions, proof, or errata |
| `已验证` | untrusted inventory metadata | inspectable source proof and kernel receipt would be required | no H or M credit |

## Variant and neighbor boundary

A probability coupling with correct marginals does not by itself make two trajectories meet. A
synchronous/common-noise coupling need not coalesce, while a successful coupling may be defined by
a finite coupling time. `dist (X_t) (Y_t) -> 0` is weaker than eventual equality and may hold almost
surely, in probability, or in expectation. Equality in distribution says nothing about samplewise
synchronization. Pairwise convergence with a null set depending on the initial pair is also not the
same as a single random point attracting all initial states.

The adjacent repository roots `THM-M-1424`, `THM-M-1425`, and `THM-M-1426` separately own random
dynamical systems, random attractors, and multivalued random dynamical systems. Markov-chain
mixing, coupling inequalities, order-preserving synchronization, Lyapunov-based synchronization,
and coalescing flows are possible theorem families, not interchangeable readings of this root.
Skorokhod representation (`THM-M-1010`), Komlos-Major-Tusnady approximation (`THM-M-1065`), and
McCann optimal transport (`THM-M-1186`) also own distinct coupling-related conclusions.

## Bibliographic ambiguity witness

One credible but nonselecting example is Franco Flandoli, Benjamin Gess, and Michael Scheutzow,
"Synchronization by noise for order-preserving random dynamical systems," *The Annals of
Probability* 45(2), 2017, DOI `10.1214/16-AOP1088`, author manuscript arXiv
`1503.08737v2`. The inspected manuscript's Theorem 2.6 assumes an order-preserving strongly mixing
random dynamical system on a partially ordered Polish space plus interval concentration of its
limit distribution, and concludes convergence in probability to an invariant random point. The
paper explicitly distinguishes this weak synchronization from stronger synchronization.

This is evidence that the received phrase admits a precise, highly assumption-dependent reading;
it is not evidence that the repository intended Theorem 2.6. The catalog attributes no particular
work, names a coupling *method* rather than this theorem, and provides no cross-reference.
Accordingly this candidate receives no H status, canonical-statement selection, or proof credit.

Two further inspected sources pull in different directions. The same authors' *Synchronization by
noise* (DOI `10.1007/s00440-016-0716-2`, arXiv `1411.1340v2`, Theorems 2.14 and 2.23) gives
different singleton-attractor criteria and does not state a coupling-method theorem. Hairer,
Mattingly, and Scheutzow's *Asymptotic coupling and a general form of Harris' theorem with
applications to stochastic delay equations* (DOI `10.1007/s00440-009-0250-6`, arXiv
`0902.4495v2`, Theorem 1.1) is genuinely about joint path-law couplings but concludes equality of
ergodic invariant measures, not random-attractor synchronization. These incompatible nearby
readings strengthen the ambiguity finding; none is selected or credited.

## Source gate

Before an approved correction can leave `H5`, an accountable reviewer must identify and preserve
an immutable primary or authoritative source; select one exact truth-valued passage and
page/section; transcribe every definition, ordered binder, hypothesis, conclusion, convergence
mode, exceptional set, and boundary case; check corrections and errata; and justify why that
proposition represents `THM-M-1423` rather than a neighboring target. A second reviewer must
approve the source-to-canonical-statement mapping.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, bounded source-name
searches found no declaration for random-system synchronization or probabilistic coupling under
those names. Pinned APIs do include `ProbabilityTheory.Kernel`, kernel composition and powers,
`ProbabilityTheory.IsMarkovKernel`, `ProbabilityTheory.IdentDistrib`, product-measure marginals,
`Filter.Tendsto`, and `dist`; `IntakeProbe.lean` verifies representative names. Unrelated geometric
"coupling" terminology in Gromov-Hausdorff modules is not a candidate for this target.

The canonical module, declaration or expression, elaborated expression hash, checked transports,
and statement mutations remain null. No H0, M0, or readable-proof closure is claimed.
