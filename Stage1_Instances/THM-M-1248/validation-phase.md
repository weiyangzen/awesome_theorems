# THM-M-1248 validation-phase evidence

Item: `S56-M-1248-VALIDATION`

Base revision: `fc1568a2997ca815b767b8cc172f3d4d339bf3b9`

Base tree: `635319193989301e577a430446e682952c51c538`

Validated: `2026-07-15` (`Asia/Shanghai`)

## Verdict

`blocked`, with a genuinely self-tested validation implementation proposed as
worker `[_]`. A fresh-output, network-isolated `--trust=0 -t0` replay checks
the exact frozen proposition, its local proof, and a separately written
reconstruction that imports neither `Proof` nor `ObligationTree`. The two root
routes are transitively sorry-free and report only `propext`,
`Classical.choice`, and `Quot.sound`.

That success is negative assurance, not Caffarelli-Kohn-Nirenberg proof credit.
The frozen statement's `ContDiff Real top` is analytic order `omega`, not the
source's smooth order `infinity`. Compact support therefore forces every
admitted function to be zero. In addition, the weighted definitions measure
the radial factor with the raw `Fin n -> Real` Pi/sup norm while evaluating the
function after Euclidean/L2 transport. No checked source transport repairs
either mismatch. The first node-order gate is the proof predecessor's missing
master acceptance; the first theorem gate is
`S56-5.1-EXACT-TARGET-IDENTITY-OR-TRANSPORT`.

## Gate Results

| Gate | Decision | Exact boundary |
|---|---|---|
| Kernel replay | provisional pass | Exact frozen root and no-`Proof` reconstruction elaborate at trust zero. |
| Placeholder and unsafe | pass for replayed roots | Lean `assert_no_sorry`, `#print sorries`, a parser-aware supplemental scan, and transitive closure inspection find no sorry, bodyless nonaxiom, or unsafe declaration. |
| Trust observation | provisional pass | Both routes report exactly the three observed axioms, but there is no accepted foundation profile or complete TCB closure. |
| Selected provenance | provisional pass | Local input hashes, mathlib revision/tree/origin/license, tools, and direct source/olean boundaries for analytic uniqueness and `ContDiff.analyticOnNhd` agree. |
| Source identity | fail closed | The frozen proposition is a vacuous analytic statement with a second radial-norm mismatch, not the intended smooth Euclidean CKN theorem. |
| Structured authority | fail closed | The proof predecessor is only `[_]`; the frozen graph still records the weighted analytic route and an open M3 root. |
| Hermetic release | fail closed | Fresh outputs and network isolation reuse the shared warm `.lake`; there is no clean empty-cache cold build, offline archive restoration, complete SBOM, or deterministic release bundle. |
| Independent verification | fail closed | The differential file is same-worker evidence in the same checkout and cache, not a distinct signed runner or independently provisioned minimal release verifier. |

## Commands

All commands ran inside the worker clone. No `lake update`, `lake build`,
dependency clone/fetch, network action, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-1248` | 0 | Rank 428, planned, L0/rework-required, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1248/check_obligation_tree.py` | 0 | 18 obligations and 43 typed edges passed; frozen root remains open M3. |
| `python3 -I -B Stage1_Instances/THM-M-1248/check_validation.py --probe` | 0 | Network-isolated trust-zero replay returned the recorded four semantic output hashes, three axioms, and a 36964-declaration/1341-module validation closure. |
| `python3 -I -B Stage1_Instances/THM-M-1248/check_validation.py --worker-packet .stage1-worker-selftest.json` | 0 | Final structured receipt, evidence hashes, packet, gates, and exact six-line summary passed. |
| `python3 -m json.tool` on the validation spec, receipt, and worker packet | 0 | All JSON artifacts parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m1248-validation-pycache python3 -m py_compile Stage1_Instances/THM-M-1248/check_validation.py` | 0 | Validator syntax compiled outside the repository. |
| `git diff --check -- Stage1_Instances/THM-M-1248 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The authoritative vector remains `[H1, M3, R3]`; no receipt or obligation is
accepted, and `audit_complete=false`, `theorem_complete=false`. Repair requires
versioning the statement with smooth order `infinity` and a consistent
Euclidean radial encoding, then refreezing every dependent statement hash,
obligation, graph, proof, and validation artifact.
