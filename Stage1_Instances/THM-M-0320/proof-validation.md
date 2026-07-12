# Proof-phase validation

Item: `S56-M-0320-PROOF`  
Base revision: `2eb836c21ebdba77082dcafd9222259988e44a54`

## Result

`Proof.lean` supplies a real proof body for frozen obligation `M0320-T-GRAPH`: on the closed
Euclidean domain, upper hemicontinuity and closed values imply that `CorrespondenceGraph K F` is
closed. The proof uses sequential closedness, coordinate convergence, mathlib's restriction
equivalence for upper hemicontinuity, and `UpperHemicontinuousAt.mem_of_tendsto`.

The proof phase is **blocked**, not self-tested as the assigned node. The frozen core obligation
`M0320-C-CORE` and its subtype integration `M0320-T-SUBTYPE` require the audited external
`harfe/fixed-point-theorems-lean4@11a9f041246d28374edae384241757f9a0cbd5e4` proof. That project is
not present in the pinned Lake dependency closure, targets different Lean/mathlib revisions, and
has no located license grant. The worker rules prohibit fetching or mutating `.lake`, and absent
license permission also prohibits truthful vendoring. Consequently no placeholder-free root proof
can be supplied in this clone, and no `.stage1-worker-selftest.json` is written.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0320/Proof.lean` | 0 | graph-bridge proof elaborated; `#print axioms` reported only `propext`, `Classical.choice`, and `Quot.sound` |
| `rg -n '\bsorry\b\|\badmit\b\|(^|[[:space:]])axiom[[:space:]]\|unsafe\|implemented_by' Stage1_Instances/THM-M-0320/Proof.lean` | 1 | expected no-match result: no placeholder, explicit axiom, unsafe declaration, or implementation override |

## Status boundary

This artifact closes only `M0320-T-GRAPH` at the local elaboration level. It does not close the
external Kakutani core, subtype integration, exact root, trust/replay gates, or theorem completion.
The assigned proof node remains blocked pending a license-compatible immutable dependency (or an
independent local Kakutani proof) and compatible local kernel integration.
