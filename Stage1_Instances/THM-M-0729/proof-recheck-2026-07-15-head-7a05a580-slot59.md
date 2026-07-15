# THM-M-0729 proof recheck at `7a05a580` (slot59)

Item: `S56-M-0729-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T17:11:57+08:00`

Base revision: `7a05a580f6eb39b1dcd87bbd8f3d9f4c0ecd4cb4`

Base tree: `681b326462f0271a612a5178ae0846f857b96648`

## Verdict

`blocked`. No eligible placeholder-free Lean 4 proof body was implemented or found for the exact
root `Stage1Instances.THM_M_0729.PCPTheorem`. The proof item stays `[ ]`; lifecycle stays `planned`;
the root vector stays `[H3, M3, R4]`; audit completion and theorem completion stay false.

The exact target is the equality of verifier-based binary NP and a nonadaptive binary PCP class
with eventual logarithmic randomness, a uniform constant query bound, perfect completeness, and
finite-cardinality soundness one half. The checked `root_of_directionalPackage` theorem is only
conditional assembly: its premise contains both missing inclusions. Definition-level inspection
found no inconsistency, vacuity, definitional equality, or model collapse. In particular, the
polynomial-time fields require actual bundled Turing-machine witnesses, and zero randomness does
not trivialize soundness.

The immediate machine root cut remains:

- `M0729-D-NP-PCP`: verifier normalization, robust gap, PCP composition, randomness/query
  accounting, perfect completeness, and soundness-half transport;
- `M0729-D-PCP-NP`: finite oracle-bit certificates, exhaustive random-string verification with a
  polynomial-time machine proof, and the finite below-threshold branch.

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` has supporting
Turing-machine, finite-cardinality, polynomial, and logarithm APIs but no NP/PCP development or
terminal PCP theorem. Even `Turing.TM2ComputableInPolyTime.comp` is only a source `proof_wanted`
marker at `Computable.lean:284`, not an importable declaration.

## New Candidate Audit

A current bounded Sourcegraph search newly located one probabilistic-PCP surface in
`facebookresearch/atlas-lean` at commit
`34ffed396f376454c1a9b297f3fd74c5c801fb50`, file
`Atlas/BooleanFunctions/code/PCP.lean`. The immutable raw file has SHA-256
`0900031bc64ebe5914022243cf68a04effad8fe0c2890d11cc4e169a17ef5fbe`.
It is ineligible:

- line 111 proves only a different Gap-3SAT claim and ends `by sorry`;
- line 100 makes polynomial-time reduction an `opaque` proposition;
- its length-indexed languages, real-valued soundness, finite proof model, and missing TM
  polynomial-time fields do not have the exact frozen target type;
- its root license is CC BY-NC 4.0 with a no-training rider, not an already-approved dependency
  integration path.

The `InPCP` query completed with one match in one repository and `skipped=[]`; `PCPVerifier` and
`Gap3SAT` completed with eight and five matches, all in the same repository. Exact phrase searches
for `probabilistically checkable`, `PCP theorem`, and `NP = PCP` completed with zero matches. These
are bounded dated discovery results, not a global-absence claim. They rule out proof credit for the
only newly located candidate.

The required predecessor `S56-M-0729-OBLIGATION_TREE` remains provisional `[_]`, rather than master
accepted. That independently prevents proof-node master acceptance even if a proof body appeared.

## Current-Base Delta

The previous blocker evidence was integrated at `b8c0a0c1`. From that commit through the current
base, no THM-M-0729 statement, composition, registry, typed graph, anchor audit, validation
specification, toolchain, dependency manifest, target-manifest entry, execution-skill input, or
proof body changed. The missing-body blocker therefore persists and is rebound to this base. The
Atlas audit is new negative candidate evidence; it adds no proof closure.

## Validation

All commands ran in this worker clone. The pre-existing untracked `Formalizations/Lean/.lake`
symlink points to canonical pinned artifacts and was reused read-only. No `lake update`, `lake
build`, dependency clone/fetch/checkout, or `.lake` mutation was performed. Lean outputs were
confined to disposable directories and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed all 15 assurance groups and 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0729` | 0 | Rank 766; `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0729/check_statement.py` | 0 | Exact expression hash `2a3d6c88...7bbc5`; all four weakened mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-0729/check_anchor_audit.py` | 0 | Immutable pins and source hashes agreed; no exact root candidate is claimed; root remains M3. |
| `python3 Stage1_Instances/THM-M-0729/check_obligation_tree.py` | 0 | Passed 19 obligations and 76 typed edges; both directional packages remain open. |
| Disposable namespaced three-module `lake env lean --trust=0 -t0` replay | 0 | Exact statement, conditional assembly, and blocker probe elaborated; axiom reports were exactly `propext`, `Classical.choice`, and `Quot.sound`; the unavailable composition application failed as expected. |
| Scoped repository and pinned-mathlib PCP search | 0 | Relevant probabilistic-PCP declarations were confined to this dossier; no terminal inclusion or root body was found; output SHA-256 `3fa8c2bf...c9a9`. |
| Six bounded Sourcegraph queries | 0 | Three exact phrases had zero matches; `InPCP`, `PCPVerifier`, and `Gap3SAT` found only Atlas. All terminal progress events had `skipped=[]`; response hashes are in the paired JSON. |
| Immutable Atlas raw-file and license download plus scan | 0 | PCP source hash `0900031b...fbe`; candidate contains `opaque IsPolyTimeReduction` and `by sorry`; license hash `289dc0e9...1abc`. |
| `rg -n 'proof_wanted TM2ComputableInPolyTime.comp' .../Computable.lean` | 0 | Pinned mathlib records only the discarded marker at line 284. |
| Parser-oriented prohibited-device scan of checked local Lean files | 1 expected | No declaration-level `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, `unsafe`, `external`, `native_decide`, or `implemented_by` occurs. |
| Frozen-input and executable digest checks | 0 | Statement, composition, audit, registry, graph, validation, toolchain, manifest, target manifest, skill, and Lean executable match the paired structured artifact. |
| `git diff --quiet b8c0a0c1..HEAD -- <frozen proof inputs and pins>` | 0 | No frozen input, pin, or proof body changed after the latest integrated THM-M-0729 recheck. |

The trust-zero replay used a disposable `THM0729` namespace directory and rewrote only the two local
import lines in the disposable copies, because Lean 4 module names are derived from the common root:

```bash
set -u
root=$PWD
target=$root/Stage1_Instances/THM-M-0729
tmp=$(mktemp -d /tmp/thm-m-0729-slot59-7a05a580-replay.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/THM0729"
cp "$target/Statement.lean" "$tmp/THM0729/Statement.lean"
sed 's/^import Statement$/import THM0729.Statement/' \
  "$target/ObligationTree.lean" > "$tmp/THM0729/ObligationTree.lean"
sed -e 's/^import Statement$/import THM0729.Statement/' \
  -e 's/^import ObligationTree$/import THM0729.ObligationTree/' \
  "$target/ProofBlockerProbe.lean" > "$tmp/THM0729/ProofBlockerProbe.lean"
cd "$root/Formalizations/Lean"
lean_path=$(timeout 120s lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 600s lake env \
  lean --trust=0 -t0 -R "$tmp" -o "$tmp/THM0729/Statement.olean" \
  "$tmp/THM0729/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 600s lake env \
  lean --trust=0 -t0 -R "$tmp" -o "$tmp/THM0729/ObligationTree.olean" \
  "$tmp/THM0729/ObligationTree.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 600s lake env \
  lean --trust=0 -t0 -R "$tmp" "$tmp/THM0729/ProofBlockerProbe.lean"
```

This command was run from `Formalizations/Lean`; the repository root remained in `$root`, so the
disposable copies and imported `.olean` files stayed outside `.lake`.

## Reopen Condition

Resume after placeholder-free implementations of both frozen directional packages and their
reduction, resource, certificate, enumeration, and boundary dependencies exist. Alternatively,
integrate an immutable, license-compatible Lean 4 terminal proof of the exact target with complete
dependency and terminal-body provenance, then rerun exact-type, trust, placeholder, provenance, and
composition checks.

This is current-base nonrelease blocker evidence, not a proof receipt. It does not satisfy
`S56-M-0729-PROOF`, promote scheduler state, close an obligation or the root, or claim audit
completion, validation, release, theorem completion, receipt acceptance, or master acceptance.
Because the assigned phase is not genuinely self-tested complete, `.stage1-worker-selftest.json`
remains absent.
