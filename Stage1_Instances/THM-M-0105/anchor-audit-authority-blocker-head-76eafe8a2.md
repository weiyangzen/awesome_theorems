# THM-M-0105 anchor-audit authority blocker

Item: `S56-M-0105-ANCHOR_AUDIT`

Worker base: `76eafe8a281129b49022878b685c5abf0c0e071c` (tree
`149043af61224fe5b06fec4e2da210e15b17e383`)

Claim order: `(v2_execution_rank=264, phase_layer=2,
S56-M-0105-ANCHOR_AUDIT)`

Verdict: `blocked`; proposed state remains `[ ]`.

## First failed gate

`G05-AUTHORITY-REPLAY`

The mandatory HEAD phase contract declares exactly two candidate paths for an
anchor-audit validator:

- `Stage1_Instances/THM-M-0105/check_anchor_audit.py`
- `Stage1_Instances/THM-M-0105/check_anchor.py`

Neither exists in the worker-base commit or working tree. The contract requires
exactly one candidate already present at the worker base, and the scheduler owns
both paths. This worker is expressly forbidden to create, refresh, rename,
replace, or delete a candidate. Therefore no lawful validator argv exists, no
`stage1-validator-semantic-result/1.0` object can be obtained, and command
success or an undeclared adapter cannot support a receipt or self-test.

Topology independently prevents master closure: predecessor
`S56-M-0105-STATEMENT` is still `[_]`, not master-accepted `[x]`.

## Dependency and reuse audit

The supplied `parent_inspection_order` is exactly empty. The complete empty
direct/transitive hard-parent closure was traversed once, in order, before any
proof work. No proof work was performed. There are no hard edges, reuse hints,
or shared groups, so no provider declaration, proof body, receipt, checkbox, or
acceptance was consumed or transferred.

The current theorem-DAG SHA-256 is
`39dc7ce5f668c527de899e74c99840aef50e6be4c576aaf146abed1b6749275c`;
the stable dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
The tracked schema-1.1 ledger has the required empty arrays, but it binds prior
graph `e8472863...`, revision `1cc6aa61...`, and the statement claim at phase
layer 1. A ledger-only refresh would not repair the absent immutable validator
and could not yield a lawful phase packet, so it was not presented as a
self-test.

## Bounded anchor observations

These are immutable, local guidance only. They are not a precommitted,
receipt-bound seven-lane inventory and do not claim phase completion or global
search saturation.

- The frozen target
  `Stage1Instances.THM_M_0105.RiemannRochTarget` in `Statement.lean` has
  expression SHA-256 `e69f2d70...15cb2`. It elaborates with its definitional
  expansion, but remains `M3`: no terminal Riemann-Roch body exists.
- The tracked legacy `S1_M_027.lean` (SHA-256 `c8a270f8...afe3`, Git blob
  `39c70776...2b1f`) elaborates statement shapes, support wrappers, metadata,
  and explicit blocker decisions. Its existential abstract divisor package is
  not the frozen universal target. Uniform L0 rework grants no proof or
  acceptance credit.
- Pinned mathlib is commit `8a178386...ea95`, tree `bdc39a31...5c2b`. Bounded
  source searches found schemes, smooth/proper/geometrically-integral
  predicates, modules and sheaf cohomology, function fields, Dedekind
  different/trace-dual, Euler characteristic, and elliptic-curve support. They
  found no algebraic-curve Riemann-Roch declaration or the combined
  Cartier/Weil divisor, canonical/dualizing divisor or sheaf, degree, and genus
  interface required for the root. This is `M3` substrate, not root closure.
- Tracked immutable audit metadata identifies
  `cguth7/roch-riemann-refactor@8e67e894...bf59` with Lean 4.27/mathlib
  `fe3134f0...ffa9`, declarations including `riemann_roch_from_euler` and
  `riemann_roch_full`, a failed external build, unavailable targeted axiom
  replay, custom axioms/placeholders, and conditional theorem-family inputs.
  Its source is not in this Lake closure and no exact checked transport exists;
  it remains `M5` with a concrete integration blocker.
- `vaca22/riemann-roch-function-fields@dbca5bee...0e82d` is a relevant
  function-field lead, but its bytes/trust closure are not locally available and
  no checked scheme/function-field transport exists. It remains `M5` guidance.
  The graph Riemann-Roch project is a material statement mismatch and likewise
  supplies no root credit.
- No content-bound statement-only or other-prover artifact is selected for the
  exact root. Network-denied replay cannot turn that into global absence.
- Hartshorne, *Algebraic Geometry* (1977), IV.1.3 remains a bibliographic lead,
  not H0: exact source bytes/page, incorporated definitions, assumption map,
  errata, arbitrary-field/geometric-integrality bridge, projective/proper
  convention, and independent review remain open.

The honest root boundary remains `M3` with zero proof credit. No candidate is
accepted as `M1` or `M0-L/W/P`.

## Checks run

All dependency use was read-only. No network request, Lake update/build,
dependency clone/fetch, checkout, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 structure and all 1546 uniform-L0 targets passed at the untouched base |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546-node v2 graph, typed contexts, and acyclicity passed |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | seven phase contracts, twelve common gates, and 23 source references passed |
| `python3 scripts/stage1_target.py check` | 0 | all 1546 ranked targets passed |
| `python3 scripts/stage1_target.py show THM-M-0105` | 0 | rank 27, planned, deep formalization debt, theorem incomplete |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --trust=0 ../../Stage1_Instances/THM-M-0105/Statement.lean` | 0 | frozen target and transport elaborated; expected mutation-cast failures printed; three sandbox stream-fd warnings were nonfatal |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --trust=0 AwesomeTheorems/Stage1/S1_M_027.lean` | 0 | legacy support/blocker module elaborated; no root body claimed |
| bounded pinned-mathlib exact-topic search | 0 | matches were repo-local Stage1 modules only; no pinned-mathlib terminal declaration was found |
| prohibited-construct scan of target-owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, `unsafe`, `implemented_by`, `native_decide`, or `proof_wanted` |
| post-edit `python3 Docs/tools/check_stage1_standard.py` | 1 | expected integration boundary: deterministic generation inventories the two new owned blocker files; this worker did not rewrite the authority projection |
| post-edit `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1 | same target evidence-inventory projection drift; master integration must regenerate the read-only projection |

## Retry condition

The scheduler must commit exactly one declared anchor-audit validator and issue
a fresh claim whose base contains that unchanged blob. After the statement
predecessor is master-accepted `[x]`, a fresh worker can precommit and execute
the complete seven-lane protocol, content-bind immutable external and negative
evidence, refresh the empty schema-1.1 dependency ledger for that graph/base,
produce exactly one `stage1-node-receipt/1.0`, and replay the unchanged validator
to exactly one typed semantic JSON result.

No anchor-audit receipt and no `.stage1-worker-selftest.json` are produced.
This target-scoped blocker does not satisfy the phase, transfer acceptance,
change H/M/R debt, prove the root, claim `AUDIT-Z` or `THEOREM-Z`, change task
state, or claim master acceptance.
