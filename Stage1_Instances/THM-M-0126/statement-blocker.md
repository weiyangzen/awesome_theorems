# Statement gate blocker

Item: `S56-M-0126-STATEMENT`

Theorem: `THM-M-0126`
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The source record identifies only the topic "Shimura curve theorem" and the phrase "modular curve
over a quaternion algebra." It gives no primary source, theorem/page, base field, ramification or
indefiniteness assumptions, quaternion order, level, moduli functor, equivalence relation, or exact
conclusion. In particular it does not decide whether the target is representability, algebraicity,
properness/smoothness, complex uniformization, a canonical model, or another theorem customarily
called a Shimura-curve theorem.

Selecting any one of these inequivalent claims would invent missing mathematics and violate the
exact-statement gate. Therefore the ordered binders, hypotheses, conclusion, degenerate cases,
expression fingerprint, checked transports, and mutation tests required by section 5.1 of the
rev-5.6 standard cannot truthfully be produced. The legacy
`AwesomeTheorems.Stage1.S1_M_045.QuaternionicModuliStatementShape` does not cure this defect: its
order, level, functor, sheaf, and representation interfaces are explicitly lightweight locally
invented placeholders, and the intake crosswalk classifies it as discovery input rather than a
source-faithful formalization.

`StatementInfrastructure.lean` checks only the uncontroversial pinned API surface for a generic
quaternion algebra and schemes. It deliberately declares no canonical theorem, proof, axiom, or
proxy predicate.

## Current execution boundary

- Repository base revision: `307c34d30fc3763c82a944a142ae922b48ff18aa`.
- Execution date: 2026-07-17.
- Exact v2 claim key: `(279, 1, S56-M-0126-STATEMENT)`.
- Parent inspection order: empty; the graph declares no direct or transitive hard parent.
- Dependency graph SHA-256:
  `8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47`.
- Dependency context SHA-256:
  `068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
- Intake predecessor: `[_]`, not master accepted; it explicitly leaves the canonical claim null.
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- No parent body, receipt, checkbox state, or proof credit is reused.

## Validation evidence

Lean commands ran from `Formalizations/Lean` with the existing pinned `.lake` artifacts. No update,
fetch, clone, or build command was used.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0126/Statement.lean` | 0 | declaration-free contract source elaborated with empty stdout/stderr; this is a negative boundary, not an exact target |
| `lake env lean ../../Stage1_Instances/THM-M-0126/StatementInfrastructure.lean` | 0 | generic quaternion-algebra and scheme infrastructure elaborated; two expected `#check` types printed |
| `lake env lean AwesomeTheorems/Stage1/S1_M_045.lean` | 0 | legacy discovery artifact elaborated, including its candidate statement shape; this is not exact-statement credit |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum lean-toolchain lake-manifest.json` | 0 | hashes match the environment fingerprint above |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0126/check_statement.py` | 0 | exactly one typed semantic JSON object; status/verdict `blocked`, `phase_accepted=false`, `phase_predicate_proven=false` |
| `python3 Docs/tools/check_stage1_standard.py` (pre-edit) | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, v2 DAG, seven-phase contract, and execution skill passed |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` (pre-edit) | 0 | 1546 theorems, 10822 states, two hard edges, five reuse hints, 310 shared groups, acyclic |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` (post-edit) | 1 | expected inventory drift: new target-owned evidence is absent from the worker-read-only theorem DAG; scheduler regeneration is required |
| `python3 Docs/tools/check_stage1_standard.py` (post-edit) | 1 | propagates the same expected theorem-DAG inventory drift; no normative standard gate changed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0126` | 0 | rank 45, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0126` | 0 | no whitespace errors |

## Retry condition

The authoritative lane must select a primary source and pinpoint theorem, including every arithmetic
and moduli assumption and the exact conclusion. The statement phase can then encode that claim with
minimal pinned imports, compare it against (or reject) the legacy candidate, and run removed-
hypothesis, changed-domain, binder-scope, and boundary mutations.

Until that input exists, the positive statement predicate remains blocked at `M4`; statement
acceptance, audit completion, and theorem completion are false. The contract-selected validator and
all negative evidence are content-bound and self-tested, so the worker handoff may truthfully propose
unfinished `[_]`. Validator success confirms the blocker packet only and cannot imply
`phase_accepted` or transfer intake acceptance.
