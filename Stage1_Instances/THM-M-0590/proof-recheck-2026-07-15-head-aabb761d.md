# THM-M-0590 proof phase blocked at `aabb761d`

Item: `S56-M-0590-PROOF`

Intent: `prove`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `aabb761d975829b09920d981edc8220edb90e8c3`

Base tree: `a988020866eb03a08cd23d18d5e7711cb5d03742`

## Verdict

`blocked`. No eligible proof body closes the exact frozen Lean target. The
target is the full Brown-Douglas-Fillmore classification of essentially normal
bounded operators on separable infinite-dimensional complex Hilbert spaces by
essential spectrum and the off-spectrum Fredholm-index function.

The placeholder-free local theorem `root_of_directional_packages` elaborates
under `--trust=0`, but it consumes `ForwardInvariantPackage` and
`BackwardClassificationPackage`. Those parameters are exactly the two missing
directional mathematical proofs. The declaration checks final biconditional
composition; it proves neither direction and is not an unconditional inhabitant
of `brownDouglasFillmoreTarget`.

Pinned mathlib has compact-operator, adjoint, and ordinary-spectrum support, but
the bounded source search retains no Calkin-algebra, general Fredholm-index,
essential-spectrum, Busby-extension, or BDF-classification implementation. A
repo-local Lean search likewise retains no unconditional body outside this
dossier. The predecessor anchor audit found no exact immutable external Lean 4
candidate; its authenticated GitHub code-search lane was unavailable, so this
record does not claim global nonexistence.

No premise, axiom, placeholder, weaker target, altered convention, or moving
dependency was added. The proof item remains `[ ]`; the root stays
`[H1, M4, R3]`. No audit, validation, release, theorem-completion, receipt, or
master-acceptance claim is made. Because the requested proof phase is not
complete, `.stage1-worker-selftest.json` is deliberately absent.

## Failed Gate And Retry

The first failed gate is terminal proof-body availability for
`M0590-B-FORWARD` and `M0590-T-BACKWARD`; these two obligations are the
remaining root cut set. The frozen route still requires Calkin and Atkinson
bridges, forward invariance of essential spectrum and Fredholm index, Busby
extensions, BDF extension classification, and completeness of the index
invariant.

Resume after these obligations have local placeholder-free Lean
implementations, or after an independently audited immutable compatible Lean 4
dependency supplies both exact directional packages plus kernel-checked
exact-type, provenance, axiom, placeholder, composition, and pinned-replay
evidence. A citation or conditional composer does not satisfy this condition.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to the canonical pinned artifacts was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake`
mutation was performed. Temporary Lean objects were created under `/tmp` and
removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0590` | 0 | Rank 630; lifecycle `planned`; lane `hard_statement_first_partial_verification`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0590/check_obligation_tree.py` | 0 | 17 obligations and 37 typed edges passed; denominator `2d5b17d162ed0ef7a445673a25243da41d3aeb4a2be8f39eab68511e1809a9e8`; root and both directional packages remain M4. |
| Isolated `lake env lean --trust=0 -t0` replay of `Statement.lean` and `ObligationTree.lean` with a temporary `Statement.olean` | 0 | The exact target and conditional composition elaborated; the target printed `THMM0590.brownDouglasFillmoreTarget.{u_2, u_3} : Prop`, and `#print axioms` reported `[propext, Classical.choice, Quot.sound]`. |
| `rg -n '^\s*(sorry\|admit\|axiom)(\s\|$)\|sorryAx' Stage1_Instances/THM-M-0590 --glob '*.lean'` | 1 (expected) | No prohibited Lean proof escape occurs in owned sources. |
| Scoped repo-local Lean search for the canonical target and directional package names outside this dossier | 1 (expected) | No retained unconditional root or directional-package body was found. |
| `rg -n -i 'Brown.?Douglas.?Fillmore\|Calkin\|essentialSpectrum\|essential spectrum\|IsFredholm\|fredholmIndex\|essentiallyNormal\|essentially normal\|Busby' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 (expected) | No matching target or missing central API was found in the pinned mathlib source. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` plus `status --porcelain=v1` | 0 | Revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`, clean dependency worktree. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `python3 -m json.tool Stage1_Instances/THM-M-0590/proof-recheck-2026-07-15-head-aabb761d.json >/dev/null` plus current-base invariant assertions | 0 | JSON parsed; item, base, source hashes, denominator, cut set, open state, empty receipts, changed paths, and deliberate self-test absence agree. |
| Owned-path and normalized added-file whitespace checks | 0 | No whitespace diagnostics in either current blocker artifact. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no completion manifest. |

The exact narrow Lean replay recipe was:

```bash
TMP=$(mktemp -d /tmp/thm-m-0590-proof-aabb761d.XXXXXX)
LEAN=$(cd Formalizations/Lean && lake env which lean)
LP=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
(cd Stage1_Instances/THM-M-0590 &&
  LEAN_NUM_THREADS=1 LEAN_PATH="$LP" timeout 600 "$LEAN" --trust=0 -t0 \
    -o "$TMP/Statement.olean" Statement.lean)
(cd Stage1_Instances/THM-M-0590 &&
  LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$LP" timeout 600 "$LEAN" --trust=0 -t0 \
    ObligationTree.lean)
rm -rf "$TMP"
```

Exact input hashes, structured outcomes, the open cut set, and the retry
condition are recorded in
`proof-recheck-2026-07-15-head-aabb761d.json`. This is durable current-base
blocker evidence, not a proof receipt.
