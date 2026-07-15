# THM-M-1056 proof recheck (slot 39)

Item: `S56-M-1056-PROOF`

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`

Base tree: `c5771c47c12b80aba613e6d844570f83b39ded6d`

Attempt date: 2026-07-15 (Asia/Shanghai)

## Verdict

`blocked`. No exact proof body was added, no frozen obligation was closed, and
no state change or receipt is proposed. The root remains `[H1, M3, R3]`, with
`M1056-T-CORE` at M4. The lifecycle stays `planned -> planned`.
`.stage1-worker-selftest.json` is absent because this proof phase is not
self-tested complete.

## First failed proof gate

The first failed gate is `M1056-T-CORE`: the repository and its pinned
dependency closure still contain no placeholder-free inhabitant of
`OseledetsCorePackage`. That package is definitionally the full universal
target. `root_of_oseledetsCorePackage` therefore checks conditional identity
composition only and supplies no terminal proof body.

There is no contradiction or vacuity shortcut. A fresh trust-zero replay of
`SanityInstance.lean` realizes the antecedents for the identity cocycle on a
one-point probability space with fiber `Real` and constructs a splitting. The
target's cocycle direction and projection-equivariance equation also agree with
the standard invertible finite-dimensional Oseledets formulation.

## Proof search and current frontier

The immutable candidate remains
`marcmorningstar/lean4-ergodic-theory@ed3fa6b8a30594eeb791160563942ba115581aa0`.
Its `ErgodicTheory.oseledets_splitting` is substantive but pins Lean
4.30.0-rc2 and mathlib `34f7a6cd...`, while this worker pins Lean 4.29.0 and
mathlib `8a178386...`.

The inherited read-only scratch backport still has 21 of the 62 transitive
modules elaborated. A fresh trust-zero replay of module 22,
`ErgodicTheory.Lyapunov.OseledetsLimit.BandProjector`, deterministically failed
with the same eight Lean-4.29 compatibility errors and produced no olean. The
diagnostic output SHA-256 is
`0edd88651f3a4d8306b9546090e047567d7d99b88254823f1c0f137b44507819`.
Scratch files are outside the owned deliverable and receive no proof credit.

Even a complete port would still require an exact wrapper. It must transport
the Euclidean matrix theorem to arbitrary finite-dimensional `E`, including
strong measurability, inversion, both log-integrability hypotheses, cocycle
iteration, and norm growth. It must also turn the measurable internal
submodules into strongly measurable oblique component projections and prove
their idempotence, pairwise annihilation, sum, nonzero, equivariance, and
simultaneous-growth fields. A concrete future route is to form orthogonal
projector matrices `R_i`, set `S = sum_i R_i`, and use `Q_i = R_i * S^-1` on
the conull internal-direct-sum set; none of those exact bridge bodies is yet
implemented or kernel-checked. Importing the matrix/submodule theorem alone
would substitute a narrower target.

Repository-local `THM-M-1057` supplies the Kingman analytic input but not the
Lyapunov flags, transversality, splitting, projections, or exact transports.
The differently encoded `THM-M-1419` Oseledets target is likewise unproved and
cannot supply proof credit.

## Fresh validation

No `lake update`, `lake build`, dependency clone/fetch, or deliberate `.lake`
mutation was performed. The shared canonical `.lake` cache was concurrently in
an incomplete `flt-regular` checkout state, so `lake env lean` and the existing
statement script failed before Lean with `could not resolve 'HEAD'`. To avoid
fetching or mutating the cache, the actual elaboration checks below invoked the
pinned Lean executable directly with the already-present mathlib olean path and
fresh output under `/tmp`.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, passed. |
| `python3 scripts/stage1_target.py show THM-M-1056` | 0 | Rank 248; planned; rework required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1056/check_obligation_tree.py` | 0 | 19 obligations and 49 typed edges passed; denominator `5246a9d...b57828`; root M3 and core M4. |
| `LEAN_NUM_THREADS=1 timeout 300 python3 Stage1_Instances/THM-M-1056/check_statement.py` | 1 | Infrastructure blocker before elaboration: canonical `flt-regular` package had invalid `HEAD`; no fetch or repair was attempted. |
| Direct pinned Lean 4.29.0 `--trust=0 -t0` mutation replay of `Statement.lean` with fresh `/tmp` sources and outputs | 0 | Exact expression SHA-256 `8e1a96a...403b`; all four frozen mutations distinguished. |
| Direct pinned Lean 4.29.0 `--trust=0 -t0` replay of `Statement.lean`, `ObligationTree.lean`, and `SanityInstance.lean` with fresh oleans | 0 | Olean SHA-256 values `c55d17a...f64db`, `a75c5008...7f0e`, and `ff4de13c...178b7`; conditional composition and sanity use only `[propext, Classical.choice, Quot.sound]`. |
| Direct pinned Lean 4.29.0 `--trust=0 -t0` replay of scratch `BandProjector.lean` | 1 | Eight compatibility errors, no olean; output SHA-256 `0edd8865...7819`. |
| Prohibited-token scan over owned Lean files | 1 | Expected no-match exit; no `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, or `extern` declaration token. |
| Pinned mathlib revision/tree check | 0 | Revision `8a178386...ea95`, tree `bdc39a31...e5c2b`; no tracked mathlib changes. |

## Retry condition

Resume by compatibly porting module 22 and the remaining 40 candidate modules,
then implement and kernel-check the arbitrary-`E`, integrability, cocycle,
growth, measurable-oblique-projection, exact-type, provenance, and trust
bridges. Alternatively, provide equivalent placeholder-free local bodies. A
future worker should also retry `lake env lean` only after the scheduler's
canonical `flt-regular` artifact is complete; it must not fetch or repair that
shared dependency itself.

This is current-base proof-blocker evidence only. Accepted receipt IDs are
empty; audit completion, theorem completion, validation, release, and master
acceptance remain open.
