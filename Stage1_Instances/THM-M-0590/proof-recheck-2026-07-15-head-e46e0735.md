# THM-M-0590 proof phase blocked at `e46e0735`

Item: `S56-M-0590-PROOF`

Intent: `prove`

Recheck time: `2026-07-15T07:54:40+08:00`

Base revision: `e46e0735d0940bb558acaf027d8386de2579f55d`

Base tree: `9f03ecc77e82eda1f0ea3f0f4b08d1d7419ce0cf`

## Verdict

`blocked`. No eligible proof body closes the exact frozen Lean target. The
target is the full Brown-Douglas-Fillmore classification of essentially normal
bounded operators on separable infinite-dimensional complex Hilbert spaces by
essential spectrum and the off-spectrum Fredholm-index function.

The placeholder-free theorem `THMM0590.root_of_directional_packages` checks
under `--trust=0`, but it consumes `ForwardInvariantPackage` and
`BackwardClassificationPackage`. Those parameters contain exactly the two
missing directional BDF proofs. The declaration checks final biconditional
composition; it does not inhabit `brownDouglasFillmoreTarget` unconditionally.

Pinned mathlib supplies compact-operator, adjoint, ordinary-spectrum, and
compact-operator Fredholm-alternative support, but the bounded source search
found no Calkin-algebra, general Fredholm-index, essential-spectrum,
Busby-extension, or BDF-classification implementation. A scoped repo-local
Lean search likewise found no unconditional body outside this dossier. The
predecessor anchor audit retained no exact immutable external Lean 4 candidate.
A fresh bounded Sourcegraph query found no `BrownDouglasFillmore` occurrence;
its `Calkin` matches were substring false positives in an unrelated repository.
These bounded results do not establish global nonexistence.

No premise, axiom, placeholder, weaker target, altered convention, or moving
dependency was added. The proof item remains `[ ]`; the root stays
`[H1, M4, R3]`. No proof, validation, release, theorem-completion, receipt, or
master-acceptance claim is made. Because the requested proof phase is not
complete, `.stage1-worker-selftest.json` is deliberately absent.

## Failed Gate And Retry

The first failed gate is terminal proof-body availability for
`M0590-B-FORWARD` and `M0590-T-BACKWARD`; these obligations are the remaining
root cut set. The frozen route still requires Calkin and Atkinson bridges,
forward invariance of essential spectrum and Fredholm index, Busby extensions,
BDF extension classification, and completeness of the index invariant.

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
| `python3 scripts/stage1_target.py show THM-M-0590` | 0 | Rank 630; lifecycle `planned`; hard-statement-first lane; legacy artifacts unaccepted; theorem incomplete. |
| `git status --short` | 0 | Before this recheck, only the automation-provided untracked `Formalizations/Lean/.lake` symlink was present. |
| `python3 Stage1_Instances/THM-M-0590/check_obligation_tree.py` | 0 | 17 obligations and 37 typed edges passed; denominator `2d5b17d162ed0ef7a445673a25243da41d3aeb4a2be8f39eab68511e1809a9e8`; root and both directional packages remain M4. |
| Isolated `lake env lean --trust=0 -t0` replay of `Statement.lean` and `ObligationTree.lean` with temporary olean outputs | 0 | The exact target and conditional composition elaborated; the target printed `THMM0590.brownDouglasFillmoreTarget.{u_2, u_3} : Prop`, and the composer reported axioms `[propext, Classical.choice, Quot.sound]`. All temporary outputs were removed. |
| Prohibited-construct scan shown below | 1 (expected) | No prohibited Lean proof escape, bodyless declaration, or executable oracle construct occurs in owned Lean sources. |
| Repo-local proof-body search shown below | 1 (expected) | No retained unconditional root or directional-package body was found outside this dossier. |
| Pinned-mathlib API search shown below | 1 (expected) | No matching target or missing central API was found in pinned mathlib source. |
| Frozen-registry `jq` assertion shown below | 0 | The 15 required obligations comprise 14 without terminal bodies and one conditional composition body at `M0590-T-ASSEMBLE`. |
| Bounded Sourcegraph global Lean queries | 0 | `BrownDouglasFillmore` returned zero matches; `Calkin` returned only substring false positives unrelated to operator algebras. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` plus `status --porcelain=v1` | 0 | Revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`, clean dependency worktree. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release; Lake 5.0.0-src+98dc76e. |
| `python3 -m json.tool Stage1_Instances/THM-M-0590/proof-recheck-2026-07-15-head-e46e0735.json` plus current-base invariant assertions | 0 | JSON parsed; item, theorem, base revision/tree, open state, empty receipts, root cut set, changed paths, and deliberate self-test absence agree. |
| Owned-path and normalized added-file whitespace checks | 0 | No whitespace diagnostics in either current blocker artifact. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no completion manifest. |

The exact narrow Lean replay recipe was:

```bash
TMP=$(mktemp -d /tmp/thm-m-0590-proof-e46e0735.XXXXXX)
LEAN=$(cd Formalizations/Lean && lake env which lean)
LP=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
(cd Stage1_Instances/THM-M-0590 &&
  LEAN_NUM_THREADS=1 LEAN_PATH="$LP" timeout 600 "$LEAN" --trust=0 -t0 \
    -o "$TMP/Statement.olean" Statement.lean)
(cd Stage1_Instances/THM-M-0590 &&
  LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$LP" timeout 600 "$LEAN" --trust=0 -t0 \
    -o "$TMP/ObligationTree.olean" ObligationTree.lean)
rm -rf "$TMP"
```

The statement stdout SHA-256 was
`0d23382885fc11411a9519d8e71bc63deaf3bf05623946c21828a00d69c7f14b`;
the conditional-composer stdout SHA-256 was
`05a0a820b771d89fb80dcea388056a6e720a5fd6b046e1cff49db37baf10803a`.

The exact source and placeholder searches were:

```bash
rg -n --glob '*.lean' \
  '(^|[^[:alnum:]_])(sorry|admit|sorryAx|implemented_by|native_decide|unsafe|extern|run_tac)([^[:alnum:]_]|$)|^[[:space:]]*(axiom|constant|opaque)[[:space:]]' \
  Stage1_Instances/THM-M-0590
rg -n 'brownDouglasFillmoreTarget|ForwardInvariantPackage|BackwardClassificationPackage' \
  --glob '*.lean' -g '!Stage1_Instances/THM-M-0590/**' \
  -g '!Formalizations/Lean/.lake/**' .
rg -n -i \
  'Brown.?Douglas.?Fillmore|Calkin|essentialSpectrum|essential spectrum|IsFredholm|fredholmIndex|essentiallyNormal|essentially normal|Busby' \
  Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'
```

The registry assertion was:

```bash
jq -e '([.obligations[] | select(.machine_eligibility == "required")]) as $r |
  (($r | length) == 15 and
   ([$r[] | select(.terminal_proof_body_id == null)] | length) == 14 and
   ([$r[] | select(.terminal_proof_body_id != null)] | length) == 1 and
   ([$r[] | select(.terminal_proof_body_id != null)][0].obligation_id ==
      "M0590-T-ASSEMBLE"))' \
  Stage1_Instances/THM-M-0590/obligation-registry.json
```

Exact structured outcomes, current input hashes, obligation fingerprints, the
open cut set, and the retry condition are recorded in the matching JSON
artifact. This is durable current-base blocker evidence, not a proof receipt.
