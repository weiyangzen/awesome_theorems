# THM-M-0346 proof-phase blocker

Item: `S56-M-0346-PROOF`. Attempted on 2026-07-12 from repository revision
`7780ee2963f599a6bf06f39a12c6fddb7eafc914`.

## Verdict

The proof phase is blocked and is not self-tested as complete. No proof body for the exact
`Stage1.THM_M_0346.CarlesonTarget` was added, and no worker self-test manifest is issued.

The frozen proof architecture requires an integrated, kernel-checked Carleson-Hunt theorem at
`p = 2` together with representative, normalization, cutoff, and almost-everywhere transports.
The only audited mathematical closure is `fpvandoorn/carleson` at commit
`80e151dff5ddce2426079ec6392616496a4ec927`, but it is anchor-only: it is not present among the
existing pinned Lake packages. It also targets Lean `v4.30.0-rc2` and mathlib
`1a4917a18b30ea1333c195e597067fe044ac9176`, while this clone is pinned to Lean `v4.29.0` and
mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`. The task forbids fetching or mutating `.lake`, so
there is no dependency artifact against which a truthful adapter or transitive kernel check can be
implemented here.

Pinned mathlib contains no declaration named `carleson_hunt` and no definition named
`partialFourierSum'`. Thus the core obligation `M0346-L-CARLESON-HUNT` remains open, as do the four
encoding transports that depend on the unavailable upstream API. The existing
`root_of_transported_carleson_hunt` theorem was re-elaborated, but it only proves the root from an
explicit premise definitionally identical to the root; it is not a proof of that premise and
receives no root proof credit.

First unblock condition: the integration lane must provide an immutable, license-reviewed
Carleson package artifact compatible with the repository toolchain (or deliberately update the
repository-wide pins), after which the exact wrapper and its transitive placeholder/axiom closure
can be checked. Inventing a local premise, using the conditional wrapper as closure, or replacing
the target with mathlib's `L2`-topology convergence theorem would be a prohibited substitution.

## Exact validation record

All dependency artifacts were inspected read-only. No `lake update`, `lake build`, clone, fetch, or
network operation was run.

| Command | Result |
|---|---|
| `git rev-parse HEAD` | exit 0; `7780ee2963f599a6bf06f39a12c6fddb7eafc914` |
| `cat Formalizations/Lean/lean-toolchain` | exit 0; `leanprover/lean4:v4.29.0` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `find Formalizations/Lean/.lake/packages -maxdepth 1 -mindepth 1 -type d -printf '%f\\n' \| sort \| rg -i '^carleson$'` | exit 1; no existing pinned Carleson package |
| `rg -n --glob '*.lean' 'theorem carleson_hunt\|def partialFourierSum.' Formalizations/Lean Stage1_Instances/THM-M-0346` | exit 1; no local upstream declaration or API |
| `rg -n --glob '*.lean' '\\b(sorry\|admit\|axiom)\\b' Stage1_Instances/THM-M-0346` | exit 1; no forbidden placeholder token in owned Lean sources |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0346/Statement.lean)` | exit 0; exact `CarlesonTarget` elaborated |
| scoped `lake env which lean` check of `Statement.lean` and `ObligationTree.lean`, with temporary `Statement.olean` outside the repository | exit 0; conditional wrapper depends on `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Stage1_Instances/THM-M-0346/check_obligation_tree.py` | exit 0; 11 obligations and 24 typed edges; root explicitly open at `M3` |

Status boundary: actionable proof blocker evidence only. `S56-M-0346-PROOF` remains open; no
machine closure, audit completion, theorem completion, receipt acceptance, or checklist transition
is claimed.
