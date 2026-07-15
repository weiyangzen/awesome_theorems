# THM-M-0729 proof recheck at `e90521b4` (slot66)

Item: `S56-M-0729-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T13:34:14+08:00`

Base revision: `e90521b4b150b98d81c4dca2462ad36b64d4673e`

Base tree: `f12951f481d2b51f33d6d300dc2874b3c49ed0e0`

## Verdict

`blocked`. No eligible Lean 4 proof body was implemented or found for the exact root
`Stage1Instances.THM_M_0729.PCPTheorem`. The proof item stays `[ ]`; lifecycle stays `planned`; the
root vector stays `[H3, M3, R4]`; audit completion and theorem completion stay false.

The checked declaration `root_of_directionalPackage` is conditional composition. Its premise is
the conjunction of both missing class inclusions, so it proves neither inclusion. Fresh independent
proof exploration found no inconsistency or trivialization in the frozen statement. The immediate
root cut remains:

- `M0729-D-NP-PCP`: verifier normalization, a constant-gap robustness theorem, PCP composition,
  logarithmic-randomness and constant-query accounting, perfect completeness, and exact
  soundness-half transport;
- `M0729-D-PCP-NP`: finite oracle-bit certificates, exhaustive enumeration of logarithmically many
  random strings with a polynomial-time machine proof, and the finite below-threshold branch.

Supplying `DirectionalPackage` as a premise, axiom, bodyless declaration, or assumed external
result would be a placeholder or theorem substitution. None was added. Pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` has deterministic Turing-machine, finite-cardinality,
polynomial, and logarithm infrastructure, but no NP/PCP development or PCP theorem. Even
`Turing.TM2ComputableInPolyTime.comp` is only a discarded source `proof_wanted` marker. The frozen
anchor audit found no compatible immutable external proof to pin; its authenticated GitHub code
search lane was unavailable, so no global-absence claim is made.

## Validation

All commands ran in this worker clone. The pre-existing untracked `Formalizations/Lean/.lake`
symlink points to canonical pinned artifacts and was reused read-only. No `lake update`, `lake
build`, dependency clone/fetch/checkout, network request, or `.lake` mutation was performed.
Temporary Lean outputs and validator scratch files were removed.

Normal `lake env lean` did not start within a bounded 12-second replay while many workers contended
on the shared canonical environment; the `flt-regular` worktree still has no resolvable `HEAD`.
The exact statement, conditional composition, and blocker probe were replayed separately with the
immutable Lean 4.29.0 executable against existing pinned package oleans at trust level zero. That
fallback passed but is nonrelease evidence only.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed all 15 assurance groups and 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0729` | 0 | Rank 766; `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all; readlink Formalizations/Lean/.lake` | 0 | Base `e90521b4...673e`, tree `f12951f4...e0e0`; only the canonical `.lake` symlink was initially untracked. |
| bounded `lake env lean ../../Stage1_Instances/THM-M-0729/Statement.lean` | 124 | Timed out before elaboration with no output; no dependency repair was attempted. |
| `python3 Stage1_Instances/THM-M-0729/check_anchor_audit.py` | 0 | Immutable pins and source hashes agreed; no exact PCP root candidate is claimed; root remains M3. |
| `python3 Stage1_Instances/THM-M-0729/check_obligation_tree.py` | 0 | Passed 19 obligations and 76 typed edges; both directional packages remain open. |
| Isolated immutable Lean 4.29.0 `--trust=0 -t0` replay against existing pinned oleans | 0 | Exact statement, conditional assembly, and blocker probe elaborated; axioms were exactly `propext`, `Classical.choice`, and `Quot.sound`; polynomial-time composition application failed as expected. |
| Scoped repository and pinned-mathlib PCP search | 0 | Exact PCP declarations were confined to this dossier; no terminal inclusion or root body was found. |
| Search for `proof_wanted TM2ComputableInPolyTime.comp` | 0 | Pinned mathlib records only the discarded marker at `Computable.lean:284`. |
| Prohibited-device scan of checked local Lean files | 1 expected | No `sorry`, `admit`, `sorryAx`, bodyless declaration, unsafe/oracle device, `native_decide`, or `implemented_by` was found. |
| Frozen-input and tool digest checks | 0 | Statement, composition, audit, registry, graph, validation, manifest, skill, executable, and dependency hashes match the paired structured artifact. |
| Scoped diff from original blocker integration `9864b47f` | 0 | Only the check-only blocker probe was added; no proof input, frozen statement, registry, graph, audit, pin, manifest, or skill changed. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test is absent because the proof phase is incomplete. |

The trust-zero replay used disposable copies and this command shape from the worker root:

```bash
set -euo pipefail
root=$(pwd)
tmp=$(mktemp -d /tmp/thm-m-0729-slot66.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0729/{Statement,ObligationTree,ProofBlockerProbe}.lean "$tmp/"
lean_bin="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
lean_path="$root/Formalizations/Lean/.lake/build/lib/lean:$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean"
while IFS= read -r d; do lean_path="$lean_path:$d"; done < <(
  find -L "$root/Formalizations/Lean/.lake/packages" -path '*/.lake/build/lib/lean' \
    -type d ! -path '*/flt-regular/*' -print | sort
)
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300s \
  "$lean_bin" --trust=0 -t0 -R "$tmp" -o Statement.olean Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300s \
  "$lean_bin" --trust=0 -t0 -R "$tmp" -o ObligationTree.olean ObligationTree.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300s \
  "$lean_bin" --trust=0 -t0 -R "$tmp" ProofBlockerProbe.lean
```

## Reopen Condition

Resume after placeholder-free implementations of both frozen directional packages and their
reduction, resource, certificate, enumeration, and boundary dependencies exist. Alternatively,
integrate an immutable compatible Lean 4 terminal proof of the exact target with full dependency
and license evidence. The canonical `flt-regular` checkout must also be repaired outside this
worker before normal `lake env lean` replay.

This is current-base nonrelease blocker evidence, not a proof receipt. It does not satisfy
`S56-M-0729-PROOF`, promote scheduler state, close an obligation or the root, or claim audit
completion, validation, release, theorem completion, receipt acceptance, or master acceptance.
Because the assigned phase is not genuinely self-tested complete, `.stage1-worker-selftest.json`
remains absent.
