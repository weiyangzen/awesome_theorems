# THM-M-0468 proof phase: current-head blocker

Item: `S56-M-0468-PROOF`  
Base revision: `64ac616628d97140f9ca64eff0298e51d7f4e9ff`  
Base tree: `9ef0acd5b747e34cacb82c6f21fce1e1380e0cf2`  
Rechecked: `2026-07-14T02:12:00+08:00`

## Verdict

`blocked`: the exact frozen Lean target cannot consistently receive a positive
proof body. The proof item remains `[ ]`; no proof, provisional state, audit
completion, validation, release, theorem completion, or master acceptance is
claimed.

`Statement.lean` quantifies over every value of `BogomolovData`, but that
structure supplies only carriers, operations, and predicates. It has no laws
requiring them to describe an abelian variety, canonical height, torsion,
translation, or Zariski density. The placeholder-free `ProofBlocker.lean`
therefore constructs a permitted singleton-carrier interpretation in which all
ambient hypotheses and density claims are true while every torsion claim is
false. Lean kernel-checks

```text
Stage1Instances.THM_M_0468.not_bogomolovTarget :
  Not Stage1Instances.THM_M_0468.BogomolovTarget
```

at trust level zero. A positive root proof together with this theorem would
derive `False`. This negative result refutes only the overbroad formal encoding,
not the mathematical Ullmo--Zhang theorem. Accordingly the human-source status
remains `H1`; the proof attempt proposes only the fail-closed machine change
`M4 -> M5`, with readability remaining `R3`.

The checked `root_of_direction_packages` composition does not repair the
target: it assumes both directions of the desired equivalence. The anchor audit
found no exact eligible Lean body. Its pinned mathlib candidate supplies only
supporting infrastructure, while external candidates are statement-mismatched
or contain placeholders.

## First failed gate

The first failed gate is exact-target consistency at `M0468-S-DOMAINS`.
Positive proof execution must not resume until the statement is replaced by
concrete pinned definitions or source-justified noncircular compatibility laws.
That repair requires a new statement fingerprint and obligation-registry
version, followed by fresh statement, anchor-audit, obligation-tree, and proof
phases.

There is also an independent predecessor-gate defect. The existing statement
checker kills four removed-predicate mutations, but rev-5.6 section 5.1 also
requires changed-domain, changed-binder-scope, and boundary-case mutations.
The dossier leaves `X=A` and zero-dimensional behavior open. Thus even without
the countermodel, the predecessor statement evidence cannot authorize proof
acceptance.

## Scoped validation

All commands ran in this worker clone. The existing canonical pinned `.lake`
artifacts were reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, or `.lake` mutation was performed. Lean sources and output objects
were copied to a fresh `/tmp` directory, and the directory was removed by a
shell trap.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0468` | 0 | Rank 314; lane `hard_mathlib_anchor_and_wrapper`; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0468/check_statement.py` | 0 | Fingerprint `def6574...fa0e`; all four recorded predicate-removal mutations were killed. |
| `python3 Stage1_Instances/THM-M-0468/check_anchor_audit.py` | 0 | Target fingerprint, exact pin, module hash, and four candidate classifications passed. |
| `python3 Stage1_Instances/THM-M-0468/check_obligation_tree.py` | 0 | 20 obligations and 44 typed edges passed; denominator `0b324115...6c4`; root remains open at `M4`. |
| Isolated pinned Lean recipe below | 0 | `BogomolovTarget` and `not_bogomolovTarget` elaborated; `#print axioms` reported `[propext, Classical.choice, Quot.sound]`. |
| `rg -n '\b(sorry\|admit\|sorryAx\|native_decide)\b\|^[[:space:]]*(axiom\|unsafe\|external)[[:space:]]' Stage1_Instances/THM-M-0468/ProofBlocker.lean` | 1 | No forbidden construct; exit 1 is ripgrep's expected no-match result. |

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

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Checked SHA-256 values:

- `Statement.lean`: `84151eb96c1159df08e882934dfc3b8652b1bb38cf150a521c09708a727dbc8c`
- `ProofBlocker.lean`: `e33f59eb5ed7ce49ab14b70e61c3e1306252cfdee25ca464a4128b2e029695e0`
- `ObligationTree.lean`: `23161c5fd3e4d4dd9a7d7b04f214cdda3531cc83a166fd730477306d37911504`
- `obligation-registry.json`: `86343feb231abc043e94742999b9a6457aaa92ed814749fa73f85f883d6692ed`
- `typed-graphs.json`: `2194c66bdcc18f7e2728859720a56f8c36f1a4e2f9054d3e53a7856551f9f62b`
- `anchor-audit.json`: `6ed5638e5bd32073aeed2014d08be820c38f28805ba926676f8521b3b45b8937`

Because the assigned positive proof phase is not genuinely complete,
`.stage1-worker-selftest.json` is deliberately absent. This is actionable
blocker evidence, not a proof receipt or an item-state claim.
