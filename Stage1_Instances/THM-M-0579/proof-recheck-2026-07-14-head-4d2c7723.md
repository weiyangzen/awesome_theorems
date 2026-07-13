# THM-M-0579 proof-phase recheck at base 4d2c7723

Item: `S56-M-0579-PROOF`

Intent: `prove`

Recheck date: 2026-07-14 (Asia/Shanghai)

Base revision: `4d2c77230343716176b4192dc38e26f4c20c7547`

Base tree: `9eebdfdfda6b289fea0b6e778fae8e13327395b2`

## Verdict

`blocked`. The pinned closure contains no eligible retained Lean 4 proof body
for the exact frozen proposition `Stage1Instances.THMM0579.Statement`. No proof
source was added. The proof item stays `[ ]`, the lifecycle stays `planned`,
the root vector stays `[H3, M3, R4]`, and neither audit nor theorem completion
is claimed. Because the positive proof phase is not complete,
`.stage1-worker-selftest.json` is intentionally absent.

Independently, this attempt cannot support worker acceptance because an excluded
auxiliary command violated the no-fetch policy as disclosed below. The
mathematical proof-body gate had already failed and remains the first theorem
gate.

The first failed gate is terminal proof-body availability. The immediate frozen
root cut contains `M0579-T-RECOGNITION` and `M0579-T-RIGIDITY`; neither package
has an inhabitant. Seven intended recognition dependencies are prose-level
planned targets rather than executable Lean contracts. The checked theorem
`root_of_recognition_and_rigidity` consumes both broad packages as premises and
does not construct either one.

A disposable trust-zero probe proves
`Statement.{u} ↔ (HomotopySphereRecognition.{u} ∧
HomotopySphereTopologicalRigidity.{u})`. A root homeomorphism supplies
recognition through `Homeomorph.toHomotopyEquiv`, and it supplies rigidity by
ignoring the extra homotopy-equivalence premise. Thus the frozen cut is
logically equivalent to the root, not a difficulty-reducing proof
decomposition. Correcting it requires an append-only obligation-registry
revision by the obligation-tree authority; this proof worker did not silently
change that frozen architecture.

Pinned mathlib contains the matching names only as Batteries `proof_wanted`
markers elaborated under `withoutModifyingEnv` and discarded. Trust-zero
`#check_failure` probes confirm that the generalized, topological, and smooth
names are absent after import. A scoped retained-declaration search found no
alternate body. The immutable external candidates frozen in
`anchor-audit.json` contain either a three-dimensional statement with an
unrelated dimension-zero proof or an explicit placeholder. Neither is eligible
for integration or proof credit.

## Validation Evidence

All retained validation output was confined to a disposable
`/tmp/thm-m-0579-proof-slot36-4d2c7723.*` directory and removed after
validation. The automation-provided untracked canonical `.lake` symlink was
reused read-only, making this nonrelease evidence. No `lake update`, `lake
build`, checkout, or canonical `.lake` mutation was performed.

One auxiliary `/tmp` `lake env` smoke probe accidentally discovered a
pre-existing `/tmp/lakefile.toml` and printed that it was starting a moving
mathlib clone. It was interrupted immediately with exit 130; no package
checkout remained in `/tmp/.lake/packages`. That command is excluded from all
proof evidence, but its attempted network/dependency action makes this worker
run noncompliant with the no-fetch policy and is reported as a known failure.
The successful replay below used the pinned binary and already present compiled
package directories directly, without Lake dependency resolution.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0579` | 0 | Rank 114; planned hard-mathlib lane; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0579/check_obligation_tree.py` | 0 | 16 obligations and 34 typed edges passed; denominator `984bcfffcea5afa7c11e3f2eb78ad31c2eed6b99e1a0913496186ceb1595776f`; root M3 and both cut packages M4 |
| `python3 Stage1_Instances/THM-M-0579/check_anchor_audit.py` | 0 | Frozen target, five candidates, discarded `proof_wanted` boundary, dependency pins, and noncompletion status agreed |
| Isolated existing-artifact `lean --trust=0` replay | 0 | `Statement.lean`, `ObligationTree.lean`, and the cut-equivalence probe elaborated; the checked composition declarations report only `propext`, `Classical.choice`, and `Quot.sound` |
| Trust-zero `#check_failure` probes | 0 | All three matching mathlib proof names reported `Unknown constant` |
| Forbidden-construct scan of checked owned Lean sources | 1 | Expected ripgrep no-match result for `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, `native_decide`, and `external` |
| Scoped retained-declaration search | 1 | Expected ripgrep no-match result for a retained matching sphere-three proof declaration |
| `$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| Pinned revision and source-hash checks | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, Batteries `756e3321fd3b02a85ffda19fef789916223e578c`, and all recorded proof inputs matched |
| `cd Formalizations/Lean && lake env lean --version` | 1 | Existing canonical `.lake/packages/flt-regular` is incomplete and has `HEAD` at `refs/heads/.invalid`; recorded as a missing pinned artifact rather than fetched or repaired |
| `cd /tmp && ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean --trust=0 /tmp/LakeEnvSmoke.lean` | 130 | Excluded failed smoke probe: a pre-existing `/tmp/lakefile.toml` caused Lake to announce a moving mathlib clone; command was interrupted immediately and retained no checkout |
| `git diff 796a8177..HEAD --quiet -- <six proof inputs>` | 0 | Statement, composition, registry, typed graphs, anchor audit, and validation specs are unchanged since the last integrated recheck |

The successful isolated elaboration recipe was:

```bash
set -euo pipefail
repo_root=$PWD
target=$repo_root/Stage1_Instances/THM-M-0579
package_root=$repo_root/Formalizations/Lean/.lake/packages
mathlib_olean=$package_root/mathlib/.lake/build/lib/lean
lean=$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean
tmp=$(mktemp -d /tmp/thm-m-0579-proof-slot36-4d2c7723.XXXXXX)
trap 'rm -rf "$tmp" /tmp/ProofAvailabilityProbe.lean' EXIT
lean_path=""
for package in Cli batteries Qq aesop proofwidgets importGraph LeanSearchClient plausible; do
  dir=$package_root/$package/.lake/build/lib/lean
  if test -d "$dir"; then lean_path="$lean_path${lean_path:+:}$dir"; fi
done
lean_path="$lean_path:$mathlib_olean:$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean"
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  -o "$tmp/ObligationTree.olean" ObligationTree.lean
cd /tmp
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  ProofAvailabilityProbe.lean
```

This bypass used only the already present pinned toolchain and compiled package
directories because the root Lake environment could not resolve the incomplete,
unrelated `flt-regular` checkout. It did not write to `.lake` or manufacture a
replacement dependency.

The disposable probe's material declaration was:

```lean
theorem proofAvailabilityProbe_cut_iff_root :
    Statement.{u} ↔
      HomotopySphereRecognition.{u} ∧
        HomotopySphereTopologicalRigidity.{u} := by
  constructor
  · intro root
    constructor
    · intro M _ _ _ _ _
      rcases root M with ⟨homeomorph⟩
      exact ⟨homeomorph.toHomotopyEquiv⟩
    · intro M _ _ _ _ _ _
      exact root M
  · rintro ⟨recognition, rigidity⟩
    exact root_of_recognition_and_rigidity recognition rigidity
```

It also printed the declaration's axioms and used `#check_failure` for the
three absent proof names. The exact negative scans were:

```bash
rg -n --pcre2 '\b(sorry|admit|axiom|sorryAx|unsafe|implemented_by|native_decide|external)\b' \
  Stage1_Instances/THM-M-0579/{Statement.lean,AnchorAudit.lean,ObligationTree.lean}

rg -n --pcre2 \
  '^(?:public\s+)?(?:theorem|lemma|def|opaque|abbrev)\s+(?:[A-Za-z0-9_]+\.)*(?:nonempty_homeomorph_sphere_three|nonempty_diffeomorph_sphere_three|nonempty_homeomorph_sphere)(?:\s|\[|:)' \
  Stage1_Instances Formalizations/Lean/AwesomeTheorems \
  Formalizations/Lean/.lake/packages/mathlib/Mathlib \
  Formalizations/Lean/.lake/packages/batteries/Batteries
```

Both exit with 1, ripgrep's expected no-match status. Proof-relevant hashes at
this attempt were:

```text
Statement.lean              307061f5847f145fb8cb4e91116ed8ab0c76e3ddc0e9301486fd879be1cf3de8
ObligationTree.lean         f5214263374c23fd2f235cdf4d06bc9cadfd50d4abbe41de32dd55a7e35f0c63
obligation-registry.json    8b70a187e8d4e071c3a658f8b5d8d31fb78dcb2fabc1bedeeddca3fd4c62b31a
typed-graphs.json           e8a756448de68ee250734fc480a06bd3fc55f1827f6da5a847b6bd31677ddce7
anchor-audit.json           0285a80d4d59466d71fdd1d163e1c6a09f7a96b1d0372ea8f682fd69c251f7e7
validation-specs.json       353bdfdcd8341bb9bbd3b3c324b634804144b119ed0b8d0ed161e28d222074aa
```

## Retry Condition

First publish a versioned, non-tautological, executable obligation-registry
revision. Then implement its terminal packages without placeholders, or
integrate a licensed immutable Lean 4 proof with a compatible dependency lock
and exact checked transport to the canonical root. The result must pass kernel,
exact-type, composition, axiom, placeholder, provenance, trust, and pinned
replay gates. Restore the already pinned `flt-regular` artifact before any
root-Lake validation, without updating or fetching it inside a worker run.
Assuming a package, treating `proof_wanted` as a theorem, or proving a
conditional or special case would substitute a different theorem.

This owned artifact is a blocker record, not a proof receipt. It does not
satisfy `S56-M-0579-PROOF`, change scheduler state, or claim audit completion,
theorem completion, release, or master acceptance.
