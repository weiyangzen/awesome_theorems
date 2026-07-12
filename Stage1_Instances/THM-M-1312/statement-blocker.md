# Statement-phase blocker

Item: `S56-M-1312-STATEMENT`  
Base revision: `4d48a3c5fbec6d005a64a99338e40c001656264c`

## Verdict

The exact Choquet-Bruhat-Geroch target cannot be elaborated from the pinned
repository environment without inventing the missing mathematical object
model. The statement gate is therefore blocked, and this artifact does not
claim a self-tested `[_]` handoff.

The intake freezes the human claim as existence and uniqueness, up to an
initial-data-preserving isometry, of a maximal globally hyperbolic development
for vacuum Einstein initial data satisfying the constraints. An exact Lean
encoding consequently needs concrete definitions for at least:

- smooth three-dimensional vacuum initial data, its Riemannian metric and
  symmetric second fundamental form;
- the Hamiltonian and momentum constraints;
- time-oriented Lorentzian spacetime developments and induced initial data;
- the vacuum Einstein equation, Cauchy hypersurfaces, global hyperbolicity,
  extension/embedding of developments, maximality, and isometry preserving the
  initial embedding.

Neither the pinned mathlib tree nor this target's owned path supplies those
definitions. Their absence is a statement-model blocker, not merely missing
proof content.

## Legacy candidate rejection

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_168.lean` elaborates, but it is
not an exact encoding of the intake claim. In particular:

- `EinsteinInitialData.constraintEquations` and the regularity, hypersurface,
  gauge, and reduction fields are unstructured propositions;
- `EinsteinDevelopment.spacetimeMetric` is only `M -> M -> Prop`, not a
  Lorentzian metric;
- the Einstein equation, induced-data, global-hyperbolicity, Cauchy-surface,
  maximality, and uniqueness conditions are proposition-valued fields supplied
  by the purported development;
- `HasMaximalGloballyHyperbolicDevelopment` asks only for `Nonempty
  EinsteinDevelopment` and does not require
  `IsMaximalGloballyHyperbolicDevelopment`;
- therefore `StatementShape` can be satisfied by packaging proposition fields
  and does not state the source theorem's geometric/PDE conclusion.

Promoting this candidate would substitute an abstract record-inhabitation
claim for the named theorem. Adding the required structures locally during
this phase would likewise invent unresolved mathematics rather than elaborate
an intake-frozen exact target.

## Mutation gate

The required removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations cannot be meaningfully frozen or killed until the
canonical expression exists. The legacy file's proposition-valued fields do
not provide valid mutation evidence for the source theorem.

## Commands and results

Commands were run from the repository root on 2026-07-12. No dependency update,
fetch, build, or mutation of the shared `.lake` artifacts was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard check passed: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | Manifest check passed: 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1312` | 0 | Rank 168, `planned`, L0/rework-required, theorem incomplete |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_168.lean` | 0 | The legacy abstract candidate elaborated; this is negative discovery evidence, not exact-statement evidence |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | Hashes `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` and `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| `rg -l -i "Lorentzian\|globally[ _-]?hyperbolic\|Einstein (equation\|tensor)\|Cauchy development\|Choquet.Bruhat\|Geroch" Formalizations/Lean/.lake/packages/mathlib/Mathlib -g '*.lean' \| wc -l` | 0 | `0` matching Lean source files in the pinned mathlib tree |
| `rg -n "structure EinsteinInitialData\|structure EinsteinDevelopment\|spacetimeMetric :\|constraintEquations : Prop\|globallyHyperbolic : Prop\|maximalAmongGloballyHyperbolicDevelopments : Prop\|uniquenessUpToIsometry : Prop" Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_168.lean` | 0 | Confirmed the abstract proposition/relation fields at lines 41-67 |
| `test ! -e .stage1-worker-selftest.json` | 0 | No self-test receipt was emitted for the blocked phase |
| `git diff --check -- Stage1_Instances/THM-M-1312` | 0 | No whitespace errors in the owned artifact |

## First failed gate and unblock condition

The first failed gate is rev-5.6 section 5.1: no exact canonical Lean expression
exists to fingerprint. The phase can resume only after a dependency-pinned,
source-crosswalked Lorentzian/Einstein/Cauchy-development object model is
available, or after those definitions are implemented and independently
audited as faithful to the source claim. At that point the exact target,
checked alternate transports, all four mutation classes, serialized expression,
and environment fingerprint must be produced and re-elaborated.

Root status remains `[H1, M3, R3]`; no theorem, proof, audit, validation, or
release completion is claimed.
