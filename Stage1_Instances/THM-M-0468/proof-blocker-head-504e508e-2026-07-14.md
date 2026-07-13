# THM-M-0468 proof phase: current-base blocker

Item: `S56-M-0468-PROOF`

Base revision: `504e508e93fd30c552d715ef48be068d5e131df2`

Base tree: `745f1603c60b7bb726e7789f08a6170c82621b6a`

Rechecked: `2026-07-14T04:08:15+08:00`

## Verdict

`blocked`: no consistent positive proof body can inhabit the exact frozen Lean
target. The proof item remains `[ ]`; no proof, provisional state, audit
completion, validation, release, theorem completion, or master acceptance is
claimed. A root `.stage1-worker-selftest.json` is deliberately absent.

`Statement.lean` quantifies over every `BogomolovData`, but the structure has no
laws connecting its operations and predicates to abelian geometry. The
placeholder-free `ProofBlocker.lean` supplies a permitted singleton model in
which every ambient hypothesis and density claim is true while
`isTorsionPoint` is false everywhere. Trust-zero Lean checks

```text
Stage1Instances.THM_M_0468.not_bogomolovTarget :
  Not Stage1Instances.THM_M_0468.BogomolovTarget
```

A positive proof of the frozen target would contradict that theorem. This
refutes only the overbroad formal encoding, not the mathematical Ullmo--Zhang
theorem. The fail-closed proposal is `[H1, M4, R3] -> [H1, M5, R3]`, subject to
master reconciliation. The checked `root_of_direction_packages` declaration
assumes both missing implications, and the pinned anchor inventory contains no
exact eligible proof body.

## Failed gates

The first workflow failure is prerequisite acceptance:
`S56-M-0468-OBLIGATION_TREE` is only worker-provisional `[_]`, not
master-accepted `[x]`. Independently, the first semantic proof failure is
exact-target consistency at `M0468-S-DOMAINS`. Positive work may resume only
after a statement repair replaces the unconstrained semantic surfaces with
concrete pinned definitions or source-justified, noncircular compatibility
laws. Those laws must cover height and torsion, translation, subvariety
membership, and Zariski density without assuming either direction of the
desired equivalence.

The predecessor statement evidence is independently incomplete. Its checker
kills four removed-predicate mutations, while rev-5.6 section 5.1 also requires
a changed domain, changed binder scope, and boundary case. The dossier still
leaves `X = A` and zero-dimensional behavior open.

Repairing the statement invalidates its expression fingerprint and the frozen
proof architecture. A new statement fingerprint and obligation-registry
version must pass fresh statement, anchor-audit, obligation-tree, and proof
phases in dependency order.

## Scoped validation

All commands ran in this worker clone. The automation-provided symlink to the
canonical pinned `.lake` artifacts was reused read-only. No `lake update`,
`lake build`, dependency clone/fetch, checkout repair, or `.lake` mutation was
performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0468` | 0 | Rank 314; lane `hard_mathlib_anchor_and_wrapper`; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0468/check_statement.py` | 0 | Fingerprint `def6574...fa0e`; four recorded predicate-removal mutations killed. |
| `python3 Stage1_Instances/THM-M-0468/check_anchor_audit.py` | 0 | Target fingerprint, exact pin, module hash, and four candidate classifications passed. |
| `python3 Stage1_Instances/THM-M-0468/check_obligation_tree.py` | 0 | 20 obligations and 44 typed edges passed; denominator `0b324115...6c4`; root remains open at `M4`. |
| Direct `lake env lean` trust-zero replay below | 0 | The copied target and its negation elaborated; `assert_no_sorry` succeeded; `#print sorries` reported `Declarations are sorry-free!`; `#print axioms` reported `[propext, Classical.choice, Quot.sound]`. |
| Isolated pinned-executable replay of `Statement.lean` and `ObligationTree.lean` | 0 | Conditional composition elaborated; its axiom report was `[propext, Classical.choice, Quot.sound]`. |
| `rg -n '\b(sorry\|admit\|sorryAx\|native_decide)\b\|^[[:space:]]*(axiom\|unsafe\|external)[[:space:]]'` over the three checked Lean sources | 1 | No forbidden construct; exit 1 is ripgrep's expected no-match result. |

Exact direct `lake env lean` recipe:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-0468-slot33.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-0468/Statement.lean "$tmp/Statement.lean"
cp Stage1_Instances/THM-M-0468/ProofBlocker.lean "$tmp/ProofBlocker.lean"
printf '%s\n' \
  'import ProofBlocker' \
  'import Mathlib.Util.AssertNoSorry' \
  '' \
  'open Stage1Instances.THM_M_0468' \
  '' \
  'assert_no_sorry not_bogomolovTarget' \
  '#print sorries not_bogomolovTarget' \
  '#print axioms not_bogomolovTarget' > "$tmp/NoSorry.lean"
(cd Formalizations/Lean &&
  LEAN_NUM_THREADS=1 lake env lean --trust=0 -R "$tmp" \
    -o "$tmp/Statement.olean" "$tmp/Statement.lean")
(cd Formalizations/Lean &&
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp" lake env lean --trust=0 -R "$tmp" \
    -o "$tmp/ProofBlocker.olean" "$tmp/ProofBlocker.lean")
(cd Formalizations/Lean &&
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp" lake env lean --trust=0 -R "$tmp" \
    "$tmp/NoSorry.lean")
```

All temporary validation outputs were removed by traps. Pinned identities and
source hashes:

- Lean `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`
- mathlib commit/tree `8a178386ffc0f5fef0b77738bb5449d50efeea95` / `bdc39a3123201dae413a9d9be56ec242c19e5c2b`
- `Statement.lean`: `84151eb96c1159df08e882934dfc3b8652b1bb38cf150a521c09708a727dbc8c`
- `ProofBlocker.lean`: `e33f59eb5ed7ce49ab14b70e61c3e1306252cfdee25ca464a4128b2e029695e0`
- `ObligationTree.lean`: `23161c5fd3e4d4dd9a7d7b04f214cdda3531cc83a166fd730477306d37911504`
- `obligation-registry.json`: `86343feb231abc043e94742999b9a6457aaa92ed814749fa73f85f883d6692ed`
- `typed-graphs.json`: `2194c66bdcc18f7e2728859720a56f8c36f1a4e2f9054d3e53a7856551f9f62b`
- `anchor-audit.json`: `6ed5638e5bd32073aeed2014d08be820c38f28805ba926676f8521b3b45b8937`

The pre-existing untracked `.lake` symlink makes this nonrelease evidence.
Retry only after the statement is repaired and re-fingerprinted and every
invalidated predecessor is rerun. This packet is an actionable blocker, not a
proof receipt or item-state claim.
