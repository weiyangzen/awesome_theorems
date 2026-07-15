# THM-M-0578 proof-phase recheck at base b1a5b03c (slot60)

Item: `S56-M-0578-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `b1a5b03c9eb85b0777b34f58df31029086acf260`

Base tree: `cb7fc5c4df1ed6cf6b1024492bf35bfa524a580b`

## Verdict

`blocked`. The exact frozen proposition
`Stage1Instances.THM_M_0578.MilnorExoticSphereTarget` still has no eligible
terminal Lean 4 proof body in the repository or pinned dependency closure. No
proof body was added. The proof item remains `[ ]`, the root vector remains
`[H3, M4, R4]`, and root closure, validation, release, audit completion, and
theorem completion remain false.

The frozen immediate root cut remains:

- `M0578-C-BUNDLE`: construct the selected smooth Milnor bundle total space;
- `M0578-T-HOMEO`: identify it with the fixed unit seven-sphere by a homeomorphism;
- `M0578-O-NONDIFF`: exclude every smooth diffeomorphism to that sphere.

The first failed proof gate is terminal proof-body availability for
`M0578-C-BUNDLE`. The checked theorem
`ObligationTree.root_of_exoticWitnessPackage` is conditional composition only:
its premise already contains the smooth manifold, homeomorphism, and
nondiffeomorphism certificate. It constructs none of the open packages and
cannot receive root proof credit. Another wrapper would duplicate that same
conditional body rather than close the root.

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`
contains the exact signature only as the discarded source marker
`proof_wanted exists_homeomorph_isEmpty_diffeomorph_sphere_seven`. Batteries
elaborates this syntax under `withoutModifyingEnv` and removes the declaration.
The trust-zero owned probe confirms that the name is unknown after import.
Local mathlib history contains only its introduction commit `041fe1fa487`, not
a proof-bearing replacement.

A current-base search across repository formalizations and all 9,676 Lean
files in the existing pinned packages found 35 relevant lines in 13 files.
They are target or analogous statements, conditional composition, audit
probes, legacy metadata, or the discarded marker. No retained declaration
inhabits the exact target or the complete `ExoticWitnessPackage`; no Milnor
bundle, clutching construction, homotopy-sphere bridge, Eells-Kuiper invariant,
or Kervaire-Milnor implementation was found. Mathlib's bordism module still
lists bordisms and bordism groups as future work.

The owned `ProofBlockerProbe.lean` rejects two invalid shortcuts at trust level
zero. `Diffeomorph.refl` inhabits the standard sphere's infinity-smooth
self-diffeomorphism type, so the standard sphere cannot be the requested
witness. The source marker is absent after import. Neither result constructs
an exotic sphere or changes the root state.

The base advanced after the `a60b47b4` recheck by integrating that blocker
pair. A proof-input whitelist diff is empty and all frozen source hashes and
Lean pins are unchanged. Fresh structural and kernel checks reproduce the
same mathematical blocker.

Closing the route requires placeholder-free Lean implementations of the
Milnor sphere-bundle construction and conventions, its homotopy/topological
sphere identification, and distinguishing smooth-invariant computations plus
invariance strong enough to derive `IsEmpty Diffeomorph`. Assuming any missing
package, crediting `proof_wanted`, or returning only the conditional composer
would violate the exact theorem boundary and was not done.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink points at shared canonical pinned artifacts
and was reused read-only. No `lake update`, `lake build`, dependency clone/fetch,
checkout repair, network request, or dependency mutation command was issued.
Lean outputs were confined to a disposable `/tmp` directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0578` | 0 | Rank 622; planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0578/check_statement.py` | 0 | Exact target elaborated; all four structural mutations were distinguished; expression digest `c9d29902fc3b1bd25c4a83aa5daaa4ce201798576d7b5e16e9bbc05e76a9d32c`. |
| `python3 Stage1_Instances/THM-M-0578/check_anchor_audit.py` | 0 | Exact source marker and discard semantics passed at the pins; root remains M4 formalization debt. |
| `python3 Stage1_Instances/THM-M-0578/check_obligation_tree.py` | 0 | 13 obligations and 28 typed edges passed; denominator `67da617160dcfef6ea2eb819f105ab0e2a68a351476d55e5761d2e668e63aeda`; root remains open M4. |
| isolated pinned `lake env` trust-zero replay of `Statement.lean`, `ObligationTree.lean`, and `ProofBlockerProbe.lean` | 0 | Exact statement, conditional composition, standard-sphere rejection, and discarded-name rejection elaborated; both printed theorems report exactly `propext`, `Classical.choice`, and `Quot.sound`; statement olean SHA-256 `83dcfaec38f0d842614531d19db521eb5f8496fa2d891fe59c6e2fc189d3d3a7`. |
| scoped retained-body search across repository and 9,676 pinned-package Lean files | 0 | 35 matching lines in 13 statement, conditional, audit, metadata, probe, or marker files; no eligible terminal proof body found. |
| pinned prerequisite search for clutching, homotopy/exotic sphere, Eells-Kuiper, Kervaire-Milnor, or Milnor-sphere implementations | 1 | Expected no-match exit; no implementation of the frozen construction, topology, or obstruction packages found. |
| pinned marker, `ProofWanted`, mathlib history, and bordism inspection | 0 | The marker is discarded; history contains only introduction commit `041fe1fa487`; bordisms and bordism groups remain future work. |
| forbidden-construct scan of owned Lean files | 1 | Expected no-match exit; no `sorry`, `admit`, axiom declaration, `sorryAx`, `native_decide`, unsafe declaration, or equivalent proof escape found. |
| scoped `git diff --name-status a60b47b4..HEAD` | 0 | Empty for every canonical proof input and Lean pin; the whole-target delta contains only the integrated prior blocker pair. |
| companion JSON parse and target-local added-file/final whitespace checks | 0 | JSON is valid and no whitespace diagnostic was emitted. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion manifest is absent because the proof phase is incomplete. |

## Exact Recipe

The isolated kernel replay used the pinned Lake environment:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-0578-proof-b1a5b03c-slot60.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0578/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0578/ObligationTree.lean "$tmp/ObligationTree.lean"
cp Stage1_Instances/THM-M-0578/ProofBlockerProbe.lean "$tmp/ProofBlockerProbe.lean"
lean=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout --foreground --kill-after=5s 600s \
  "$lean" --trust=0 -t0 -R "$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean"
sha256sum "$tmp/Statement.olean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout --foreground --kill-after=5s 600s \
  "$lean" --trust=0 -t0 -R "$tmp" "$tmp/ObligationTree.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout --foreground --kill-after=5s 600s \
  "$lean" --trust=0 -t0 -R "$tmp" "$tmp/ProofBlockerProbe.lean"
```

The environment, retained-body, prerequisite, source-history, escape, and
base-delta checks used these exact commands:

```bash
git rev-parse HEAD^{commit} HEAD^{tree}
git status --short
sha256sum "$(cd Formalizations/Lean && lake env which lean)"
git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD^{commit} HEAD^{tree}
git -C Formalizations/Lean/.lake/packages/batteries rev-parse HEAD^{commit} HEAD^{tree}
git -C Formalizations/Lean/.lake/packages/flt-regular rev-parse HEAD^{commit} HEAD^{tree}
sha256sum \
  Stage1_Instances/THM-M-0578/Statement.lean \
  Stage1_Instances/THM-M-0578/ObligationTree.lean \
  Stage1_Instances/THM-M-0578/ProofBlockerProbe.lean \
  Stage1_Instances/THM-M-0578/obligation-registry.json \
  Stage1_Instances/THM-M-0578/typed-graphs.json \
  Stage1_Instances/THM-M-0578/anchor-audit.json \
  Stage1_Instances/THM-M-0578/validation-specs.json \
  Stage1_Instances/THM-M-0578/statement.json \
  Formalizations/Lean/lake-manifest.json \
  Formalizations/Lean/lean-toolchain

pattern='(MilnorExoticSphereTarget|exists_homeomorph_isEmpty_diffeomorph_sphere_seven|ExoticWitnessPackage|ExoticSevenSphereExists|Milnor.{0,40}sphere|exotic.{0,40}(7.?sphere|seven.?sphere)|Eells.?Kuiper|Kervaire.?Milnor|sphere.{0,30}bundle.{0,30}sphere)'
mapfile -t files < <(rg -l -i --glob '*.lean' "$pattern" \
  Stage1_Instances Formalizations/Lean/AwesomeTheorems \
  Formalizations/Lean/.lake/packages | sort)
printf 'matching_files=%d\n' "${#files[@]}"
printf '%s\n' "${files[@]}"
rg -n -i --glob '*.lean' "$pattern" Stage1_Instances \
  Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages | wc -l
find -L Formalizations/Lean/.lake/packages -type f -name '*.lean' | wc -l

rg -n -i --glob '*.lean' \
  '(clutching|homotopy.?sphere|exotic.?sphere|eells.?kuiper|kervaire.?milnor|milnor.?sphere)' \
  Formalizations/Lean/.lake/packages/mathlib/Mathlib \
  Formalizations/Lean/.lake/packages/batteries/Batteries

sed -n '45,85p' \
  Formalizations/Lean/.lake/packages/mathlib/Mathlib/Geometry/Manifold/PoincareConjecture.lean
rg -n -C 5 'withoutModifyingEnv|syntax.*proof_wanted|elab.*proof_wanted' \
  Formalizations/Lean/.lake/packages/batteries/Batteries/Util/ProofWanted.lean
rg -n -i -C 3 'future work|bordism group|bordisms' \
  Formalizations/Lean/.lake/packages/mathlib/Mathlib/Geometry/Manifold/Bordism.lean
git -C Formalizations/Lean/.lake/packages/mathlib log --all \
  -S'exists_homeomorph_isEmpty_diffeomorph_sphere_seven' \
  --format='%H %cI %s' -- Mathlib/Geometry/Manifold/PoincareConjecture.lean

rg -n '\b(sorry|admit|sorryAx|native_decide|implemented_by)\b|^[[:space:]]*(axiom|constant|opaque|unsafe|extern|external)([[:space:]]|$)' \
  Stage1_Instances/THM-M-0578 --glob '*.lean'

git diff --name-status a60b47b4551b044fd5fad26599908ccef4000024..HEAD -- \
  Stage1_Instances/THM-M-0578/Statement.lean \
  Stage1_Instances/THM-M-0578/ObligationTree.lean \
  Stage1_Instances/THM-M-0578/ProofBlockerProbe.lean \
  Stage1_Instances/THM-M-0578/obligation-registry.json \
  Stage1_Instances/THM-M-0578/typed-graphs.json \
  Stage1_Instances/THM-M-0578/anchor-audit.json \
  Stage1_Instances/THM-M-0578/validation-specs.json \
  Stage1_Instances/THM-M-0578/statement.json \
  Docs/Stage1_Targets_rev-5.6.json \
  skills/execute-stage1-rev56/SKILL.md \
  Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json
git diff --name-status a60b47b4551b044fd5fad26599908ccef4000024..HEAD -- \
  Stage1_Instances/THM-M-0578
```

The prerequisite and forbidden-construct searches each returned the recorded
expected no-match exit `1`; all other commands above returned `0`. Final
artifact checks used this exact recipe after the paired files were written:

```bash
set -euo pipefail
json=Stage1_Instances/THM-M-0578/proof-recheck-2026-07-15-head-b1a5b03c-slot60.json
markdown=Stage1_Instances/THM-M-0578/proof-recheck-2026-07-15-head-b1a5b03c-slot60.md
python3 -m json.tool "$json" >/dev/null
set +e
git diff --no-index --check /dev/null "$json"
json_diff_exit=$?
git diff --no-index --check /dev/null "$markdown"
markdown_diff_exit=$?
rg -n '\b(sorry|admit|sorryAx|native_decide|implemented_by)\b|^[[:space:]]*(axiom|constant|opaque|unsafe|extern|external)([[:space:]]|$)' \
  Stage1_Instances/THM-M-0578 --glob '*.lean'
forbidden_exit=$?
set -e
test "$json_diff_exit" -eq 1
test "$markdown_diff_exit" -eq 1
test "$forbidden_exit" -eq 1
git diff --check -- Stage1_Instances/THM-M-0578
test ! -e .stage1-worker-selftest.json
```

## Retry Condition

Resume after placeholder-free implementations of `M0578-C-BUNDLE`,
`M0578-T-HOMEO`, and `M0578-O-NONDIFF` with their frozen child obligations.
Alternatively, integrate an immutable compatible Lean 4 proof-bearing
declaration of the exact root with a complete dependency lock, license record,
and terminal-body provenance, then rerun node-scoped exact-type, trust,
provenance, and composition checks.

This is well beyond five unresolved root-level execution ticks. The integration
lane should schedule dependency-legal child proof tasks rather than another
discovery-only root recheck; this worker does not change the authoritative DAG.

This current-base artifact is nonrelease blocker evidence. It is not a proof
receipt, does not satisfy `S56-M-0578-PROOF`, proposes no state change, and
supports neither root closure nor theorem completion. Because the assigned
proof phase is incomplete, `.stage1-worker-selftest.json` is intentionally
absent.
