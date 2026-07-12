# Statement-phase blocker

Item: `S56-M-0343-STATEMENT`  
Theorem: `THM-M-0343`  
Worker base revision: `bd0d227173ac95971603f633607751754850337e`

## Gate decision

The exact Lean 4 target cannot be elaborated truthfully from the repository source record. The
record names the Poisson summation formula but supplies only `傅里叶级数与傅里叶变换的关系` ("the
relationship between Fourier series and the Fourier transform"). It gives no displayed equality,
function class, convergence hypotheses, Fourier-transform normalization, lattice scale,
translation parameter, ordered binders, or boundary cases. It also gives no source edition,
theorem number, or page from which those choices could be recovered.

At least these inequivalent statements remain compatible with the metadata:

1. the general translated identity for a continuous `ℝ → ℂ` function under local uniform
   summability of integer translates and summability of Fourier samples;
2. the same identity under polynomial decay of both the function and its Fourier transform;
3. the Schwartz-function specialization;
4. an unshifted `x = 0` identity or a scaled-lattice variant.

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the first three
variants in `Mathlib.Analysis.Fourier.PoissonSummation`, but availability does not select one as the
repository's canonical claim. Choosing one would add mathematical content absent from the source
and could substitute a stronger, weaker, or differently normalized theorem. Consequently there is
no canonical expression to serialize or hash, no credited alternate encoding to transport, and no
sound removed-hypothesis, changed-domain, changed-scope, or boundary mutation suite. Section 5.1 of
the rev-5.6 blueprint therefore fails before proof evidence may be inspected.

`IntakeProbe.lean` was re-elaborated only to distinguish an available pinned Lean environment from
a missing exact mathematical statement. It confirms candidate APIs, not a canonical target, and
receives no statement or proof credit. No `sorry`, `admit`, or `axiom` occurs in the target's Lean
source.

## Exact validation record

Validation date: `2026-07-12` (`Asia/Shanghai`). The worker clone's `.lake` path resolves to the
pre-existing canonical pinned artifact and was used read-only. No dependency update, build, fetch,
or clone was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets; ranks 1..1546; all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0343` | 0 | rank 836; planned; legacy artifacts unaccepted; theorem_complete false |
| `rg -n -i 'THM-M-0343\|泊松求和公式\|Poisson summation formula\|傅里叶级数与傅里叶变换的关系' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Docs/Stage1_Targets_rev-5.6.json` | 0 | only the name, topic gloss, and manifest metadata were found; no exact proposition or source pinpoint |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0343/IntakeProbe.lean)` | 0 | four candidate Poisson-summation declarations elaborated; no canonical theorem target asserted |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0343 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom found |
| `python3 -m json.tool Stage1_Instances/THM-M-0343/instance.json` | 0 | intake JSON is syntactically valid |
| `python3 -m json.tool Stage1_Instances/THM-M-0343/task-dag.json` | 0 | task DAG JSON is syntactically valid |

## Required unblocker and status boundary

The first unblocker is an immutable, independently inspected human-source passage that states one
exact formula and fixes its function class, Fourier convention, lattice and translation parameters,
ordered hypotheses, conclusion, and boundary cases. Only then can the minimal import and canonical
Lean expression be frozen, the normalized expression fingerprinted, alternate encodings transported,
and all four required mutation classes executed.

This statement node remains `[ ]` and blocked at `M4`. The root remains `[H3, M4, R4]` with
`audit_complete: false` and `theorem_complete: false`. No worker self-test manifest is emitted,
because the assigned statement deliverable did not pass its gate.
