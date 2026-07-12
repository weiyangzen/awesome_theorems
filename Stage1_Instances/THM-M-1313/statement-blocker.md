# Statement gate blocker

Item: `S56-M-1313-STATEMENT`  
Theorem: `THM-M-1313`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The repository does not identify one exact singularity theorem. Its two underlying research
records disagree materially:

- `Docs/researches/math_theorems.md` gives the year 1965, joint attribution to Roger Penrose and
  Stephen Hawking, and only the gloss "singularities in general relativity";
- `Docs/researches/physics_theorems.md` gives the years 1965/1970, attribution to
  Penrose/Hawking, and the stronger but still informal gloss "gravitational collapse necessarily
  produces singularities."

Those data can refer to Penrose's 1965 trapped-surface theorem, later Hawking cosmological
singularity theorems, or the Hawking-Penrose 1970 theorem. These are not alternate spellings of one
claim: they have different causal, curvature, genericity, trapped-set, and initial-condition
hypotheses and different timelike/null geodesic-incompleteness conclusions. Even "singularity" must
be resolved to the appropriate geodesic-incompleteness statement; it must not be silently encoded
as a curvature-divergent point.

The intake's choice of Penrose 1965 is explicitly provisional. Its `intake.json` leaves the exact
dimension, differentiability, universe/typeclass context, causal and curvature conventions, and
formal declaration open. The source crosswalk likewise says the referent and conclusion remain
questions. Promoting that provisional reading to an exact Lean target would therefore invent
missing mathematics and violate the rev-5.6 prohibition on substituted or broadened theorems.

Section 5.1 requires the canonical claim before its binder context, elaborated expression,
expression/environment fingerprint, checked transports, and semantic mutations can be accepted.
Claim identity fails first here. Consequently there is no source-faithful expression on which to
run the removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutation tests.
No `axiom`, `sorry`, placeholder geometry, proxy proposition, or unproved declaration was added.
The machine state remains `M4`; statement acceptance and theorem completion remain false.

## Pinned environment and library boundary

- Repository base revision: `08421a58e672ceace1eb99b6ba8b479e5bbb3b05`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Toolchain pin: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Math research record SHA-256:
  `bdde11afb307986844ab56ec7002cf6e598ee533ca86e6546e395f60bef32a29`.
- Physics research record SHA-256:
  `6abf9da63cf075b0c6a05f3a245838ec0d7848fe873c43f529a7e0ee72cf94fa`.

A scoped search of all 7,871 pinned mathlib Lean files found no Penrose/Hawking singularity,
trapped-surface, Lorentzian-spacetime, Cauchy-hypersurface, or null-geodesic API. The only matches
were unrelated complex-analysis prose about Riemann's removable singularity theorem. This library
observation does not choose the canonical human claim and receives no statement or proof credit.

## Validation evidence

Commands ran from this worker clone. Lean used only the existing canonical pinned `.lake`
artifacts; no update, build, fetch, or clone command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1313` | 0 | rank 478, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | checked mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `find Formalizations/Lean/.lake/packages/mathlib/Mathlib -type f -name '*.lean' \| wc -l` | 0 | searched pinned library contains 7,871 Lean source files |
| `rg -n -i --glob '*.lean' 'Penrose singularity\|singularity theorem\|trapped surface\|null geodesic\|Lorentzian spacetime\|Cauchy hypersurface' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | only unrelated removable-singularity prose matched; no target-domain declaration or source reference |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Docs/researches/physics_theorems.md Docs/researches/math_theorems.md Stage1_Instances/THM-M-1313/intake.json` | 0 | pinned files and source/intake inputs were fingerprinted; intake SHA-256 is `71afe169a45af049965124ee2509adb427d554dc7ed4b567c60e9333f393b773` |

No target elaboration command is recorded because there is no exact target to elaborate. Compiling
an invented abstract interface would be a fake statement-gate result, not narrower validation.

## Retry condition

The authoritative lane must pin an immutable primary-source edition and an exact theorem/page, and
must justify whether this ID denotes Penrose 1965, Hawking-Penrose 1970, or another named result.
The source crosswalk must then freeze all domains, ordered binders, hypotheses, conventions,
conclusion, and degenerate cases. A later statement run can encode that claim against actual Lean
geometry APIs, elaborate it with minimal imports, preserve its expression/environment fingerprint,
check any transports, and execute all four mutation classes.

Until that happens the assigned phase is not genuinely self-tested to its completion gate.
Accordingly no `.stage1-worker-selftest.json` is emitted.
