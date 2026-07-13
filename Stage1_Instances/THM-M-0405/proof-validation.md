# THM-M-0405 proof-phase validation

Item: `S56-M-0405-PROOF`

Base revision: `4683af33601abf1185b47caafb86ccd3ddc30158`

Base tree: `9b49ee18fec214315592ea125d7049e4ea668740`

## Implemented bodies

`Proof.lean` contains 18 local, placeholder-free theorem bodies making partial
progress toward
`M0405-N-PAIR-NORMALIZATION`, `M0405-T-LUCAS-ADAPTER`, and
`M0405-T-LEHMER-ADAPTER`. They establish:

- nonzero Lucas and Lehmer components from the stored nonzero product;
- distinct components from the nontorsion quotient hypothesis;
- nonzero odd and even quotient denominators;
- both stored discriminant identities over `Complex`; and
- the forced initial values `U₀ = 0`, `U₁ = 1`, `L₁ = 1`, and `L₂ = 1`.

These are genuine algebraic prerequisites, but the frozen nodes are broader
prose-level packages. Therefore zero frozen obligations are claimed closed.
The proof does not produce a primitive prime divisor or establish avoidance of
the discriminant and every earlier positive term.

## Boundary

The first failed root gate remains `M0405-X-BHV-BRIDGE`. The pinned closure has
no terminal BHV or Zsigmondy theorem, and the frozen central route still needs
exact signatures and bodies for the cyclotomic factor, valuation bounds,
large-index exclusion, defective-pair classification, common bridge, and both
exact adapters. `statement_of_branches` consumes the two complete branches and
cannot substitute for them.

The provisional root vector remains `[H1, M4, R3]`;
`root_kernel_closed=false`, `theorem_complete=false`, and this handoff is not theorem completion.
The dated `proof-recheck-*` files are retained as history.

## Commands and exact results

All Lean commands used the existing canonical pinned `.lake` artifacts. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was
performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0405` | 0 | Rank 18, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0405/check_obligation_tree.py` | 0 | `ok: 15 obligations, 30 typed edges, denominator cd9daee4...da793; root open M4` |
| `bash Stage1_Instances/THM-M-0405/check_proof.sh` | 0 | Isolated `Statement -> ObligationTree -> Proof` elaboration with `--trust=0`; 18 exact axiom reports were present once each and used only the allowed foundation profile; receipt, scope, hashes, and open-root boundary passed. |
| `rg -n '\b(sorry|admit|sorryAx|implemented_by|native_decide)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe\|extern)[[:space:]]+' Stage1_Instances/THM-M-0405/Proof.lean` | 1 | Expected no-match exit; no prohibited proof device occurs. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git diff --check -- Stage1_Instances/THM-M-0405 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

`check_proof.sh` writes all `.olean` and audit output only beneath a temporary
`/tmp/stage1-m0405-proof.*` directory and removes it on exit. The pre-existing
untracked `Formalizations/Lean/.lake` symlink is the automation-provided link to
the canonical artifacts and is not part of this change.

## Known prerequisite inconsistencies

The prerequisite tree prose reports 12 human-source-required obligations while
the registry reports 11; several graph nodes name a nonexistent
`obligation-graphs.json`; and the central planned packages have prose targets
rather than exact Lean signatures. This proof phase records those issues but
does not rewrite prerequisite-owned frozen artifacts.
