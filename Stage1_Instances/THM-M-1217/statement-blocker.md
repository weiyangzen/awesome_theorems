# Statement-phase blocker

Item: `S56-M-1217-STATEMENT`  
Theorem: `THM-M-1217`  
Base revision: `a2044374af8048c248b7f7eecf9440b4d4e00485`

## Verdict

The exact-statement gate is blocked. No canonical Lean target has been created, and this phase is
not eligible for a worker self-test receipt.

The complete repository source record consists of the label "Tao theorem", attribution to Terence
Tao, the year 2006, and the phrase "global well-posedness of critical NLS". It provides no primary
publication, equation, theorem locator, or assumptions. In particular, it does not determine:

- mass-critical versus energy-critical scaling;
- focusing versus defocusing sign, exponent, spatial dimension, or equation normalization;
- radial versus unrestricted initial data and the critical initial-data space;
- the solution and uniqueness classes, continuous-dependence topology, or maximal interval; or
- whether spacetime bounds and scattering are part of the conclusion.

Each choice changes the mathematical proposition and its ordered Lean binders. Tao has distinct
results in nearby critical dispersive regimes, so neither the author nor the approximate year
selects a unique theorem. Choosing one candidate from memory would broaden or substitute the
source claim. Rev-5.6 section 5 therefore prevents freezing a canonical statement, elaborated
expression hash, checked transports, or the four required mutation classes.

The historical module `AwesomeTheorems.Stage1.S1_M_153` does not resolve the identity failure. It
documents a Cazenave-Weissler local critical-NLS statement candidate and analytic interfaces, not
an exact Tao global well-posedness theorem. Its successful elaboration below is toolchain and
discovery evidence only. It receives no statement or proof credit for `THM-M-1217`.

The intake grades remain `[H4, M4, R4]`; statement acceptance, audit completion, and theorem
completion remain false. No proxy predicate, unconstrained `Prop`, axiom, placeholder, or weakened
theorem was introduced.

## Environment fingerprint

- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Historical discovery module SHA-256:
  `9a1eaa222369ee2d623422cba4183773f380d17dff0a0dab0149998754ff8eff`.

## Commands and results

Commands ran in this worker clone. Lean used the existing pinned `.lake` artifacts. No update,
build, dependency clone/fetch, or other `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1217` | 0 | rank 408, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_153.lean` | 0 | historical Cazenave-Weissler candidate module elaborated; this does not establish Tao statement identity |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_153.lean` | 0 | hashes match the environment fingerprint above |

## Retry condition

Provide an immutable primary-source edition and a pinpoint theorem/page that identifies the
intended result, including all referenced definitions and errata. A later statement run can then
crosswalk and freeze the exact equation, criticality, dimension, sign, data and solution spaces,
symmetry hypotheses, ordered quantifiers, well-posedness components, and any scattering conclusion;
encode the result with minimal pinned imports; and run the required domain, hypothesis, binder, and
boundary mutations.

Until that source identity is available, no `lake env lean <canonical-target>` command can be run
truthfully. Consequently `.stage1-worker-selftest.json` is intentionally absent.
