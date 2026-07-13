# THM-M-0857 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Petersen's theorem. The repository
gloss is `三次桥less图有完美匹配`: a bridgeless cubic graph has a perfect matching. It attributes
the result to Julius Petersen in 1891 and labels it verified. Under rev-5.6, that label is untrusted
inventory metadata, not a source audit, an exact Lean proposition, or proof evidence.

The inspected primary source is Julius Petersen, *Die Theorie der regulären graphs*, *Acta
Mathematica* 15 (1891), 193-220. A CC0 scan from Zenodo record 2304433 was checked at SHA-256
`8762abd5e2f1fb3edcd1917b4db3b0c213a75d4ecfe026829b58e2e7913cca8c`. Petersen's definitions
explicitly permit parallel lines. Printed pages 210 and 218-219 give the historical route from
bridge-separated "leaves" and primitive cubic graphs to a degree-one factor. This is a strong
primary-source lead for the modern theorem, but the translation of Petersen's connected multigraph
language to the catalog's terse wording has not received an independent assumptions, definitions,
proof, or errata review. It is therefore `H1`, not `H0`.

Pinned mathlib supplies simple-graph predicates for regular degree, bridges, edge connectivity, and
perfect matchings, as well as Tutte's theorem. `IntakeProbe.lean` authenticates those interfaces.
A bounded repository and pinned-mathlib search found no declaration closing Petersen's theorem.
The APIs and Tutte reduction are usable formal substrate (`M3`), not an exact target or proof body.

The catalog does not say finite or infinite, connected or componentwise, simple graph or
multigraph, how degree counts parallel edges, or how bridgelessness and perfect matching are
encoded. Intake therefore does not silently freeze the convenient finite `SimpleGraph` statement.
`instance.json` records the scope authority and `task-dag.json` keeps all six downstream phases
open. The provisional vector is `[H1, M3, R4]`. No canonical statement, H0, M0, R0, accepted proof
state, audit completion, theorem completion, or master acceptance is claimed.
