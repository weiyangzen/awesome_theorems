# THM-M-1115 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for the configuration model. The repository source
says only "a random graph with a prescribed degree sequence." That is the name and purpose of a
model, not a theorem with a determinate conclusion. The intake preserves this ambiguity instead of
substituting a convenient degree-preservation or asymptotic statement. The metadata label
`已验证` is untrusted discovery input and gives no proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Input data | finite vertices and a prescribed natural-number degree function | labels, order conventions, and whether a family varies asymptotically remain open |
| Feasibility | an even total number of half-edges permits pairings | parity is necessary for the construction; graphicality is not required for a multigraph but matters for simple-graph claims |
| Sample space | labelled half-edges partitioned by vertex and perfect matchings of all half-edges | the source does not specify whether pairings or resulting multigraphs carry the uniform measure |
| Graph output | contract paired half-edges to a multigraph with the prescribed degrees | loops and parallel edges occur unless a simple event or conditioning is selected explicitly |
| Candidate elementary result | every paired construction has the prescribed multigraph degrees | this is a possible invariant, not accepted as the intended root theorem |
| Candidate probabilistic result | probability of simplicity, conditioning, enumeration, or an asymptotic property | no observable, hypotheses, limiting regime, or conclusion is supplied by the source |
| Formal system | Lean 4 and repository-pinned mathlib | no exact expression, module, declaration, or kernel evidence is credited at intake |

The provisional architecture has data, half-edge, pairing, multigraph-quotient, degree-invariant,
simple-event, and root-conclusion nodes. These are scope nodes only, not a frozen obligation registry
and not proof credit.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M4, R3]`. The first failed theorem gate is
exact-statement identity. A primary 1980 Bollobas paper for the regular-graph pairing method has been
bibliographically identified, but it cannot by itself choose an arbitrary-degree theorem or supply
the missing conclusion. The statement phase must inspect a pinpoint primary statement, select one
exact claim, and reject the other variants before elaborating Lean.

Exact intake checks and their limits are recorded in `validation.md`. Master acceptance and every
dependent theorem gate remain open; the theorem is not complete.
