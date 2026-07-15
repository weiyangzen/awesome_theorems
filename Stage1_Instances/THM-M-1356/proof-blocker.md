# THM-M-1356 proof-phase execution

Item: `S56-M-1356-PROOF`

Execution date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `51c2828e82ffb19860830f78b771f80e13ad7dff`

## Verdict

`blocked`; the exact arbitrary-degree Routh-Hurwitz root remains open. This
execution adds a placeholder-free proof of the complete degree-one instance,
including the descending coefficient transport, the unique complex root, the
unique Hurwitz minor, and their exact equivalence. It does not prove either
frozen all-degree direction and therefore closes no registry obligation.

The lifecycle stays `planned` and the authoritative vector stays
`[H1, M3, R4]`. No proof receipt or completion self-test is emitted. In
particular, the existing conditional declarations in `ObligationTree.lean`
continue to receive no proof credit because they take both target directions
as explicit premises.

## Checked Contribution

`Proof.lean` supplies four real bodies:

| Declaration | Checked result |
|---|---|
| `complexPolynomial_fin_one` | the frozen adapter at `n = 1` is `a_0 X + a_1` over `Complex` |
| `strictlyStable_fin_one` | under `0 < a_0`, strict stability is equivalent to `0 < a_1` |
| `hurwitzMinor_fin_one` | the unique leading minor is `a_1` |
| `routhHurwitz_fin_one` | the exact frozen stability/minor equivalence holds at `n = 1` |

All four declarations elaborate with Lean `--trust=0` and report exactly
`[propext, Classical.choice, Quot.sound]`. The source contains no proof
placeholder, axiom declaration, unsafe/oracle device, or assumed direction.
This is substantive boundary evidence, but it is not a substituted theorem:
the canonical target quantifies over every positive degree.

## Failed Gate

The first failed implementation gate is the arbitrary-degree engine upstream
of `M1356-B-STABLE-TO-MINORS` and `M1356-B-MINORS-TO-STABLE`. The frozen route
requires alternating even/odd polynomial identities, signed Euclidean/Sturm
sequences, Hermite hodograph root counting, Cauchy indices, regular and five
nonregular Routh cases, no-pivot Hurwitz-block elimination, and the leading
minor product identity. None has a terminal body in the pinned closure.

The frozen minimal root cut remains:

- `M1356-B-STABLE-TO-MINORS`
- `M1356-B-MINORS-TO-STABLE`

A supplemental immutable near-candidate,
`PerAlexandersson/RealRooted@634a949d31683785b4181efbba6faff31e81e006`,
was available in pre-existing audit scratch. Its Hermite-Biehler and Hurwitz
matrix terminals contain explicit `sorry`, and its infinite total-
nonnegativity/right-half-plane formulation is not the finite strict-minor
target. It is therefore rejected for both placeholder and exact-target gates.

## Validation

All commands used the automation-provided existing `.lake` symlink and the
pinned toolchain read-only. No Lake update/build, dependency clone/fetch,
network retrieval, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, passed |
| `python3 scripts/stage1_target.py show THM-M-1356` | 0 | rank 966; planned; L0/rework-required; theorem incomplete |
| isolated `lake env which lean` replay of copied `Statement.lean` and `Proof.lean` with `--trust=0 -t0` | 0 | exact statement and all four degree-one bodies elaborated; `Proof.olean` SHA-256 `dbd13ed0...e66cf` |
| later redundant isolated replay of unchanged `ObligationTree.lean` | no result captured | host-wide concurrent Lean saturation interrupted the attempt; no proof claim depends on this conditional module |
| comment-stripped token-anchored prohibited-device scan of `Proof.lean` | 1 | expected no-match exit; no prohibited construct found |
| exact-topic scan of repo-local and pinned dependency Lean sources | 1 for pinned dependencies; repo scan matched only this dossier | no arbitrary-degree candidate outside the owned dossier found |
| `python3 -B Stage1_Instances/THM-M-1356/check_obligation_tree.py` | 1 | predecessor checker rejects current HEAD because it hard-pins base `431e77db...`; this is stale predecessor freshness evidence, not a Lean failure |
| pinned mathlib status/revision check | 0 | clean revision `8a178386...ea95`, tree `bdc39a31...d8b` |
| `python3 -m json.tool Stage1_Instances/THM-M-1356/proof-blocker.json` and scoped whitespace checks | 0 | blocker record parses and touched files have no whitespace errors |

## Status Boundary

This is current-base blocker evidence plus a checked degree-one partial proof.
It does not satisfy `S56-M-1356-PROOF`, close a frozen obligation or the root,
change scheduler state, or claim proof-phase completion, audit completion,
theorem completion, validation, release, receipt acceptance, or master
acceptance. Because the assigned phase is not complete, there is deliberately
no `.stage1-worker-selftest.json`.
