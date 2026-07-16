# THM-M-0570 statement blocker

Item: `S56-M-0570-STATEMENT`

Worker base: `1cc6aa61bb055a5c032297ee457905c849af7608`

Verdict: `blocked`; semantic self-test passed; `phase_accepted=false`

## First failed gate

`S02-EXACT-TARGET.primary_source_and_variant_selection`

The repository identifies only a proof method: "heat-kernel proof of the index theorem", glossed
as an Atiyah-Singer proof by heat-kernel methods. This does not select one proposition among the
McKean-Singer heat-supertrace identity, the general cohomological Atiyah-Singer formula, a
Dirac-type specialization, and a pointwise local index theorem. These variants differ in operator,
manifold, bundle, grading, coefficient, normalization, boundary, and conclusion choices.

The three candidate publications in `source-statement-crosswalk.md` remain discovery anchors. No
immutable edition, exact theorem/page and wording, incorporated definition chain, errata decision,
or independent source-fidelity approval selects the canonical claim. Choosing a variant here would
invent missing mathematics and violate the rev-5.6 exact-statement gate.

## Dependency and legacy boundary

The v2 theorem DAG declares an empty direct/transitive hard-parent closure, no reuse hint, and no
shared lemma group. `dependency-reuse-ledger.json` audits that complete empty context in claim order
`(329, 1, S56-M-0570-STATEMENT)`. It supplies no mathematical-independence or proof credit and does
not inherit acceptance. The intra-theorem intake predecessor remains worker-provisional `[_]`.

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_113.lean` elaborates, but its
`HeatKernelIndexData` stores unconstrained predicates and index functions, and its `StatementShape`
is explicitly an abstract candidate. It cannot determine the missing source identity or count as
an exact target. The contract-selected `Statement.lean` is consequently declaration-free and has
no imports. Its successful elaboration checks only this fail-closed boundary.

## Self-test evidence

All commands ran from the worker clone on 2026-07-17. The canonical `.lake` symlink and pinned
dependencies were used read-only; no update, build, clone, or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0570/check_statement.py` | 0 | exactly one `stage1-validator-semantic-result/1.0` object; `status=blocked`, `phase_accepted=false`, `phase_predicate_proven=false` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0570/Statement.lean)` | 0 | no output; declaration-free negative boundary elaborates |
| `(cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_113.lean)` | 0 | no output; legacy discovery module elaborates without receiving statement credit |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique uniform-L0 targets |
| `python3 scripts/stage1_target.py show THM-M-0570` | 0 | rank 113, planned, legacy evidence unaccepted, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0570 .stage1-worker-selftest.json` | 0 | no output |

After the new target-owned JSON was added, `check_stage1_theorem_dag_v2.py` and the aggregate
standard check truthfully report that the checked-in DAG differs from fresh deterministic
generation. The worker is forbidden to edit that projection; the integration lane must regenerate
it after integrating this packet. The broader acceptance-evidence unit suite also cannot exercise
its real bubblewrap tests in this managed worker because the host home is read-only and the
bubblewrap executable fails its ownership policy; the target validator does not use that bypass.

## Required unblock

An accountable reviewer must bind and independently approve one immutable primary-source theorem,
including exact wording and definitions, corrections, domains, ordered hypotheses, conclusion,
normalizations, and boundary cases. A later statement worker can then encode exactly that claim,
minimize imports, bind the expression and environment fingerprints, check credited transports, and
run all four required mutation classes.

This is a target-scoped, worker-self-tested blocker. It proposes only unfinished `[_]` handoff
evidence. It claims no exact statement, mutation pass, proof, audit completion, theorem completion,
transferred acceptance, or master acceptance.
