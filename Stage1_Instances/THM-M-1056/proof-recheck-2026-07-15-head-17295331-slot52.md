# THM-M-1056 proof recheck (slot 52)

Item: `S56-M-1056-PROOF`

Base revision: `1729533156a59958dac4908793303a66434eb925`

Base tree: `604b6669e6ab2f485c9dcb71de3a150c6deaf755`

Attempt date: 2026-07-15 (Asia/Shanghai)

## Verdict

`blocked`. No exact proof body was added under the owned path, no frozen
obligation was closed, and no state change or receipt is proposed. The root
remains `[H1, M3, R3]`; `M1056-T-CORE` remains M4. The lifecycle stays
`planned -> planned`, and `.stage1-worker-selftest.json` is absent because this
proof phase is not complete.

## First failed proof gate

The first failed gate is `M1056-T-CORE`: neither the repository nor its pinned
dependency closure contains a placeholder-free inhabitant of
`OseledetsCorePackage`. That package is definitionally the complete universal
target. Consequently, `root_of_oseledetsCorePackage` is only conditional
identity composition and provides no terminal proof body.

There is no contradiction or vacuity shortcut. `SanityInstance.lean` realizes
the antecedents for the identity cocycle on a one-point probability space with
fiber `Real` and constructs the requested splitting.

## Proof work completed in scratch

The immutable external candidate is
`marcmorningstar/lean4-ergodic-theory@ed3fa6b8a30594eeb791160563942ba115581aa0`.
It contains `ErgodicTheory.oseledets_splitting`, but pins Lean 4.30.0-rc2 and
mathlib `34f7a6cd...`, whereas this worker pins Lean 4.29.0 and mathlib
`8a178386...`.

This attempt advanced its 62-module transitive scratch port from 17 to 21
kernel-elaborated modules. In addition to the earlier modules, these four now
elaborate under the pinned environment with `--trust=0` and no placeholders:

| Module | Olean SHA-256 | Result |
|---|---|---|
| `ExteriorNorm.Basic` | `643f57eb04e0a5286fc2a076f72ba274b28f7fd4478a41b3ba97dc62da584851` | 3,754,944 bytes; exit 0 |
| `ExteriorNorm.Plucker` | `0ce4ee4ede269c4f76fbbe2b2935b44fb866afc84dc3c82a8fe4719bf583c947` | 3,092,400 bytes; exit 0 with two unused-simp warnings |
| `ExteriorNorm.Weyl` | `008cef104d291101b28f140e50e41d7c837cf223d17f9305a57c453196b3325f` | 603,544 bytes; exit 0, empty log |
| `OseledetsLimit.SingularValues` | `6b4e0f58eedd15b6b78f9566e267d6718c5c2c6cccbefea53f2b729bbcc72548` | 1,258,192 bytes; exit 0, empty log |

The next module, `OseledetsLimit.BandProjector` (22/62), fails with eight
Lean-4.29 compatibility errors. They comprise one deterministic typeclass
heartbeat timeout, an eigenvector-matrix simplification goal, the renamed
Hermitian/symmetric bridge, two scalar-inner-product normal forms, two brittle
orthonormal-basis reindex rewrites, and one positivity goal. The diagnostic log
SHA-256 is
`0edd88651f3a4d8306b9546090e047567d7d99b88254823f1c0f137b44507819`.
Scratch artifacts are discovery/port evidence only and are not repository proof
credit.

Even a completed port would prove a Euclidean matrix/submodule result, not the
frozen exact target. A wrapper must still transport arbitrary finite-dimensional
`E`, measurability, inversion, both log-integrability assumptions, cocycle
iteration and norm growth. It must also construct strongly measurable oblique
component projections for the generally nonorthogonal internal direct sum and
prove their algebraic, equivariance, nonzero, and simultaneous-growth fields.
No existing local or pinned-mathlib theorem supplies that measurable oblique
projection bridge. Importing the narrower result would be theorem substitution.

Repository-local `THM-M-1057` supplies the Kingman analytic input, including
`ErgodicTheory.tendsto_kingman_ergodic_means`, but not the Lyapunov flags,
transversality, splitting, projections, or exact transports.

## Fresh validation

The automation-provided `.lake` symlink was reused read-only. No `lake update`,
`lake build`, dependency clone/fetch, network action, or `.lake` mutation was
performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, passed. |
| `python3 scripts/stage1_target.py show THM-M-1056` | 0 | Rank 248; planned; rework required; theorem incomplete. |
| `LEAN_NUM_THREADS=1 python3 Stage1_Instances/THM-M-1056/check_statement.py` | 0 | Exact expression SHA-256 `8e1a96a304ce3dd43838f934406d58ac3594b9d34c6e1617461abc17e65d403b`; all four mutations passed. |
| `python3 Stage1_Instances/THM-M-1056/check_obligation_tree.py` | 0 | 19 obligations and 49 typed edges passed; denominator `5246a9d5966e76ff5cb379c8f39f48100fafd3c2ce99bf7c7e10f953f8b57828`; root M3, core M4. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 commit `98dc76e...`; Lake `5.0.0-src+98dc76e`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` and status | 0 | Revision `8a178386...ea95`, tree `bdc39a31...e5c2b`; clean package worktree. |
| Copy `Statement.lean`, `ObligationTree.lean`, and `SanityInstance.lean` to fresh `/tmp`; elaborate each with the existing package `LEAN_PATH`, `LEAN_NUM_THREADS=1`, `--trust=0 -t0`, and fresh oleans; remove the directory | 0 | All three elaborated. Olean SHA-256 values: `c55d17a...f64db`, `a75c5008...7f0e`, `ff4de13c...178b7`. Printed axiom sets for conditional composition and sanity were `[propext, Classical.choice, Quot.sound]`. |
| Compile scratch modules 18-21 with `LEAN_PATH=/tmp/m1056-module18-slot36:$(lake env printenv LEAN_PATH) lake env lean --trust=0 -t0 -R /tmp/m1056-module18-slot36 -o <fresh-olean> <module>` | 0 each | Modules 18-21 elaborated; the hashes above bind their outputs. |
| Compile scratch module 22 with the same pinned command | 1 | Eight compatibility errors; no olean produced; log hash `0edd8865...7819`. |
| `rg` prohibited declaration tokens over owned Lean files and the four repaired scratch sources | 1 | Expected no-match exit; no `sorry`, `admit`, `axiom`, `sorryAx`, `unsafe`, `implemented_by`, or `extern` declaration token. |
| Search repository targets and pinned mathlib for an exact Oseledets body | 0 | Only target/interface definitions were found; no terminal Oseledets theorem exists in the checked closure. |

## Retry condition

Resume at scratch module 22, compatibly port all remaining modules, and then
implement and kernel-check the arbitrary-`E`, integrability, cocycle-growth,
measurable-oblique-projection, equivariance, count, exact-type, provenance, and
trust bridges. Alternatively, provide equivalent placeholder-free local bodies.

This artifact is a current-base proof blocker, not a proof receipt. Audit,
validation, release, theorem completion, and master acceptance remain open.
