# THM-M-0665 release reconciliation

Item: `S56-M-0665-RELEASE`

Base revision: `1228bcced6922a2593bfd2fcd1e51e2b0c3091e4`

## Exact verdict

`blocked`. The lifecycle remains `planned`, the root remains `[H1, M3, R4]`, and both
`audit_complete` and `theorem_complete` are false. No receipt is accepted and no release or
authoritative state transition is claimed. This artifact self-tests the negative decision only.

The first workflow failure is `S56-10.2-DEPENDENCY-ACCEPTANCE`: the validation dependency is
provisional `[_]`, has verdict `blocked`, is `accepted=false` and `release_grade=false`, and has no
master acceptance. Independently, the first theorem gate is `M0665-C-PARAM.root_closure`; the first
release-protocol failure is `S56-RELEASE-IMMUTABLE-CLEAN-INPUT`, followed by
`S56-10.6-HERMETIC-COLD-EMPTY-CACHE`.

## Evidence reconciliation

The canonical target is exactly `Stage1Instances.THM_M_0665.PilaWilkie`, expression SHA-256
`da66c715ce12af9ff6dfb55a721665c8240358c0ee547062b3d2fc10c7785944`. It is a `Prop` definition,
not a theorem body. `Proof.lean` contains fourteen real elementary or special-case bodies, and the
current replay checks all of them plus three differential declarations with Lean trust level zero.
They are sorry-free and their observed axiom union is `Classical.choice`, `Quot.sound`, and
`propext`. This is genuine partial evidence, not a proof of the general theorem.

The frozen registry has twenty obligations. `M0665-ROOT` has no terminal proof body, the graph has
zero closed obligations and no checked composition certificate, and the exact root remains `M3`.
The open mathematical cut is `M0665-C-PARAM`, `M0665-L-DERIVATIVE`,
`M0665-L-ARITHMETIC`, `M0665-L-DROP`, and `M0665-L-COUNT`. Controlled parametrization,
determinant estimates, arithmetic vanishing, dimension drop, exponent bookkeeping, and the general
subpolynomial count are not present.

`AUDIT-Z` also fails: the source crosswalk lacks independent primary-source and errata review,
there is no accepted H0 or independently reviewed R0, and public state is not master-reconciled.
`THEOREM-Z` additionally lacks exact root closure, accepted composition/provenance/foundation/TCB
closure, immutable clean input, a cold empty-cache build, offline restoration, complete SBOM and
license closure, a deterministic content-addressed bundle, two independently provisioned signed
runners, an independently implemented minimal verifier, protected adversarial CI, and master
acceptance.

The integrated validation checker is correctly bound to its ancestor worker revision and cannot be
rerun unmodified at current HEAD. This release phase therefore uses a separately specified
current-head replay; it does not pretend the stale validation recipe ran. The root Lake project also
cannot resolve the pinned `flt-regular` checkout's `HEAD`. The replay derives `LEAN_PATH` from the
clean pinned mathlib project and reuses only existing outputs. No update, build, fetch, clone,
repair, or `.lake` mutation was performed.

## Commands and results

Commands ran on 2026-07-15 (Asia/Shanghai) from the worker clone unless a working directory is
shown.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0665` | 0 | Rank 709, planned lifecycle, theorem incomplete. |
| `cd Formalizations/Lean && lake env lean --version` | 1 | Pinned `flt-regular` could not resolve `HEAD`; recorded without repair or fetch. |
| recorded Bubblewrap `python3 -I -B Stage1_Instances/THM-M-0665/check_release.py` recipe | 0 | Network-isolated current-head trust-zero replay; 14 proof and 3 differential declarations sorry-free; all 20 negative states and both false terminal decisions reconciled. |
| `python3 -m json.tool` on the release JSON artifacts and worker packet | 0 | All structured artifacts parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0665-release-pycache python3 -m py_compile Stage1_Instances/THM-M-0665/check_release.py` | 0 | Checker compiled outside the repository. |
| `git diff --check -- Stage1_Instances/THM-M-0665 .stage1-worker-selftest.json` | 0 | No whitespace diagnostics. |

The release checker prints:

```text
PASS THM-M-0665 current network-isolated trust-zero Lean replay
PASS provisional dependency, frozen denominator, and all 20 negative states reconciled
OPEN H1/M3/R4; zero closed obligations; AUDIT-Z=false; THEOREM-Z=false; theorem_complete=false
BLOCKED dependency acceptance, exact root, hermetic release, independent verification, and master acceptance
```

Retry requires dependency-ordered master acceptance, an unconditional placeholder-free proof of the
five-member root cut and checked root composition, accepted H0/R0 and trust/provenance closure, then
a separately provisioned clean cold/offline release lane with supply-chain closure, deterministic
bundling, independent signed verification, protected adversarial CI, and master reconciliation.
