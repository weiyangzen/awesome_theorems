# THM-M-0468 proof phase: current-base blocker

Item: `S56-M-0468-PROOF`

Base revision: `71bcc40e66b043742dafd4e66c6a868ff2b2a6ad`

Base tree: `741fca489134e06814154a72672b15212ec28c19`

Validated: `2026-07-15T08:49:51+08:00` (`Asia/Shanghai`)

## Verdict

`blocked`: the exact frozen Lean target has a kernel-checked negation, so no
consistent positive proof body can inhabit it. The proof item remains `[ ]`.
No proof completion, provisional item state, validation, release, theorem
completion, receipt acceptance, or master acceptance is claimed. A root
`.stage1-worker-selftest.json` is deliberately absent.

`Statement.lean` quantifies over every `BogomolovData`, but that structure has
no laws relating its operations and predicates to abelian geometry. The
placeholder-free `ProofBlocker.lean` supplies singleton carriers for which all
ambient hypotheses and density claims are true while `isTorsionPoint` is false
everywhere. Trust-zero Lean checks the exact declaration

```text
Stage1Instances.THM_M_0468.not_bogomolovTarget :
  Not Stage1Instances.THM_M_0468.BogomolovTarget
```

The declaration is sorry-free and depends only on `propext`,
`Classical.choice`, and `Quot.sound`. This refutes only the overbroad abstract
encoding, not the mathematical Ullmo--Zhang theorem. The conditional
`root_of_direction_packages` theorem assumes both missing implications and
therefore supplies no positive proof-body credit.

The first workflow failure is also unchanged: the authoritative predecessor
`S56-M-0468-OBLIGATION_TREE` is only worker-provisional `[_]`, not accepted
`[x]`. Independently, the first semantic proof failure is exact-target
consistency at `M0468-S-DOMAINS`.

## Retry Condition

Reopen `S56-M-0468-STATEMENT`. Replace the unconstrained semantic record with
concrete pinned definitions, or add source-justified noncircular compatibility
laws connecting height, torsion, translation, subvariety membership, and
Zariski density. The repair must rule out the countermodel without assuming
either direction of the desired equivalence. It must also add the rev-5.6
changed-domain, binder-scope, and boundary-case mutations absent from the
current four predicate-removal mutations. Then freeze a new expression and
registry and rerun statement, anchor audit, obligation tree, and proof phases
in dependency order.

## Scoped Validation

All commands ran in this worker clone. The automation-provided untracked
`.lake` symlink to the canonical pinned artifacts was reused read-only. No
`lake update`, `lake build`, dependency clone/fetch, checkout repair, network
command, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0468` | 0 | Rank 314; lane `hard_mathlib_anchor_and_wrapper`; lifecycle `planned`; target incomplete. |
| `git status --short` | 0 | Before this packet, only the automation-provided `?? Formalizations/Lean/.lake` symlink was present. |
| `LEAN_NUM_THREADS=1 timeout 300 python3 Stage1_Instances/THM-M-0468/check_statement.py` | 0 | Fingerprint `def6574c...fa0e`; the four recorded predicate-removal mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-0468/check_anchor_audit.py` | 0 | Target fingerprint, exact pin, module hash, and four candidate classifications passed. |
| `python3 Stage1_Instances/THM-M-0468/check_obligation_tree.py` | 0 | 20 obligations and 44 typed edges passed; denominator `0b324115...6c4`; root remains open at `M4`. |
| Direct pinned `lake env lean --trust=0` recipe below | 0 | Exact target and negation elaborated; `assert_no_sorry` reported `Declarations are sorry-free!`; axioms were `[propext, Classical.choice, Quot.sound]`. |
| `rg -n '\\b(sorry|admit|sorryAx|native_decide)\\b|^[[:space:]]*(axiom|unsafe|external)[[:space:]]'` over `Statement.lean`, `ObligationTree.lean`, and `ProofBlocker.lean` | 1 | No matches; exit 1 is ripgrep's expected no-match result. |
| `python3 -m json.tool Stage1_Instances/THM-M-0468/proof-blocker-head-71bcc40e-slot43-2026-07-15.json` | 0 | The structured blocker packet parsed successfully. |
| `git diff --no-index --check /dev/null FILE` for each new packet | 1 each | Expected new-file differences with empty diagnostics; no whitespace errors. |

Exact narrow Lean recipe, run from the repository root:

```bash
set -euo pipefail
root=$PWD
tmp=$(mktemp -d /tmp/thm-m-0468-71bcc40e-slot43.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp "$root/Stage1_Instances/THM-M-0468/Statement.lean" "$tmp/Statement.lean"
cp "$root/Stage1_Instances/THM-M-0468/ProofBlocker.lean" \
  "$tmp/ProofBlocker.lean"
printf '%s\n' \
  'import ProofBlocker' \
  'import Mathlib.Util.AssertNoSorry' \
  '' \
  '#check Stage1Instances.THM_M_0468.BogomolovTarget' \
  '#check Stage1Instances.THM_M_0468.not_bogomolovTarget' \
  'assert_no_sorry Stage1Instances.THM_M_0468.not_bogomolovTarget' \
  '#print sorries Stage1Instances.THM_M_0468.not_bogomolovTarget' \
  '#print axioms Stage1Instances.THM_M_0468.not_bogomolovTarget' \
  > "$tmp/Probe.lean"
cd "$root/Formalizations/Lean"
LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -R "$tmp" \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp" timeout 300 lake env lean --trust=0 \
  -R "$tmp" -o "$tmp/ProofBlocker.olean" "$tmp/ProofBlocker.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp" timeout 300 lake env lean --trust=0 \
  -R "$tmp" -o "$tmp/Probe.olean" "$tmp/Probe.lean"
sha256sum "$tmp/Statement.olean" "$tmp/ProofBlocker.olean" \
  "$tmp/Probe.olean"
```

The temporary olean hashes were
`19af297ff7259ebbe1b3c4ed1d3c7e9afd3c6ec4e05cd985d9baac027f2e8bbd`,
`96b8c09c90c07271ec8af33ff6240ac2eb7be9ed4bdc6013a0dd865efe376a1d`,
and `8de5e73e3fde29b061539621fbfad13d708bb6e538450ea9743fc715904c0f46`.
The trap removed every temporary artifact.

Pinned identities are Lean `4.29.0` at
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake
`5.0.0-src+98dc76e`, and mathlib commit/tree
`8a178386ffc0f5fef0b77738bb5449d50efeea95` /
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

This is actionable negative kernel evidence under the owned path, not a proof
receipt or a state-transition claim.
