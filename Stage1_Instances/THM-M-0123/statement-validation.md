# Statement validation record

Item: `S56-M-0123-STATEMENT`  
Base revision: `2dc5a410b68eff806858fd6ed0cb33d57f6209f7`

## Frozen target

`Stage1Instances.THM_M_0123.MordellTarget` states the intake-selected form:
over every number field, the rational-section type of every smooth, proper,
geometrically connected relative curve whose geometric genus is at least two
is finite. Smoothness, relative dimension, properness, geometric base change,
scheme morphisms, structure-sheaf cohomology, and rational sections use
concrete pinned mathlib surfaces.

The pin exposes no native scheme-curve genus or K-linear finrank for
`H^1(X, O_X)`. The statement therefore uses the standard cohomological
characterization on the actual curve: the underlying additive group of
`H^1(X, O_X)` is additively equivalent to `K^n` for some `2 <= n`. This cannot
be satisfied by selecting an unrelated proposition or a stored natural-number
field. The missing checked comparison to the native K-linear/geometric genus
remains explicit M3 normalization debt; no proof of Mordell's conjecture is
present or credited.

## Import and mutation evidence

The source has eight narrow direct imports. Deleting each import in turn makes
an exact temporary copy fail elaboration at the feature that import supplies;
there is no aggregate `Mathlib` import or proof-bearing Faltings module.

Four separately elaborated propositions change one required dimension:
removing the genus hypothesis, dropping `NumberField`, changing the universal
curve binder to an existential binder, and permitting genus one. Lean rejects
each as a term of the canonical target with `#check_failure`, and
`check_statement.py` requires all five explicit expressions to be pairwise
distinct. It also checks the definitional expansion, the section/slice point
transport, the empty v2 dependency closure, the graph/context digests, the
pinned environment, and the artifact bindings.

## Commands and results

| Working directory | Command | Exit | Result |
|---|---|---:|---|
| repository root | `python3 scripts/stage1_target.py check` | 0 | 1546 unique uniform-L0 targets passed |
| repository root | `python3 scripts/stage1_target.py show THM-M-0123` | 0 | rank 42, planned, legacy evidence unaccepted, theorem incomplete |
| `Formalizations/Lean` | `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0123/Statement.lean` | 0 | exact target, three transports, four expected mutation rejections, explicit expression, and axiom reports elaborated |
| repository root | `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0123/check_statement.py` | 0 | exactly one semantic JSON result with `phase_accepted=true`; expression, source, output, dependency, and artifact bindings agreed |
| repository root | `git diff --check -- Stage1_Instances/THM-M-0123 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The repository structural validator was also run and truthfully returned exit
1: the checked-in v2 DAG differs from fresh deterministic generation because
the new worker-owned source and receipt appear in its derived evidence
inventory. Workers are forbidden to update that generated authority; the
integration lane must regenerate it atomically when it accepts this packet.
This expected integration delta does not alter the target's parent closure,
rank, dependency-context digest, or authoritative statement state.

The canonical explicit-expression SHA-256 is
`9fa3c7a0bff55098e7cc234793cb06ec1628e84e003ddb273a6dc47094f58dbd`;
the statement source SHA-256 is
`62c3d5936d64ed2225d239246ac8139663bc4f722f896625b94bb9a11e59ca8f`;
the complete canonical Lean-output SHA-256 is
`f57215dfa63c8993cf43abfd1a3bbe60715bdda3e635f2c4a9a8cf35591748a6`.

## Status boundary

This phase proposes only a worker-self-tested statement node. Intake and this
node still require dependency-ordered master acceptance. Source fidelity,
native-genus comparison, anchor provenance, obligations, proof, trust,
readability, validation, and release remain open. `audit_complete` and
`theorem_complete` are false.
