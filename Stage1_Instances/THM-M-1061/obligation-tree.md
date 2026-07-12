# THM-M-1061 frozen obligation tree

Registry version 1 freezes 15 semantic obligations before proof-phase closure
inspection. Proof edges are reciprocal `proof_requires`/`composes` pairs;
refinement, provenance, evidence, trust, documentation, and workflow edges live
in separate graphs in `typed-graphs.json`.

## M1061-ROOT
Exact bounded-continuous Varadhan integral lemma. Open at M3.

## M1061-S-DEFINITIONS
Frozen elaborated LDP, good-rate, logarithmic-integral, and ambient interfaces.

## M1061-S-BOUNDARIES
Positive vanishing speed, nonempty domain, bounded test function, and extended
value behavior.

## M1061-S-FOUNDATION
Classical, noncomputable, import, axiom, and TCB audit boundary.

## M1061-N-VARIATIONAL
Normalization of the EReal supremum and finite approximation behavior.

## M1061-L-LOWER-LOCAL
Neighborhood localization using continuity and the open-set LDP lower bound.

## M1061-T-LOWER
Global liminf lower bound after passage to the variational supremum.

## M1061-C-COMPACT-COVER
Finite-cover construction on compact finite rate sublevels.

## M1061-L-CORE-UPPER
Closed-set LDP bound for the compact core and finite maximum.

## M1061-L-TAIL-UPPER
Bounded-function tail estimate outside a large rate sublevel.

## M1061-T-UPPER
Global limsup upper bound after core/tail assembly and truncation removal.

## M1061-T-LIMIT-MERGE
EReal liminf/limsup merge into the exact `Tendsto` conclusion. This is the
remaining root cut set and has no proof body.

## M1061-T-ROOT-TRANSPORT
Lean-checked conditional identity transport from the exact terminal package.

## M1061-X-SOURCE
Primary-source premise and inference crosswalk, without machine proof credit.

## M1061-X-PROVENANCE
Terminal-body, wrapper, import, trust, and replay overlay, without duplicate
semantic credit.

Status boundary: this artifact freezes architecture and checks only a
conditional terminal-to-root composition. It does not prove Varadhan's lemma,
close the root, establish H0/R0, or satisfy validation or release gates.
