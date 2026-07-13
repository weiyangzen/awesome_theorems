# THM-M-0468 proof phase: current-base recheck

Item: `S56-M-0468-PROOF`

Base revision: `ffea62ba1a7c0b0f84d70fd07f87d3eef57fe330`

Base tree: `4662e08d189bd534919775f750c6909591aeafcb`

Rechecked: `2026-07-14T02:29:34+08:00`

## Verdict

`blocked`: no consistent positive proof body can inhabit the exact frozen Lean
target. The proof item remains `[ ]`; no proof, provisional state, validation,
release, theorem completion, or master acceptance is claimed. A root
`.stage1-worker-selftest.json` is deliberately absent.

`Statement.lean` quantifies over every `BogomolovData`, but that structure has
no laws connecting its carriers, operations, or predicates to abelian
geometry. The placeholder-free `ProofBlocker.lean` supplies a permitted
singleton interpretation in which every ambient hypothesis and density claim
is true while `isTorsionPoint` is false everywhere. Lean therefore checks

```text
Stage1Instances.THM_M_0468.not_bogomolovTarget :
  Not Stage1Instances.THM_M_0468.BogomolovTarget
```

at trust level zero. A positive proof of the frozen target would contradict
this result. The countermodel refutes only the overbroad abstract encoding, not
the mathematical Ullmo--Zhang theorem. The fail-closed proposal is consequently
`[H1, M4, R3] -> [H1, M5, R3]`, subject to master reconciliation.

The checked `root_of_direction_packages` declaration is conditional: it takes
the two missing implications as premises and supplies no proof body for either.
The anchor audit likewise contains no exact eligible Lean proof body.

## First failed gate

Exact-target consistency fails at `M0468-S-DOMAINS`. The universally quantified
semantic record admits the checked countermodel. Positive execution may resume
only after the statement is replaced by concrete pinned definitions or by
source-justified, noncircular compatibility laws that rule out this model.

That upstream repair invalidates the current statement fingerprint and proof
architecture. The statement phase must also add the changed-domain,
changed-binder-scope, and boundary-case mutations required by rev-5.6 section
5.1; its current checker covers only four removed-predicate mutations. A new
statement fingerprint and obligation-registry version must then pass fresh
statement, anchor-audit, obligation-tree, and proof phases in dependency order.

## Scoped validation

All commands ran in this worker clone. The automation-provided symlink to the
canonical pinned `.lake` artifacts was reused read-only. No `lake update`,
`lake build`, dependency clone/fetch, or `.lake` mutation was performed. The
only pre-existing worktree entry was `?? Formalizations/Lean/.lake`, so this is
nonrelease blocker evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0468` | 0 | Rank 314; lane `hard_mathlib_anchor_and_wrapper`; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0468/check_statement.py` | 0 | Fingerprint `def6574...fa0e`; four recorded predicate-removal mutations killed. |
| `python3 Stage1_Instances/THM-M-0468/check_anchor_audit.py` | 0 | Target fingerprint, exact pin, module hash, and four candidate classifications passed. |
| `python3 Stage1_Instances/THM-M-0468/check_obligation_tree.py` | 0 | 20 obligations and 44 typed edges passed; denominator `0b324115...6c4`; root remains open at `M4`. |
| Isolated pinned Lean recipe below | 0 | The exact target and its negation elaborated with `--trust=0`; `#print axioms` reported `[propext, Classical.choice, Quot.sound]`. |
| `rg -n '\\b(sorry\|admit\|sorryAx\|native_decide)\\b\|^[[:space:]]*(axiom\|unsafe\|external)[[:space:]]' Stage1_Instances/THM-M-0468/ProofBlocker.lean` | 1 | No forbidden construct; exit 1 is ripgrep's expected no-match result. |
| `git diff --check -- Stage1_Instances/THM-M-0468` | 0 | The tracked-diff whitespace check passed. |
| `git diff --no-index --check /dev/null <each new packet file>` | 1 each | Expected new-file difference exit; empty output confirmed no whitespace errors in either untracked packet file. |

Exact narrow Lean recipe:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-0468-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0468/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0468/ProofBlocker.lean "$tmp/ProofBlocker.lean"
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
lean_bin=$(cd Formalizations/Lean && lake env which lean)
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" "$lean_bin" --trust=0 \
  -o Statement.olean Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" "$lean_bin" --trust=0 \
  ProofBlocker.lean
```

The recipe wrote only to a fresh `/tmp` directory and removed it by trap.
Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake
`5.0.0-src+98dc76e`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

This packet is fresh negative kernel evidence only. It supplies no positive
root proof credit and cannot advance the proof item or any downstream phase.
