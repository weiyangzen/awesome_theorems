# THM-M-0729 proof recheck at `b8c0a0c1` (slot59)

Item: `S56-M-0729-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T16:22:31+08:00`

Base revision: `b8c0a0c119a82ef435e23f9ff85bfd783db95736`

Base tree: `831576eb7d1273d01e99653d36b616e99e85dc0f`

## Verdict

`blocked`; no proof node or theorem state changes.

The exact target remains the full binary PCP theorem: verifier-based `InNP` equals the class
recognized by polynomial-time, nonadaptive proof-oracle checkers with eventual logarithmic
randomness, a uniform constant query bound, perfect completeness, and soundness one half. The only
checked root assembly, `root_of_directionalPackage`, assumes both inclusions and therefore supplies
no body for either one.

No eligible local or pinned declaration constructs `M0729-D-NP-PCP` or `M0729-D-PCP-NP`. The forward
direction still requires the frozen constraint normalization, robust gap, PCP composition, resource,
perfect-completeness, and soundness packages. The reverse direction still requires finite proof-bit
certificates, exhaustive logarithmic-randomness verification with a polynomial-time implementation,
and the finite short-input branch. Even the supporting pinned mathlib polynomial-time composition
operation is only a source-level `proof_wanted` marker and is not a checked declaration.

The prerequisite `S56-M-0729-OBLIGATION_TREE` remains provisional `[_]`, independently preventing
master acceptance. This recheck adds no premise, axiom, placeholder, altered checker model, weaker
inclusion, external moving dependency, or synthetic proof result.

## Current-base delta

The preceding recheck was based on `6ac589f0d8c5a9eeb726a1a05def7f9467ea2e2d`. The current base
integrated that recheck pair plus work for unrelated targets. A scoped diff found no change to the
statement, conditional composition, blocker probe, anchor audit, obligation registry, typed graphs,
validation specification, toolchain, dependency manifest, target manifest, or execution skill.
Their recorded hashes still match. Thus no proof authority, dependency, or proof candidate changed;
the missing-body blocker is rebound to the current base.

The initial worktree contained only the automation-provided untracked `Formalizations/Lean/.lake`
symlink to canonical pinned artifacts. It was reused read-only. No `lake update`, `lake build`,
dependency clone/fetch/checkout, network discovery, or `.lake` mutation was performed. Lean outputs
were written only under a disposable `/tmp` directory and removed.

## Exact validation evidence

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed all 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0729` | 0 | Rank 766; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all; readlink Formalizations/Lean/.lake; date --iso-8601=seconds` | 0 | Base `b8c0a0c1...5736`, tree `831576eb...dc0f`; only the canonical `.lake` symlink was initially untracked; timestamp above. |
| `python3 Stage1_Instances/THM-M-0729/check_statement.py` | 0 | Exact expression hash `2a3d6c88...7bbc5`; all four weakened mutations were distinguished against pinned mathlib. |
| `python3 Stage1_Instances/THM-M-0729/check_anchor_audit.py` | 0 | Immutable pins and source hashes agreed; no exact PCP root candidate is claimed; root remains M3. |
| `python3 Stage1_Instances/THM-M-0729/check_obligation_tree.py` | 0 | Passed 19 obligations and 76 typed edges; denominator `66be2951...a2e854`; both directional packages remain open. |
| Disposable three-module `lake env lean --trust=0 -t0` replay | 0 | Exact statement, conditional assembly, and blocker probe elaborated. Axiom reports were exactly `propext`, `Classical.choice`, and `Quot.sound`; the unavailable polynomial-time composition application failed as expected. |
| Scoped repository and pinned-mathlib Lean-source search | 0 | Exact probabilistic PCP declarations were confined to this dossier; no terminal directional or root proof body was found. |
| `rg -n 'proof_wanted TM2ComputableInPolyTime\.comp' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Computability/TuringMachine/Computable.lean` | 0 | Pinned mathlib line 284 contains only the discarded marker, not proof authority. |
| Prohibited-device scan of the checked local Lean surface | 1 expected | No `sorry`, `admit`, `sorryAx`, bodyless declaration, unsafe/oracle device, `native_decide`, or `implemented_by` was found. |
| Frozen-input, executable, and dependency revision/hash checks | 0 | All values match the paired JSON artifact and the immutable audit. |
| Scoped diff from `6ac589f0` to the current base | 0 | No proof input or pin changed; only the already integrated prior recheck pair exists under this target. |

The trust-zero replay used this command shape from the worker root:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-0729-slot59-b8c0a0c1.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0729/{Statement,ObligationTree,ProofBlockerProbe}.lean "$tmp/"
cd Formalizations/Lean
lean_path=$(timeout 30s lake env printenv LEAN_PATH)
timeout --foreground --kill-after=3s 300s lake env env LEAN_NUM_THREADS=1 \
  LEAN_PATH="$lean_path" lean --trust=0 -t0 -R "$tmp" \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean"
timeout --foreground --kill-after=3s 300s lake env env LEAN_NUM_THREADS=1 \
  LEAN_PATH="$tmp:$lean_path" lean --trust=0 -t0 -R "$tmp" \
  -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean"
timeout --foreground --kill-after=3s 300s lake env env LEAN_NUM_THREADS=1 \
  LEAN_PATH="$tmp:$lean_path" lean --trust=0 -t0 -R "$tmp" \
  "$tmp/ProofBlockerProbe.lean"
```

## Reopen condition

Resume after placeholder-free implementations of both frozen directional packages and their
reduction, resource, certificate, enumeration, and boundary dependencies exist. Alternatively,
integrate an immutable compatible Lean 4 proof of the exact target with complete dependency,
license, type-transport, trust, and provenance evidence.

This is current-base nonrelease blocker evidence, not a proof receipt. It does not satisfy
`S56-M-0729-PROOF`, close any obligation or the root, change scheduler state, or claim audit
completion, validation, release, theorem completion, receipt acceptance, or master acceptance.
Because the assigned phase is not genuinely self-tested complete, `.stage1-worker-selftest.json`
remains absent.
