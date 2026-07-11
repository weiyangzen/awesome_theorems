# THM-M-0580 proof-phase blocker

Item: `S56-M-0580-PROOF`  
Attempt date: 2026-07-12  
Base revision: `046b0721abb228d13c7042349574736fe375cd97`

## Result

The proof phase is blocked and is not self-tested as complete. No proof body was
added, and no theorem-completion or machine-closure claim is made.

The exact root is
`Stage1Instances.THM_M_0580.PerelmanPoincareTarget`. The frozen proof graph's
immediate semantic cut set remains:

- `M0580-N-SMOOTH`: compatible smoothing of the fixed topological manifold;
- `M0580-T-SMOOTH-POINCARE`: the full smooth three-dimensional Poincare
  package, expanded through Ricci flow, noncollapsing, canonical neighborhoods,
  surgery, finite extinction, decomposition, and fundamental-group
  elimination.

The only local proof body,
`root_of_smoothing_and_smooth_poincare`, is a conditional composition theorem:
it takes both missing packages as premises. It elaborates, but it does not
inhabit either package and therefore provides no proof credit for the root.

The pinned mathlib source contains only `proof_wanted` entries for
`SimplyConnectedSpace.nonempty_homeomorph_sphere_three` and
`SimplyConnectedSpace.nonempty_diffeomorph_sphere_three`. Those entries do not
create retained theorem declarations or terminal proof bodies. The prior
immutable anchor audit likewise found no eligible external dimension-three
body to pin or import. Consequently there is no truthful local implementation
or wrapper available without formalizing the unresolved cut set itself.

## Commands and exact results

Run from the repository root unless a command contains an explicit `cd`.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0
  check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy
  slots, 1546 uniform-L0 Lean 4 targets, execution skill present)

python3 scripts/stage1_target.py check
  exit 0
  stage1_target: ok (1546 unique targets, ranks 1..1546, all
  L0/rework_required)

python3 scripts/stage1_target.py show THM-M-0580
  exit 0
  execution rank 115; lifecycle planned; baseline L0; rework_required true;
  theorem_complete false

LEAN_BIN=$(cd Formalizations/Lean && lake env which lean)
LEAN_LIB=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
(cd Stage1_Instances/THM-M-0580 &&
  LEAN_PATH="$LEAN_LIB" "$LEAN_BIN" -o Statement.olean Statement.lean &&
  LEAN_PATH=".:$LEAN_LIB" "$LEAN_BIN" ObligationTree.lean)
rm -f Stage1_Instances/THM-M-0580/Statement.olean
  exit 0
  root_of_smoothing_and_smooth_poincare elaborated at result type
  PerelmanPoincareTarget; #print axioms reported [propext, Classical.choice,
  Quot.sound] and no sorryAx

python3 Stage1_Instances/THM-M-0580/check_anchor_audit.py
  exit 0
  ok: exact statement anchors are bodyless, external root is statement-only,
  root=M4

python3 Stage1_Instances/THM-M-0580/check_obligation_tree.py
  exit 0
  PASS THM-M-0580 obligation tree: 20 obligations, 42 typed edges
  registry denominator sha256:
  46585d643f518847529b9ef08ddd76ea206e6ca7a9645ce21aa28126d8c98a6d
  root closure: open (M4); smoothing and smooth Perelman packages remain
  unproved

rg -n "proof_wanted SimplyConnectedSpace\\.nonempty_(homeomorph|diffeomorph)_sphere_three|theorem SimplyConnectedSpace\\.nonempty_(homeomorph|diffeomorph)_sphere_three" Formalizations/Lean/.lake/packages/mathlib/Mathlib/Geometry/Manifold/PoincareConjecture.lean
  exit 0
  lines 47 and 52 are the two proof_wanted markers; no matching theorem line
```

No dependency fetch, update, build, clone, or `.lake` mutation was performed.
The pre-existing untracked `Formalizations/Lean/.lake` link was left unchanged.

## Reopen condition

Resume the proof phase only when either (a) a complete Lean proof of the frozen
cut set is implemented under this target, or (b) an eligible Lean 4 terminal
declaration is found with an immutable source revision, dependency lock, and
license, then exact-type checked and imported through the pinned environment.
Until then the root remains `M4`, `root_closed=false`, and
`theorem_complete=false`.

Because the assigned proof deliverable is not complete,
`.stage1-worker-selftest.json` must remain absent.
