# THM-M-0578 proof-phase recheck at base be2be0df (slot61)

Item: `S56-M-0578-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `be2be0dfe2f4f2cbdd35f1f2397e5a372d199eb9`

Base tree: `2d3961f99039c515141bdff4511470530d799581`

## Verdict

`blocked`. The exact frozen proposition
`Stage1Instances.THM_M_0578.MilnorExoticSphereTarget` still has no eligible
terminal Lean 4 proof body in the repository or pinned dependency closure. No
proof body was added. The proof item remains `[ ]`, the root vector remains
`[H3, M4, R4]`, and root closure, validation, release, audit completion, and
theorem completion remain false.

The frozen immediate root cut set remains:

- `M0578-C-BUNDLE`: construct the selected smooth Milnor bundle total space;
- `M0578-T-HOMEO`: identify it with the fixed unit seven-sphere by a homeomorphism;
- `M0578-O-NONDIFF`: exclude every smooth diffeomorphism to that sphere.

The first failed proof gate is terminal proof-body availability for
`M0578-C-BUNDLE`. The checked local theorem
`ObligationTree.root_of_exoticWitnessPackage` is only conditional composition:
its premise already contains the smooth manifold, homeomorphism, and
nondiffeomorphism certificate. It constructs none of the open packages and
cannot receive root proof credit.

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`
contains the exact signature only as
`proof_wanted exists_homeomorph_isEmpty_diffeomorph_sphere_seven`. A direct
trust-zero import probe reports that name as unknown. The local mathlib
`master` still contains the marker, and all-ref history finds only its
introduction commit `041fe1fa487`, not a proof-bearing replacement.

A current scoped Lean-source search found 11 relevant files. They are this
dossier, `THM-M-0605`'s duplicate statement and conditional assembly, legacy
statement/audit files, one neighboring statement probe, and mathlib's discarded
marker. No declaration inhabits the exact root or the complete witness package.
Mathlib's bordism module also explicitly lists bordisms and bordism groups as
future work.

The repository base advanced after the prior `e08cfa3f` recheck only by
integrating that prior blocker packet in this target. A proof-input whitelist
diff is empty and the exact source hashes are unchanged. The mathematical
blocker therefore persists at this base.

Closing the frozen route requires placeholder-free Lean implementations of the
Milnor sphere-bundle construction and boundary conventions, its homeomorphism
to the fixed unit seven-sphere, and distinguishing smooth-invariant
computations with invariance strong enough to derive `IsEmpty Diffeomorph`.
Assuming any missing package, crediting `proof_wanted`, or returning only the
conditional composer would violate the assigned theorem boundary and was not
done.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink points at shared canonical artifacts. No
`lake update`, `lake build`, dependency clone/fetch, checkout repair, network
request, or dependency mutation command was issued. Lean outputs were confined
to disposable `/tmp` directories and removed.

The shared `flt-regular` checkout has an invalid `HEAD`, so `lake env` and
`check_statement.py` fail before target elaboration. The pinned Lean 4.29.0
executable and existing dependency oleans remain available. The exact statement
and conditional composition were replayed directly against those artifacts at
trust level zero. This is narrow nonrelease blocker evidence, not a dependency
repair or release-grade reproduction.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0578` | 0 | Rank 622; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0578/check_anchor_audit.py` | 0 | Exact marker and discard semantics passed at the pins; root remains M4 formalization debt. |
| `python3 Stage1_Instances/THM-M-0578/check_obligation_tree.py` | 0 | 13 obligations and 28 typed edges passed; denominator `67da617160dcfef6ea2eb819f105ab0e2a68a351476d55e5761d2e668e63aeda`; root remains open M4. |
| `timeout --foreground 180s python3 Stage1_Instances/THM-M-0578/check_statement.py` | 1 | Shared `flt-regular` failed before elaboration because it cannot resolve `HEAD`; no repair or fetch was attempted. |
| direct pinned-Lean trust-zero replay below | 0 | Exact statement and conditional composition elaborated; `#print axioms` reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| direct trust-zero probe of the source marker name | 1 | Expected negative evidence: `Unknown identifier`. |
| scoped retained-body search | 0 | 11 relevant files were duplicate/conditional statements, legacy/audit material, or the discarded marker; no eligible terminal body was found. |
| forbidden-construct scan of owned Lean files | 1 | Expected no-match exit; no prohibited proof escape was found. |
| scoped `git diff --name-status e08cfa3f..HEAD` | 0 | Empty for all proof-input files and Lean pins; only the prior blocker packet was integrated in this target. |
| `python3 -m json.tool` on the companion blocker record | 0 | The current-base blocker record is valid JSON. |
| target-local tracked and added-file `git diff --check` | 0 | No whitespace diagnostic. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion manifest is absent because the proof phase is incomplete. |

The direct kernel replay used only the pinned executable and existing olean
closure:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d /tmp/thm-m-0578-proof-be2be0df-slot61.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0578/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0578/ObligationTree.lean "$tmp/ObligationTree.lean"
lean="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
lean_path="$root/Formalizations/Lean/.lake/build/lib/lean:$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean"
for d in "$root"/Formalizations/Lean/.lake/packages/*/.lake/build/lib/lean; do
  if [ -d "$d" ]; then lean_path="$lean_path:$d"; fi
done
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 600s \
  "$lean" --trust=0 -t0 -R "$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 600s \
  "$lean" --trust=0 -t0 -R "$tmp" "$tmp/ObligationTree.lean"
```

The expected-negative declaration probe used the same pinned environment:

```bash
printf '%s\n' \
  'import Mathlib.Geometry.Manifold.PoincareConjecture' \
  '#check exists_homeomorph_isEmpty_diffeomorph_sphere_seven' \
  > "$tmp/Probe.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 300s \
  "$lean" --trust=0 -t0 -R "$tmp" "$tmp/Probe.lean"
```

It exited 1 with
`Unknown identifier exists_homeomorph_isEmpty_diffeomorph_sphere_seven`.

## Retry Condition

Resume after placeholder-free implementations of `M0578-C-BUNDLE`,
`M0578-T-HOMEO`, and `M0578-O-NONDIFF` with their frozen child obligations.
Alternatively, integrate an immutable compatible Lean 4 proof-bearing
declaration of the exact root with a complete dependency lock, license record,
and terminal-body provenance, then rerun node-scoped exact-type, trust,
provenance, and composition checks. Separately restore the scheduler-provided
pinned `flt-regular` checkout before requiring `lake env` replay.

This is a current-base nonrelease blocker record. It is not a proof receipt,
does not satisfy `S56-M-0578-PROOF`, proposes no state change, and supports
neither root closure nor theorem completion. Because the assigned proof phase
is incomplete, `.stage1-worker-selftest.json` is intentionally absent.
