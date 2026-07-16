# Statement validation record

Item: `S56-M-0123-STATEMENT`  
Base revision: `6cff7bae0e4547cf9ad8b7abaae20d1abb9fe049`

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
transport, the empty hard-parent closure, the sole weak shared-module decision,
the graph/context digests, the pinned environment, and the artifact bindings.

## Commands and results

| Working directory | Command | Exit | Result |
|---|---|---:|---|
| repository root | `python3 scripts/stage1_target.py check` | 0 | 1546 unique uniform-L0 targets passed |
| repository root | `python3 scripts/stage1_target.py show THM-M-0123` | 0 | rank 42, planned, legacy evidence unaccepted, theorem incomplete |
| `Formalizations/Lean` | `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0123/Statement.lean` | 0 | exact target, three transports, four expected mutation rejections, explicit expression, and axiom reports elaborated |
| repository root | `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0123/check_statement.py` | 0 | unchanged scheduler validator emitted one typed `repair_required` JSON result because its worker-base contract pins the pre-integration `[ ]` cursor |
| repository root | `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0123/statement-head-selftest.py` | 0 | current HEAD claim order, unique immutable validator selection, weak-group decision, receipt, and worker packet agree |
| repository root | `git diff --check -- Stage1_Instances/THM-M-0123 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The repository structural and v2 theorem-DAG validators were also run. Both
truthfully return exit 1 because refreshing the owned receipt and ledger makes
the checked-in, read-only evidence inventory stale; workers are forbidden to
regenerate that authority projection. The target itself has no hard parent or
transitive ancestor. Its sole weak shared group co-mentions the Atlas Faltings
module with `THM-M-0122`; that member's current states, receipts, Lean bodies,
and reusable artifacts were inspected. It has no premise-free terminal theorem,
so the ledger records `not_applicable` and transfers no body, receipt, checkbox,
or acceptance credit. The scheduler must reconcile the derived inventory during
integration and replay both structural checks.

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
