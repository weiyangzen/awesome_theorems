# THM-M-0729 proof blocker at `29a69c34` (slot56)

Item: `S56-M-0729-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T14:41:26+08:00`

Base revision: `29a69c34f06bf3444399287853ea7806767d0944`

Base tree: `de0efce35b6fcc6f851b9c2e643d61ec49d831e0`

## Verdict

`blocked`. No eligible Lean 4 proof body was implemented or found for the exact root
`Stage1Instances.THM_M_0729.PCPTheorem`. The proof item stays `[ ]`; lifecycle stays `planned`; the
root vector stays `[H3, M3, R4]`; audit completion and theorem completion stay false.

The checked `root_of_directionalPackage` theorem is conditional composition. Its premise contains
both missing class inclusions, so it proves neither. Independent proof searches found no
inconsistency, vacuity, or definitional shortcut in the frozen target. The immediate root cut is:

- `M0729-D-NP-PCP`: verifier normalization, robust gap, PCP composition, logarithmic-randomness and
  constant-query accounting, perfect completeness, and exact soundness-half transport;
- `M0729-D-PCP-NP`: finite oracle-bit certificates, exhaustive random-string enumeration with a
  polynomial-time machine proof, and the finite below-threshold branch.

Supplying `DirectionalPackage` as a premise, axiom, bodyless declaration, or assumed external
result would be a prohibited placeholder or theorem substitution. Pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` contains supporting deterministic Turing-machine,
finite-cardinality, polynomial, and logarithm APIs, but no NP/PCP development or terminal theorem.
Even `Turing.TM2ComputableInPolyTime.comp` is only a discarded source `proof_wanted` marker. The
immutable anchor audit found no compatible exact external proof to pin; no global-absence claim is
used as proof evidence.

## Required Split

This is the eighth documented unresolved execution tick: the original blocker, six integrated
rechecks, and this run. Blueprint section 10.2 and the execution skill require splitting after five
unresolved ticks. The integration lane should stop retrying the monolithic item and introduce
dependency-legal child proof nodes for `M0729-D-NP-PCP` and `M0729-D-PCP-NP`, further divided by the
ten frozen packages listed in the paired JSON artifact. This worker did not edit the authoritative
DAG or generated checklist.

## Validation

All commands ran in this worker clone. The pre-existing untracked `Formalizations/Lean/.lake`
symlink points to canonical pinned artifacts and was reused read only. No `lake update`, `lake
build`, dependency clone/fetch/checkout, network request, or `.lake` mutation was performed. Lean
outputs were confined to a disposable directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed all 15 assurance groups and 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0729` | 0 | Rank 766; `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0729/check_statement.py` | 0 | Exact expression hash `2a3d6c88...7bbc5`; all four weakened mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-0729/check_anchor_audit.py` | 0 | Immutable pins and source hashes agreed; no exact PCP root candidate is claimed; root remains M3. |
| `python3 Stage1_Instances/THM-M-0729/check_obligation_tree.py` | 0 | Passed 19 obligations and 76 typed edges; both directional packages remain open. |
| Bounded `lake env lean ../../Stage1_Instances/THM-M-0729/Statement.lean` | 0 | Printed the exact `PCPTheorem` expression. |
| Disposable three-module immutable Lean 4.29.0 `--trust=0 -t0` replay | 0 | Exact statement, conditional assembly, and blocker probe elaborated; axioms were exactly `propext`, `Classical.choice`, and `Quot.sound`; polynomial-time composition remained unavailable as expected. |
| Scoped repository and pinned-mathlib PCP search | 0 | Exact relevant PCP declarations were confined to this dossier; no terminal directional or root body was found. |
| Search for `proof_wanted TM2ComputableInPolyTime.comp` | 0 | Pinned mathlib records only the discarded marker at `Computable.lean:284`. |
| Prohibited-device scan of checked local Lean files | 1 expected | No `sorry`, `admit`, `sorryAx`, bodyless declaration, unsafe/oracle device, `native_decide`, or `implemented_by` was found. |
| Frozen-input and tool digest checks | 0 | Statement, composition, audit, registry, graph, validation, manifests, skill, executable, and dependency hashes match the paired JSON artifact. |
| Scoped diff from original blocker integration `9864b47f` | 0 | Only the check-only blocker probe was added; no proof input or pin changed. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test is absent because the proof phase is incomplete. |

The trust-zero replay copied `Statement.lean`, `ObligationTree.lean`, and
`ProofBlockerProbe.lean` to a `mktemp` directory, assembled `LEAN_PATH` exclusively from the
existing pinned build directories, ran the immutable Lean 4.29.0 binary in dependency order, and
removed the directory. The paired JSON artifact records the full command results and hashes.

## Reopen Condition

After the required split, implement both frozen directional packages and their reduction,
resource, certificate, enumeration, and boundary dependencies without placeholders. Alternatively,
integrate an immutable compatible Lean 4 terminal proof of the exact target with full dependency,
license, and provenance evidence, then rerun exact-type, trust, placeholder, provenance, and
composition checks.

This is current-base nonrelease blocker evidence, not a proof receipt. It does not satisfy
`S56-M-0729-PROOF`, promote scheduler state, close an obligation or the root, or claim audit
completion, validation, release, theorem completion, receipt acceptance, or master acceptance.
Because the assigned phase is not genuinely self-tested complete, `.stage1-worker-selftest.json`
remains absent.
