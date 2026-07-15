# THM-M-0729 proof blocker at `d6616cc6` (slot60)

Item: `S56-M-0729-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T17:43:55+08:00`

Base revision: `d6616cc60ad980c635f22ef840e9c5db2ebcab50`

Base tree: `d6f3c3aedec26191f09878fd6eb1fec666adf318`

## Verdict

`blocked`. No eligible placeholder-free Lean 4 proof body was implemented or found for the exact
root `Stage1Instances.THM_M_0729.PCPTheorem`. The proof item stays `[ ]`; lifecycle stays `planned`;
the root vector stays `[H3, M3, R4]`; audit completion and theorem completion stay false.

The checked `root_of_directionalPackage` theorem is conditional assembly. Its premise already
contains both complete language-class inclusions and therefore proves neither. Definition-level
inspection and a disposable simplification attempt found no inconsistency, vacuity, definitional
shortcut, or model collapse; the attempt left the two expected existential inclusion goals open.

The immediate machine root cut remains:

- `M0729-D-NP-PCP`: constraint normalization, robust gap, PCP composition, randomness/query
  accounting, perfect completeness, and exact soundness-half transport;
- `M0729-D-PCP-NP`: finite oracle-bit certificates, exhaustive random-string verification with a
  polynomial-time machine proof, and the finite below-threshold branch.

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` has supporting
Turing-machine, finite-cardinality, polynomial, and logarithm APIs but no NP/PCP development or
terminal PCP theorem. Even `Turing.TM2ComputableInPolyTime.comp` is only a source `proof_wanted`
marker at `Computable.lean:284`, not an importable declaration. Repository history contains only
this target's statement, conditional obligation composition, and blocker probe, never a proof.
The latest integrated external audit found only a differently typed Atlas Gap-3SAT claim ending in
`sorry` behind an `opaque` reduction predicate, so it is ineligible.

## Required Split

This target already contained thirteen integrated proof-blocker/recheck JSON packets before this
run. Blueprint section 10.2 and the execution skill mandate a split after five unresolved ticks.
The integration lane should stop assigning the monolithic proof item and create dependency-legal
children for `M0729-D-NP-PCP` and `M0729-D-PCP-NP`, further divided by the ten frozen packages in
the paired JSON artifact. This worker did not edit the authoritative DAG or generated checklist.

The required predecessor `S56-M-0729-OBLIGATION_TREE` is also only provisional `[_]`, not master
accepted. That independently prevents proof-node master acceptance.

## Validation

All commands ran in this worker clone. The pre-existing untracked `Formalizations/Lean/.lake`
symlink points to canonical pinned artifacts and was reused read-only. No `lake update`, `lake
build`, dependency clone/fetch/checkout, network request, or `.lake` mutation was performed. Lean
outputs were confined to a disposable directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed all 15 assurance groups and 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0729` | 0 | Rank 766; `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0729/check_statement.py` | 0 | Exact expression hash `2a3d6c88...7bbc5`; all four weakened mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-0729/check_anchor_audit.py` | 0 | Immutable pins and source hashes agreed; no exact root candidate is claimed; root remains M3. |
| `python3 Stage1_Instances/THM-M-0729/check_obligation_tree.py` | 0 | Passed 19 obligations and 76 typed edges; both directional packages remain open. |
| Bounded `lake env lean ../../Stage1_Instances/THM-M-0729/Statement.lean` | 0 | Printed the exact `PCPTheorem` expression. |
| Direct `lake env lean` on `ProofBlockerProbe.lean` | 1 | The target-local `Statement` module was not staged in Lake's search path; the staged replay below is the real probe validation. |
| Disposable three-module immutable Lean 4.29.0 `--trust=0 -t0` replay | 0 | Exact statement, conditional assembly, and blocker probe elaborated; axioms were exactly `propext`, `Classical.choice`, and `Quot.sound`; polynomial-time composition remained unavailable as expected. |
| Scoped repository, history, and pinned-package PCP searches | 0/1 expected | No terminal inclusion/root body or pinned PCP development was found; history contains only this target's statement/obligation/probe commits. |
| `rg -n 'proof_wanted TM2ComputableInPolyTime.comp' .../Computable.lean` | 0 | Pinned mathlib records only the discarded marker at line 284. |
| Parser-oriented prohibited-device scan of checked local Lean files | 1 expected | No `sorry`, `admit`, `sorryAx`, bodyless declaration, unsafe/oracle device, `native_decide`, or `implemented_by` occurs. |
| Frozen-input and executable digest checks | 0 | Statement, composition, audit, registry, graph, validation, toolchain, manifest, target manifest, skill, probe, and Lean executable match the paired JSON. |
| Scoped diff from original blocker integration `9864b47f` | 0 | Only the check-only blocker probe was later added; no frozen proof input or pin changed. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test is absent because the proof phase is incomplete. |

The successful trust-zero replay copied `Statement.lean`, `ObligationTree.lean`, and
`ProofBlockerProbe.lean` to a `mktemp` directory, assembled `LEAN_PATH` only from the existing pinned
package build directories, ran the immutable Lean 4.29.0 binary in dependency order, and removed
the directory. The paired JSON records exact command results and hashes.

## Reopen Condition

After the required split, implement both frozen directional packages and their reduction,
resource, certificate, enumeration, and boundary dependencies without placeholders. Alternatively,
integrate an immutable, license-compatible Lean 4 terminal proof of the exact target with complete
dependency and terminal-body provenance, then rerun exact-type, trust, placeholder, provenance, and
composition checks.

This is current-base nonrelease blocker evidence, not a proof receipt. It does not satisfy
`S56-M-0729-PROOF`, promote scheduler state, close an obligation or the root, or claim audit
completion, validation, release, theorem completion, receipt acceptance, or master acceptance.
Because the assigned phase is not genuinely self-tested complete, `.stage1-worker-selftest.json`
remains absent.
