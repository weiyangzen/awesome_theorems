# Source-statement crosswalk

| Claim component | Repository source | Primary-source discovery anchor | Lean target | Intake assessment |
|---|---|---|---|---|
| Root | `Docs/Stage0_Blueprint.md`: `鞅的几乎必然收敛` | J. L. Doob, *Stochastic Processes*, Wiley, 1953, Chapter VII (martingale convergence results) | unresolved | The repository phrase is a topic-level gloss, not an exact theorem |
| Time and value domain | omitted | Doob's classical discrete-parameter real-valued setting is a candidate | candidate `Nat`-indexed real process | Must not silently exclude continuous time or extended-real limits |
| Convergence-enabling premise | omitted | Classical variants use an `L¹`/positive-part bound, nonnegativity, or uniform integrability | unresolved | Essential: an arbitrary martingale need not converge almost surely |
| Process premise | only "martingale" | filtration, adaptedness, measurability, and integrability are definitional/source premises | unresolved | Binder order and API representation await statement work |
| Conclusion | "almost surely converges" | classical results distinguish finite a.s. limits, integrability, and `L¹` convergence | unresolved | Limit codomain and any integrability claim must be sourced explicitly |

The date `1953` and attribution to Joseph Doob in Stage0 point toward Doob's monograph, but neither
a theorem number/page nor an edition scan/hash is present. Consequently this intake does not assign
`H0`, does not pretend that the two candidate readings are equivalent, and does not nominate a
mathlib declaration before the source claim is fixed.

Required source-resolution work for the statement phase:

1. Obtain a stable edition or scan of Doob (1953), record file/edition identity, exact theorem and
   pages, all definitions and assumptions incorporated by reference, and relevant errata.
2. Decide whether the intended root is the bounded submartingale theorem, the nonnegative
   supermartingale corollary, or another explicitly quoted theorem.
3. Transcribe the selected theorem with ordered binders and boundary cases, then independently
   review the transcription before Lean elaboration.
4. Only afterward audit mathlib declarations and prove checked transports for alternate encodings.

Discovery identifier (not an immutable evidence receipt): Doob, *Stochastic Processes*, Wiley,
1953, WorldCat OCLC 180133.

