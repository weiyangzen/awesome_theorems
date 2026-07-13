# THM-M-0468 proof phase: current-head blocker

Item: `S56-M-0468-PROOF`

Base revision: `4d2c77230343716176b4192dc38e26f4c20c7547`

Base tree: `9eebdfdfda6b289fea0b6e778fae8e13327395b2`

Rechecked: `2026-07-14T03:26:23+08:00`

## Verdict

`blocked`: no consistent positive proof body can inhabit the exact frozen Lean
target. The proof item remains `[ ]`; no proof, provisional state, audit
completion, validation, release, theorem completion, or master acceptance is
claimed. A root `.stage1-worker-selftest.json` is deliberately absent.

`Statement.lean` quantifies over every `BogomolovData`, but the structure has no
laws connecting its operations and predicates to abelian geometry. The
placeholder-free `ProofBlocker.lean` supplies a permitted singleton model in
which every ambient hypothesis and density claim is true while
`isTorsionPoint` is false everywhere. The checked declaration is

```text
Stage1Instances.THM_M_0468.not_bogomolovTarget :
  Not Stage1Instances.THM_M_0468.BogomolovTarget
```

A positive proof of the frozen target would contradict this result. This
refutes only the overbroad formal encoding, not the mathematical Ullmo-Zhang
theorem. The fail-closed proposal is therefore `[H1, M4, R3] -> [H1, M5, R3]`,
subject to master reconciliation. The checked `root_of_direction_packages`
theorem assumes both missing implications and supplies no proof-body credit.
The pinned anchor inventory contains no exact Bogomolov proof body.

## Failed gates

The first failed gate is exact-target consistency at `M0468-S-DOMAINS`. The
semantic record admits the countermodel. Positive work may resume only after a
statement repair replaces the unconstrained surfaces with concrete pinned
definitions or source-justified, noncircular compatibility laws. The repair
must cover height/torsion, group translation, subvariety membership, and
Zariski-density semantics rather than merely assume either desired direction.

The predecessor statement gate is independently incomplete. Its checker kills
four removed-predicate mutations, while rev-5.6 section 5.1 also requires a
changed domain, changed binder scope, and boundary case. The dossier still
leaves `X = A` and zero-dimensional behavior open.

A transient shared-cache event interrupted an earlier validation attempt. The
canonical `flt-regular` checkout temporarily had `HEAD = refs/heads/.invalid`,
so `lake env` rejected the project before invoking Lean. The cache-owning lane
subsequently restored the exact manifest-pinned detached commit
`56161b6e...`; without this worker changing `.lake`, the required Lake-derived
recipe then replayed successfully. No moving dependency was fetched.

## Scoped validation

All commands ran in this worker clone. No network or dependency mutation was
used.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0468` | 0 | Rank 314; lane `hard_mathlib_anchor_and_wrapper`; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0468/check_statement.py` | 0 | Fingerprint `def6574...fa0e`; four recorded predicate-removal mutations killed. An earlier transient-cache attempt exited 1 before Lean. |
| `python3 Stage1_Instances/THM-M-0468/check_anchor_audit.py` | 0 | Target fingerprint, exact pin, module hash, and four candidate classifications passed. |
| `python3 Stage1_Instances/THM-M-0468/check_obligation_tree.py` | 0 | 20 obligations and 44 typed edges passed; denominator `0b324115...6c4`; root remains open at `M4`. |
| Isolated Lake-derived trust-zero replay | 0 | `lake env` selected the pinned Lean executable and path; copied sources elaborated and `#print axioms` reported `[propext, Classical.choice, Quot.sound]`. |
| `rg -n '\b(sorry\|admit\|sorryAx\|native_decide)\b\|^[[:space:]]*(axiom\|unsafe\|external)[[:space:]]' Stage1_Instances/THM-M-0468/ProofBlocker.lean` | 1 | No forbidden construct; exit 1 is ripgrep's expected no-match result. |

Exact Lake-derived recipe:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-0468-lake.XXXXXX)
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

Pinned identities and current source hashes:

- Lean commit: `98dc76e3c0a9b856c9b98726b713fb04fab16740`
- mathlib commit/tree: `8a178386ffc0f5fef0b77738bb5449d50efeea95` / `bdc39a3123201dae413a9d9be56ec242c19e5c2b`
- flt-regular manifest pin: `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`
- `Statement.lean`: `84151eb96c1159df08e882934dfc3b8652b1bb38cf150a521c09708a727dbc8c`
- `ProofBlocker.lean`: `e33f59eb5ed7ce49ab14b70e61c3e1306252cfdee25ca464a4128b2e029695e0`
- `ObligationTree.lean`: `23161c5fd3e4d4dd9a7d7b04f214cdda3531cc83a166fd730477306d37911504`
- `obligation-registry.json`: `86343feb231abc043e94742999b9a6457aaa92ed814749fa73f85f883d6692ed`
- `typed-graphs.json`: `2194c66bdcc18f7e2728859720a56f8c36f1a4e2f9054d3e53a7856551f9f62b`
- `anchor-audit.json`: `6ed5638e5bd32073aeed2014d08be820c38f28805ba926676f8521b3b45b8937`

Retry only after the statement is repaired and re-fingerprinted and all
invalidated predecessors are rerun. This is actionable blocker evidence, not a
proof receipt or item-state claim.
