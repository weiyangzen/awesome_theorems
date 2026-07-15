# THM-M-0729 proof recheck at `5cca9791` (slot67)

Item: `S56-M-0729-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T15:43:56+08:00`

Base revision: `5cca979173a36d739670a3b5ecad23d89dc96292`

Base tree: `97ccf7381b147bf0f25425a5a7678e51265c6eb3`

## Verdict

`blocked`. No eligible Lean 4 proof body was implemented or found for the exact root
`Stage1Instances.THM_M_0729.PCPTheorem`. The proof item stays `[ ]`; lifecycle stays `planned`; the
root vector stays `[H3, M3, R4]`; audit completion and theorem completion stay false.

The checked `root_of_directionalPackage` theorem is conditional composition. Its premise is the
conjunction of both missing class inclusions, so it proves neither inclusion. Definition-level
inspection found no definitional equality, inconsistency, vacuity, or model collapse in the frozen
statement. In particular, perfect completeness and finite-cardinality soundness do not trivialize
the checker class. The immediate root cut remains:

- `M0729-D-NP-PCP`: verifier normalization, a constant-gap robustness theorem, PCP composition,
  logarithmic-randomness and constant-query accounting, perfect completeness, and exact
  soundness-half transport;
- `M0729-D-PCP-NP`: finite oracle-bit certificates, exhaustive enumeration of logarithmically many
  random strings with a polynomial-time machine proof, and the finite below-threshold branch.

Supplying `DirectionalPackage` as a premise, axiom, bodyless declaration, or assumed external result
would be a prohibited placeholder or theorem substitution. Pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` has deterministic Turing-machine,
finite-cardinality, polynomial, and logarithm support, but no NP/PCP development or terminal PCP
theorem. Even `Turing.TM2ComputableInPolyTime.comp` is only a discarded source `proof_wanted`
marker. Fresh bounded GitHub and Sourcegraph discovery found no Lean PCP theorem candidate; those
mutable results provide neither proof credit nor a global-absence claim. The immutable anchor audit
still has no compatible external terminal proof to pin.

The required predecessor `S56-M-0729-OBLIGATION_TREE` is provisional `[_]`, not master accepted.
That independently prevents proof-node master acceptance, even if a new proof body were available.

## Current-Base Delta

The current base integrated the preceding `435748c4` recheck pair plus unrelated target work. No
THM-M-0729 statement, composition, registry, typed graph, anchor audit, validation specification,
toolchain, dependency manifest, target-manifest entry, execution-skill input, or proof body changed.
The terminal-body blocker is therefore unchanged and rebound to this base.

## Validation

All commands ran in this worker clone. The pre-existing untracked `Formalizations/Lean/.lake`
symlink points to canonical pinned artifacts and was reused read-only. No `lake update`, `lake
build`, dependency clone/fetch/checkout, or `.lake` mutation was performed. Lean outputs were
confined to a disposable directory and removed. The two discovery agents used read-only network
search; no dependency or repository content was fetched.

The exact statement mutation check and a node-scoped replay of `Statement.lean`,
`ObligationTree.lean`, and `ProofBlockerProbe.lean` with `lake env lean --trust=0 -t0` passed against
existing pinned artifacts. This establishes that the exact statement and conditional composition
still elaborate; it supplies neither missing PCP inclusion.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed all 15 assurance groups and 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0729` | 0 | Rank 766; `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all; readlink Formalizations/Lean/.lake` | 0 | Base `5cca9791...292`, tree `97ccf738...eb3`; only the canonical `.lake` symlink was initially untracked. |
| `python3 Stage1_Instances/THM-M-0729/check_statement.py` | 0 | Exact expression hash `2a3d6c88...7bbc5`; four weakened mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-0729/check_anchor_audit.py` | 0 | Immutable pins and source hashes agreed; no exact PCP root candidate is claimed; root remains M3. |
| `python3 Stage1_Instances/THM-M-0729/check_obligation_tree.py` | 0 | Passed 19 obligations and 76 typed edges; both directional packages remain open. |
| Disposable three-module `lake env lean --trust=0 -t0` replay | 0 | Exact statement, conditional assembly, and blocker probe elaborated; axioms were exactly `propext`, `Classical.choice`, and `Quot.sound`; polynomial-time composition application failed as expected. |
| Scoped repository and pinned-mathlib PCP search | 0 | Exact probabilistic PCP declarations were confined to this dossier; no terminal inclusion or root body was found. |
| Read-only GitHub and Sourcegraph discovery | 0 | Two GitHub repository searches returned zero results; the bounded Sourcegraph Lean query returned `matchCount: 0`, `limitHit: false`. No proof credit or global-absence claim is derived. |
| Search for `proof_wanted TM2ComputableInPolyTime.comp` | 0 | Pinned mathlib records only the discarded marker at `Computable.lean:284`. |
| Prohibited-device scan of checked local Lean files | 1 expected | No `sorry`, `admit`, `sorryAx`, bodyless declaration, unsafe/oracle device, `native_decide`, or `implemented_by` was found. |
| Frozen-input and tool digest checks | 0 | Statement, composition, audit, registry, graph, validation, manifest, skill, executable, and dependency hashes match the paired structured artifact. |
| Scoped diff from prior recheck base `435748c4` | 0 | No proof input, frozen statement, registry, graph, audit, pin, manifest, skill, or proof body changed. |

The trust-zero replay used disposable copies and this command shape from the worker root:

```bash
set -euo pipefail
root=$(pwd)
tmp=$(mktemp -d /tmp/thm-m-0729-slot67-lake.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0729/{Statement,ObligationTree,ProofBlockerProbe}.lean "$tmp/"
cd Formalizations/Lean
lean_path=$(lake env printenv LEAN_PATH)
lake env env LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300s \
  lean --trust=0 -t0 -R "$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
lake env env LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300s \
  lean --trust=0 -t0 -R "$tmp" -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean"
lake env env LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300s \
  lean --trust=0 -t0 -R "$tmp" "$tmp/ProofBlockerProbe.lean"
```

## Reopen Condition

Resume after placeholder-free implementations of both frozen directional packages and their
reduction, resource, certificate, enumeration, and boundary dependencies exist. Alternatively,
integrate an immutable compatible Lean 4 terminal proof of the exact target with full dependency
and license evidence, then rerun exact-type, trust, provenance, and composition checks.

This is current-base nonrelease blocker evidence, not a proof receipt. It does not satisfy
`S56-M-0729-PROOF`, promote scheduler state, close an obligation or the root, or claim audit
completion, validation, release, theorem completion, receipt acceptance, or master acceptance.
Because the assigned phase is not genuinely self-tested complete, `.stage1-worker-selftest.json`
remains absent.
