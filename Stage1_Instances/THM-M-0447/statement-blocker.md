# Statement gate blocker

Item: `S56-M-0447-STATEMENT`  
Theorem: `THM-M-0447`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The repository metadata names the "Taylor-Wiles method" and glosses it only as "modularity lifting
for Galois representations." This does not identify one theorem. The intake provisionally narrows
the topic to the classical minimal two-dimensional odd setting over `Q`, but explicitly leaves open
whether the canonical root is an `R = T` theorem or a modularity-lifting consequence. It also leaves
unfixed the coefficient prime and ring, residual determinant and restriction hypotheses, local
conditions at the coefficient prime, ramification set, Hecke algebra and localization, and the
precise compatibility conclusion. Those choices change both the ordered binders and the
proposition. Neither the Stage0 record nor the intake crosswalk supplies a pinpoint theorem/page
whose complete hypotheses resolve them.

Selecting one Taylor-Wiles or Wiles theorem now would therefore invent missing mathematics or
substitute a narrower claim for the metadata. Under rev-5.6 sections 2 and 5, unresolved target
identity and a missing expression fingerprint are hard statement blockers.

The legacy module `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_065.lean` cannot repair the
failure. Its `SelectedStatementShape` is an abstract interface: essential arithmetic content is
stored in locally defined `Prop` fields such as `isREqualsT`,
`taylorWilesNumericalCriterion`, and `patchedModuleFaithful`; its conclusion is then obtained only
after those fields are assumed. The module itself describes the declaration as a statement-shape
candidate rather than a source-faithful terminal theorem. It elaborates successfully, but receives
no exact-statement or proof credit.

Consequently the exact domains, ordered binders, hypotheses, conclusion, degenerate cases,
normalized expression, expression hash, and meaningful removed-hypothesis, changed-domain,
binder-scope, and boundary mutations cannot truthfully be frozen. Machine debt remains `M4`. No
`sorry`, axiom, proxy predicate, placeholder theorem, or broadened alternate claim was introduced.

## Environment fingerprint

- Repository base revision: `91cf43768c2b03b5c98d8ca436c450ba5a70babb`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Legacy discovery module SHA-256:
  `f66bb518e9d15ff8bb172a76e2fc0a0c07994d4729ad29ff18c008ee6f584608`.

The worktree's `Formalizations/Lean/.lake` is an existing symlink to the canonical pinned Lake
artifacts and appears untracked in this automation clone. It was used read-only. This is scoped,
nonrelease evidence; no update, build, fetch, or clone command was run.

## Validation evidence

Commands ran from this worker clone with the existing pinned `.lake` artifacts.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_065.lean` | 0 | Legacy interface and statement-shape module elaborated; this does not establish exact source identity |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Checked mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_065.lean` | 0 | Produced the three hashes recorded above |
| `rg -n -i 'Taylor[- ]?Wiles\|modularity lifting\|deformation ring.*Hecke\|R ?= ?T' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | Only a Taylor-Wiles bibliographic mention in `Mathlib/NumberTheory/FLT/Basic.lean` was relevant; no terminal statement was found |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0447` | 0 | Rank 65, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |

## Retry condition

The authoritative lane must select an immutable primary-source theorem and pinpoint location,
declare whether `R = T` or modularity lifting is the root, and transcribe every referenced
coefficient, residual, local, ramification, Hecke, and compatibility assumption. The next statement
run can then encode that proposition using pinned Lean interfaces, reject or transport the legacy
candidate, serialize its elaborated expression, and execute the four required mutation classes.

Until then, statement acceptance and theorem completion are false. Because the assigned phase is
not genuinely self-tested to its completion gate, no `.stage1-worker-selftest.json` is emitted.
