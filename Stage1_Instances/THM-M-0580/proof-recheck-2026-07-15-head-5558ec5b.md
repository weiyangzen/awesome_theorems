# THM-M-0580 proof-phase recheck at base 5558ec5b

Item: `S56-M-0580-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `5558ec5b162bfdfa95b44fafcf97b69a44d1ff37`

Base tree: `f17ce1a24cd65800f536301fdb66a12e18ef3ae3`

## Verdict

`blocked`. No eligible terminal Lean 4 proof body exists in the repository or pinned dependency
closure for the exact proposition `Stage1Instances.THM_M_0580.PerelmanPoincareTarget`. No proof body
or receipt was added. The item remains `[ ]`, the root vector remains `[H2, M4, R4]`, and the audit,
root, and theorem remain incomplete.

The immediate frozen root cut set remains:

- `M0580-N-SMOOTH`, the proposed topological smoothing package;
- `M0580-T-SMOOTH-POINCARE`, the proposed smooth three-dimensional Poincare package.

`root_of_smoothing_and_smooth_poincare` assumes both packages and only composes them. The diagnostic
`smoothThreeDimensionalPoincare_of_perelmanPoincareTarget` goes from the root back to the second
package, so using it to construct a premise for the root would be circular.

Pinned mathlib supplies the matching generalized, topological, and smooth signatures only through
`proof_wanted`. The pinned Batteries implementation elaborates these signatures inside
`withoutModifyingEnv`; it deliberately discards them, and they cannot be used as axioms. Direct
trust-zero checking after import reports the names as unknown. Current scoped searches found no
alternate retained body. The immutable external audit contains only a dimension-three statement
and an unrelated dimension-zero proof.

## First Failed Gate

The structured prerequisite is not accepted. `task-dag.json` has `accepted_states: []` and records
`STATEMENT`, `ANCHOR_AUDIT`, `OBLIGATION_TREE`, and `PROOF` as open. The generated checklist shows
only provisional `[_]` artifacts for the prerequisites; a proof worker cannot accept or reconcile
that state.

The frozen proof architecture also requires an append-only prerequisite revision before node-level
implementation:

- `TopologicalThreeManifoldSmoothable` receives an already selected `ChartedSpace` and requires
  `Nonempty (IsManifold ... M)` for that atlas. This is stronger than existence of a replacement
  compatible smooth atlas; wrapping the proposition in `Nonempty` chooses no atlas.
- `SmoothThreeDimensionalPoincare` concludes the same homeomorphism as the root under one extra
  `IsManifold` instance. The root therefore implies this package directly. It does not encode the
  distinct diffeomorphism-valued smooth result described by the graph prose.
- `C-METRIC` through `L-PI1-ELIMINATION` have planned prose strings rather than exact Lean formal
  targets, no owned proof sources, and recipes covering no Lean declarations.

Silently replacing those frozen contracts would violate both the registry rule and this worker's
proof-phase authority. Even after correction, the Ricci-flow, surgery, extinction, decomposition,
and fundamental-group packages remain unformalized in the pinned closure.

## Validation

All commands ran in this worker clone. Lean outputs were confined to disposable `/tmp` paths. The
automation-provided untracked `.lake` symlink was reused read-only. No `lake update`, `lake build`,
dependency clone/fetch, or dependency mutation was run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0580` | 0 | rank 115; planned; L0/rework-required; theorem incomplete |
| independent trust-zero `lake env lean` probe | 0 | the exact statement and conditional composition elaborated; `#print axioms root_of_smoothing_and_smooth_poincare` reported `[propext, Classical.choice, Quot.sound]` |
| direct trust-zero check of `SimplyConnectedSpace.nonempty_homeomorph_sphere_three` | 1 | expected negative evidence: `Unknown constant`; the `proof_wanted` entry is not retained |
| `python3 Stage1_Instances/THM-M-0580/check_obligation_tree.py` | 0 | 20 obligations and 42 typed edges passed; denominator `46585d643f518847529b9ef08ddd76ea206e6ca7a9645ce21aa28126d8c98a6d`; root remains open at M4 |
| scoped exact-root and cut-set `rg` search | 0 | `PASS: no alternate exact-root or cut-set declaration found` |
| inverted prohibited-construct `rg --pcre2` scan of the four owned Lean modules | 0 | `PASS: no prohibited proof construct in four owned Lean modules` |
| pinned marker and Batteries implementation `rg` checks | 0 | exactly the three relevant `proof_wanted` entries were found; Batteries states they are discarded and cannot be used as axioms |
| `cd Formalizations/Lean && timeout 60 lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |

The independent narrow Lean probe used the pinned `lake env which lean` executable and the pinned
`lake env printenv LEAN_PATH`. It wrote `Statement.olean` only under `/tmp/slot27-m0580-probe`, then
checked `ObligationTree.lean` with that directory prepended to `LEAN_PATH`. No repository build
artifact was written.

The owned `check_statement.py` helper was also started at the current base, but the rerun was
abandoned before completion under severe shared-runner contention. It left no output or owned
artifact. The unchanged `Statement.lean`, toolchain, manifest, and mathlib hashes match the already
integrated 2026-07-15 trust-zero statement validation that killed all four structural mutations and
produced canonical expression SHA-256
`938ef54298273a011a66395812b53e6bf8071b0925b84cd94ae5fb4f9a6eb664`. No proof-completion claim
depends on that prior result.

## Retry Condition

First reconcile and master-accept the prerequisite task state. Then publish an append-only
obligation-tree revision with a replacement-atlas smoothing contract, faithful smooth-package
semantics, exact Lean targets for every child, checked composition, and declaration-covering
recipes. Implement those corrected packages without placeholders. Alternatively, integrate an
immutable, licensed, compatible exact-root Lean 4 proof with a complete dependency lock and
exact-type/provenance checks.

Assuming either missing package, treating `proof_wanted` as an axiom, or presenting conditional
composition as root closure would violate the exact-target and proof-body gates. This is an owned
blocker artifact, not a proof receipt; it does not satisfy `S56-M-0580-PROOF` or support theorem
completion. Because the phase is not genuinely complete, `.stage1-worker-selftest.json` remains
absent.
