# THM-M-1018 proof-phase recheck at `e6c4d56e`

Item: `S56-M-1018-PROOF`

Date: `2026-07-14T04:15:13+08:00`

Base revision: `e6c4d56e017f77b02752e6c1325f0298dfb7f4d4`

Base tree: `3aa71b6797c53e65f39bbac295dabcd2fff8e0a6`

## Verdict

`blocked`. The exact sharp-cutoff Levy interval-inversion target has no unconditional proof body in
the owned dossier and no sufficient theorem in the pinned dependency closure. No proof body was
added. The lifecycle remains `planned`, the item remains `[ ]`, and the root vector remains
`[H2, M3, R4] -> [H2, M3, R4]`.

The graph-level remaining cut is `M1018-T-ANALYTIC`. Pinned mathlib supplies substantial supporting
analysis, including finite characteristic-function Fubini identities, exponential-integral
identities, dominated convergence, endpoint-measure lemmas, Levy convergence, and Gaussian Fourier
inversion. It does not supply the exact interval-mass inversion theorem or the central sharp
Dirichlet sine-integral evaluation and bound needed to build one. In particular,
`integral_charFun_Icc` is unweighted, while `Integrable.fourierInv_fourier_eq` assumes an integrable
density and integrable Fourier transform, which an arbitrary probability measure need not have.

The first concrete missing analytic terminal on the selected route is a placeholder-free theorem
that evaluates the symmetric sine integral (equivalently, gives the limits of the sine-integral
primitive at both infinities) and establishes a global bound. With that strong package, the
remaining measure limit is not blocked by domination: after the endpoint-kernel cancellation, the
physical-space approximant is a difference of two bounded sine-integral primitives, so a constant
dominates it against the finite probability measure. Only the naive pre-cancellation `1 / |t|`
bound is invalid. Finite-rectangle Fubini, normalization, endpoint branches, dominated convergence,
and their exact Lean composition remain nontrivial implementation work, but the pinned APIs provide
useful substrate for them.

No repo-local exact wrapper can currently be formed. `target_iff_expanded` is only a definitional
transport. `ObligationTree.root_compose` merely returns the complete analytic premise supplied by
its caller; moreover, it concludes the separately defined `ObligationTree.InversionFor` and does
not import `Statement.lean` or check a bridge to the canonical `LevyInversionTarget`. Returning that
conditional theorem would not satisfy the proof gate.

## Evidence Boundary

The frozen obligation artifacts are useful planning evidence but not proof evidence for the open
nodes. `check_obligation_tree.py` structurally checks 17 nodes and 34 typed edges and deliberately
asserts `root_closed=false`; all recorded node recipes call that same structural checker. Most open
analytic nodes still have prose `planned ...` targets rather than exact Lean signatures. The root
fingerprint labeled `lean-expression-sha256:88009a...` is the whole-file SHA-256 of `Statement.lean`,
not a canonical elaborated-expression digest. The mutation probes elaborate changed propositions
but do not prove their non-equivalence to the target. None of these facts supplies an analytic proof
body or changes the truthful blocked verdict.

## Validation

All Lean checks used the automation-provided canonical pinned `.lake` artifacts read-only. No
`lake update`, `lake build`, dependency clone/fetch, network access, or `.lake` mutation was used.
Temporary Lean objects and logs were created under `/tmp` and removed. The pre-existing untracked
`.lake` link makes this nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1018` | 0 | rank 494; planned hard-mathlib-anchor-and-wrapper lane; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1018/check_obligation_tree.py` | 0 | structural PASS for 17 obligations and 34 typed edges; denominator `c5662da4...d6c2`; root open M3 |
| isolated trust-zero replay of `Statement.lean`, `ObligationTree.lean`, and `AnchorAudit.lean` | 0 | all three elaborated with Lean 4.29.0; `root_compose` reported `[propext, Classical.choice, Quot.sound]` |
| exact-anchor scan over every pinned package `*.lean` | 1 | expected no-match exit for Levy inversion and `charFun`/`Ioc` interval-mass patterns |
| focused sine-integral terminal scan in pinned mathlib | 0 | matches were unrelated; no sine-integral-at-infinity evaluation was found |
| scoped prohibited-construct scan over owned `*.lean` files | 1 | expected no-match exit for `sorry`, `admit`, axiom declarations, `sorryAx`, unsafe/oracle hooks, and equivalents |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `8a178386...ea95`; tree `bdc39a31...e242b` |
| `test ! -e .stage1-worker-selftest.json` | 0 | completion self-test deliberately absent because the assigned proof phase is incomplete |

The isolated replay resolved Lean and `LEAN_PATH` through `lake env`, copied the three modules to a
fresh `/tmp/thm-m-1018-proof-e6c4d56e.*` directory, and invoked the resolved compiler with
`LEAN_NUM_THREADS=1 --trust=0 -t0 --root=<temporary-directory>`. It produced temporary olean hashes
`1a9dc999...4656` for `Statement` and `233dac9d...16d6` for `ObligationTree`; the printed canonical
statement output hash was `c897cb4f...964`. Source inputs remained `88009a0b...fdd7` for
`Statement.lean`, `2df4f358...055e` for `ObligationTree.lean`, `14938dc0...fb95` for the registry,
and `0ab51094...fba2` for the typed graphs. Mathlib is pinned at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`.

## Retry Condition

Resume after a placeholder-free implementation of the exact strong sine-integral limit/bound
package and its finite-Fubini, normalization, endpoint, dominated-limit, and canonical-root
composition dependents, or after an immutable compatible exact theorem enters the pinned closure
and passes exact-type, terminal-body, provenance, placeholder, axiom, composition, and trust checks.

This is current-base nonrelease blocker evidence, not a proof receipt. It does not satisfy
`S56-M-1018-PROOF`, propose an item-state transition, or support audit completion, validation,
release, theorem completion, receipt acceptance, or master acceptance.
