# Statement gate blocker

Item: `S56-M-0523-STATEMENT`  
Theorem: `THM-M-0523`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The authoritative repository record does not identify a proposition that can be frozen and
elaborated without inventing mathematics. It pairs the name "Manin-Drinfeld theorem" with only the
gloss `椭圆曲线上Heegner点的性质` ("properties of Heegner points on elliptic curves"). That gloss
does not state which property of which Heegner points is intended, and it describes a materially
different topic from the standard named theorem about torsion classes of cuspidal divisors on
modular curves.

The accepted intake deliberately leaves `canonical_claim` null. It has no immutable primary-source
edition, theorem/page pinpoint, assumption crosswalk, errata review, or independent adjudication
selecting either a Heegner-point proposition or the named cusp-divisor theorem. Choosing the
familiar Manin-Drinfeld conclusion from the name would silently correct the source; choosing a
Heegner-point height, trace, rank, torsion, or non-torsion result would invent the unspecified
"property". Neither is permitted by the rev-5.6 exact-statement gate.

Even the candidate named-theorem reading remains underdetermined: the source must fix the class of
congruence subgroups or modular curves, base field and cusp field of definition, compactification,
Jacobian versus degree-zero Picard target, geometric versus rational divisors, ordered binders,
equal-cusp boundary, and the precise torsion predicate. The duplicate `THM-M-0124` legacy file uses
user-supplied abstract curve and divisor-class interfaces. It is explicitly discovery-only and
cannot supply statement identity or proof credit for this ID.

Consequently the canonical expression, expression fingerprint, checked transports, and meaningful
removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutations required by
rev-5.6 section 5.1 cannot be produced truthfully. No `Statement.lean`, proxy predicate, axiom,
placeholder, weakened special case, broadened target, or substituted theorem was introduced.
Machine status remains `M4`; statement acceptance, audit completion, and theorem completion are
false.

## Lean substrate boundary

The existing `IntakeProbe.lean` was re-elaborated only to distinguish a missing mathematical target
from a missing Lean installation. Its sole direct import is
`Mathlib.NumberTheory.ModularForms.Cusps`; it checks arithmetic subgroups, cusps, cusp orbits, the
`SL(2,Z)` cusp characterization, and finiteness of cusp orbits. Those APIs do not construct a
compactified modular curve, Jacobian or `Pic^0`, cuspidal divisor class, or Abel-Jacobi map, and
finiteness of cusp orbits is not torsion of cusp-difference classes. A bounded name/API search of
the pinned mathlib source found no Manin-Drinfeld or cuspidal-divisor declaration. This is substrate
reconnaissance, not a canonical target or an anchor-audit result.

## Environment fingerprint

- Repository base revision: `028e2535b68678b8296e63e2cacb05ed9775a2d8`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- `IntakeProbe.lean` SHA-256:
  `a1dd3387dee272c8975f39ab2ea57179501a4cd1f2bc634c946df660f73ab926`.
- The pre-existing canonical `.lake` symlink was used read-only. No update, build, dependency clone,
  or fetch was run.

## Validation evidence

All commands ran inside this worker clone except that the existing `.lake` symlink resolves to the
canonical pinned artifacts.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0523` | 0 | Rank 895, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0523/IntakeProbe.lean` | 0 | All six cusp-substrate checks elaborated; no canonical theorem target asserted |
| `rg` over the repository source entries and Stage0 projection | 0 | Found only the conflicting Heegner-point gloss and fields explicitly left open |
| bounded `rg` for Manin-Drinfeld/cuspidal-divisor APIs in pinned mathlib | 1 | Expected no-match exit; no matching declaration or source occurrence found |
| `python3 -m json.tool Stage1_Instances/THM-M-0523/statement-blocker.json` | 0 | Blocker receipt is valid JSON |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0523 -g '*.lean'` | 1 | Expected no-match exit; no prohibited placeholder or axiom occurs in target Lean source |
| `git diff --check -- Stage1_Instances/THM-M-0523` | 0 | No whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | Confirmed that this blocked phase emitted no completion manifest |

## Retry condition and boundary

An accountable source review must first select an immutable primary-source edition and exact
theorem/page, check errata, and independently adjudicate the repository gloss against the theorem
name. If the cusp-divisor theorem is selected, the review must freeze every modular-curve, field,
divisor, target-group, binder, and boundary convention listed above; if a Heegner-point result is
selected, it must state the exact property and all hypotheses. A later statement run can then encode
that exact claim using concrete pinned APIs, minimize imports, serialize its elaborated expression,
compile any credited transports, and execute all four required mutation classes.

Until that condition is met, the statement phase has not passed its completion gate. No
`.stage1-worker-selftest.json` is emitted. The root remains `[H3, M4, R4]`; no downstream phase or
theorem-completion credit is claimed.
