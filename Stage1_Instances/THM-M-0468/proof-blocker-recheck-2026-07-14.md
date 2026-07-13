# THM-M-0468 proof-phase recheck: blocked

Item: `S56-M-0468-PROOF`  
Base revision: `f3a2545c7e6634696c48f725a9581e7e248c8877`  
Base tree: `a9ade4224e40322a81336ccd63462829ffedc8eb`  
Validation time: `2026-07-14T01:47:20+08:00`

## Verdict

`blocked`: no consistent positive proof body can inhabit the exact frozen Lean target. The
assigned proof item remains `[ ]`; no proof, audit-completion, validation, release,
theorem-completion, or master-acceptance claim is made.

`Statement.lean` quantifies over every value of `BogomolovData`, but that structure contains only
types, operations, and predicates. It states no laws requiring them to model an abelian variety,
canonical height, torsion, translation, or Zariski density. The existing placeholder-free
`ProofBlocker.lean` therefore supplies a valid singleton-carrier countermodel: every ambient
hypothesis and every density assertion is true, while `isTorsionPoint` is false everywhere. Its
theorem

```text
Stage1Instances.THM_M_0468.not_bogomolovTarget :
  Not Stage1Instances.THM_M_0468.BogomolovTarget
```

kernel-checks at trust level zero. A positive root proof together with this theorem would derive
`False`. This negative evidence refutes only the overbroad formal encoding, not the mathematical
Ullmo--Zhang theorem.

The conditional theorem `root_of_direction_packages` cannot repair the issue: it assumes both
directions of the desired equivalence as premises. The frozen anchor audit also identifies no exact
eligible Lean proof body. Its pinned mathlib candidate supplies only supporting abelian-variety
infrastructure, and the external candidates either prove different elliptic-curve height results or
contain placeholders.

## First Failed Gate

The first failed gate is exact-target consistency at `M0468-S-DOMAINS`. Positive proof execution
must not resume until the statement phase replaces the unconstrained semantic record with concrete
pinned definitions or source-justified noncircular compatibility laws. A repaired statement needs
a new fingerprint and obligation-registry version, followed by fresh statement mutations, anchor
audit, obligation-tree construction, and proof execution.

## Scoped Validation

All checks ran in this worker clone. The existing canonical pinned `.lake` artifacts were reused;
no `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed. The Lean
recipe copied the two source files to a fresh `/tmp` directory, wrote `Statement.olean` only there,
and removed the directory on exit.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0468` | 0 | Rank 314; lane `hard_mathlib_anchor_and_wrapper`; lifecycle `planned`; theorem incomplete. |
| Isolated pinned Lean recipe below | 0 | `BogomolovTarget` and `not_bogomolovTarget` elaborated; `#print axioms` reported `[propext, Classical.choice, Quot.sound]`. |
| `python3 Stage1_Instances/THM-M-0468/check_statement.py` | 0 | Exact statement fingerprint `def6574...fa0e`; all four recorded structural mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-0468/check_anchor_audit.py` | 0 | Target fingerprint, exact dependency pin, module hash, and four candidate classifications passed. |
| `python3 Stage1_Instances/THM-M-0468/check_obligation_tree.py` | 0 | 20 obligations and 44 typed edges passed; denominator `0b324115...6c4`; root remains open at `M4`. |
| `rg -n '\b(sorry|admit|sorryAx|native_decide)\b|^[[:space:]]*(axiom|unsafe|external)[[:space:]]' Stage1_Instances/THM-M-0468/ProofBlocker.lean` | 1 | No forbidden construct; exit 1 is ripgrep's expected no-match result. |

Exact narrow Lean recipe, run from the repository root:

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

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Checked source SHA-256 values:

- `Statement.lean`: `84151eb96c1159df08e882934dfc3b8652b1bb38cf150a521c09708a727dbc8c`
- `ProofBlocker.lean`: `e33f59eb5ed7ce49ab14b70e61c3e1306252cfdee25ca464a4128b2e029695e0`
- `ObligationTree.lean`: `23161c5fd3e4d4dd9a7d7b04f214cdda3531cc83a166fd730477306d37911504`
- `obligation-registry.json`: `86343feb231abc043e94742999b9a6457aaa92ed814749fa73f85f883d6692ed`
- `typed-graphs.json`: `2194c66bdcc18f7e2728859720a56f8c36f1a4e2f9054d3e53a7856551f9f62b`
- `anchor-audit.json`: `6ed5638e5bd32073aeed2014d08be820c38f28805ba926676f8521b3b45b8937`

Because the assigned positive proof phase is not genuinely complete,
`.stage1-worker-selftest.json` is deliberately absent. This report is actionable blocker evidence,
not a proof receipt and not a provisional item-state claim.
