# THM-M-0346 proof recheck at current base

Item: `S56-M-0346-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T20:26:27+08:00`

Base revision: `6ee4e043011799c8a8d6f7f5a2b68dd5fb819679`

Base tree: `8e7811b64a8ad5298ec20aa3f40898f299dce655`

## Verdict

`blocked`. The assigned proof phase remains `[ ]`; no completion self-test is issued.

The exact target is `Stage1.THM_M_0346.CarlesonTarget`: every complex `L^2` class on the
period-one additive circle has its inclusive symmetric Fourier sums converge almost everywhere to
the canonical `Lp` representative. The six declarations in `Proof.lean` are genuine,
placeholder-free adapter bodies. A trust-zero isolated replay checks the representative's `MemLp`
certificate, the period and exponent facts, specialization of an upstream-shaped Carleson-Hunt
contract, the exact local cutoff equality, and conditional composition into the frozen target.
`ObligationTree.lean` also re-elaborates its conditional assembly.

These bodies do not prove `RawCarlesonHunt`. In particular,
`carlesonTarget_of_rawCarlesonHunt : RawCarlesonHunt -> CarlesonTarget` is a checked conditional
adapter, not a proof of its premise or of the root. The local `upstreamPartialFourierSum` models the
audited API but does not import or validate the external `partialFourierSum'` definition.

The first failed gate remains `M0346-L-CARLESON-HUNT`. The pinned dependency closure has no
Carleson package and no source or compiled declarations for `carleson_hunt` or
`partialFourierSum'`. Pinned mathlib's `hasSum_fourier_series_L2` proves convergence in the `Lp`
Hilbert space, not pointwise or almost-everywhere convergence. Its pointwise theorem requires a
continuous function with summable Fourier coefficients and cannot establish the arbitrary-`L^2`
target.

The audited upstream history supplies no compatible proof body. Revision
`306ae5b29300771aece1aa39f0a939183cc59486` uses Lean `v4.29.0`, but pins mathlib
`f1a99cc3d4b62bff01325ac228882baadea934af` and defines `carleson_hunt := sorry`. The first
source-complete revision, `d422163115553c400bb93b6b3b0d50313b7a9f25`, requires Lean
`v4.30.0-rc2` and mathlib `1a4917a18b30ea1333c195e597067fe044ac9176`; it is not installed or
compiled in this repository's pinned closure, and its previously traversed import closure contains
active `sorry` terms. The worker may neither fetch that dependency nor mutate `.lake`, so its
analytic proof body cannot be truthfully integrated here.

Copying only the source-complete `CarlesonHunt.lean` is not a portable workaround: it directly
imports four project-local modules and recursively needs about 117 Carleson modules, newer mathlib
APIs, and the placeholder-bearing support modules above. Backporting and closing that graph would
be a separate major formalization project rather than a pinned proof import for this worker item.

## Narrow evidence

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts was reused read-only. Temporary
Lean objects were confined below `/tmp` and removed. No `lake update`, `lake build`, dependency
clone/fetch, network request, external checkout, source import, or `.lake` mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1,546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1,546 unique ordered targets and ranks passed. |
| `python3 scripts/stage1_target.py show THM-M-0346` | 0 | Rank 839; lifecycle planned; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0346/check_obligation_tree.py` | 0 | Eleven obligations and 24 typed edges passed; denominator `1ff60884ffc043439ab5a7b812bc9f2e8133e9d1eb8d130330d43f2709439c8c5`; root open at M3. |
| Isolated replay of copied `Statement.lean`, `Proof.lean`, and `ObligationTree.lean` below `/tmp`, using the Lean binary and `LEAN_PATH` obtained through existing `lake env`, with `LEAN_NUM_THREADS=1`, `timeout 600`, `--trust=0`, and `-t0` | 0 | The exact target, all six local adapter bodies, and conditional obligation composition elaborated. Every adapter was sorry-free and reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| `rg -n --pcre2 '(?m)^\s*(?:axiom\|constant\|opaque)\b\|\b(?:sorry\|admit\|sorryAx\|unsafe\|extern\|implemented_by\|native_decide)\b' Stage1_Instances/THM-M-0346/{Statement,Proof,ObligationTree}.lean` | 1 | Expected no-match exit; no prohibited mechanism occurs in the owned Lean sources. |
| `find -L Formalizations/Lean/.lake/packages -maxdepth 1 -mindepth 1 -type d -printf '%f\n' \| sort \| rg -i '^carleson$'` | 1 | Expected no-match exit; no pinned Carleson package exists. |
| `rg -n --glob '*.lean' 'theorem\s+carleson_hunt\b\|def\s+partialFourierSum.' Formalizations/Lean Stage1_Instances/THM-M-0346` | 1 | Expected no-match exit; the actual upstream theorem and API are absent. |
| Scoped search of existing package build directories for `Carleson/Classical/CarlesonHunt.{olean,ilean,ir}` | 0 | Empty output; no compiled Carleson-Hunt artifact exists in the pinned closure. |
| Direct `--trust=0 -t0` probe of source-complete upstream `CarlesonHunt.lean` against the current pinned `lake env` | 1 | Lean rejected line 1 with `unknown module prefix 'Carleson'`; only the repository's pinned package paths were available. |
| `git diff --name-status f53223e6746df4856b00068d3e8723264dfd044a..HEAD --` over canonical proof, registry, graph, anchor, pin, manifest, target-manifest, and execution-skill inputs | 0 | Empty output; no scoped proof source or pin changed since that prior recheck base. |
| Canonical JSON projection of the seven `THM-M-0346` execution-DAG objects at the prior and current bases | 0 | Both projections hash to `ff3000b25705d750abb1f87f1978b380ac985f3a124e580503e26b96a76dbe51`; global generated-DAG changes concern other targets. |
| `cd Formalizations/Lean && timeout 120 lake env lean --version` | 0 | Lean 4.29.0 at commit `98dc76e3`; the pinned environment is available. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion manifest is deliberately absent because the proof phase is incomplete. |

Source SHA-256 values are `a2af9f8bfdb524a60b3fc3d2e3eaaa064d8e70063d90e25a5134c79ae0bc4a4d`
for `Statement.lean`, `690e35222ca644aaf708ba0ab2ffc5d886b60209d46511edea6bfc1a60fbb81d`
for `Proof.lean`, and `dbb718dbad1143a5423b426a916ef88b5c8f736965acbe7a7c4ead7772088bb1`
for `ObligationTree.lean`. The isolated object SHA-256 values were
`a349e94179235a765512cd39fca2fd50f09a0fb20009d0ad55155d2677906b82`,
`b7dd98fcb48d359df7bc92c1bea086896383aa08053f76772eb2852df44d2c91`, and
`2085328b3e8be96e6954d75a039f0ccc981a88cd07885f2d827273028968b7c5`.

## Boundary and retry condition

Lifecycle stays `planned`; the frozen root stays `[H3, M3, R4]`. The remaining root cut is
`M0346-C-REPRESENTATIVE`, `M0346-N-NORMALIZATION`, `M0346-N-CUTOFF`,
`M0346-L-CARLESON-HUNT`, and `M0346-T-AE-REP`. `audit_complete=false` and
`theorem_complete=false`. This record changes no scheduler state, accepts no receipt, and supports
no proof-completion, validation, release, audit-completion, theorem-completion, or master-acceptance
claim.

Resume after the integration lane provides an immutable, license-reviewed, placeholder-free
Carleson package compatible with the repository pins, or after a deliberate repository-wide pin
migration. Then import the real theorem, validate the exact external partial-sum transport, audit
its transitive terminal bodies and axioms, and compose the exact root. Until then,
`.stage1-worker-selftest.json` must remain absent.
