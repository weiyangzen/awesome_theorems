# Exact-statement gate: blocked

Item: `S56-M-0991-STATEMENT`  
Theorem: `THM-M-0991`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The complete repository source statement is only "rate of convergence in the central limit
theorem." It gives a theorem name, attribution, and year, but no immutable primary-source edition,
pinpoint theorem or pages, hypotheses, normalization, constant, or errata. This does not select one
exact Berry-Esseen proposition. Materially different classical forms include independent versus
i.i.d. summands, an exact or bounded third absolute centered moment, normalized or unnormalized
variance, a universal existential constant versus a stated numerical constant, and pointwise-for-all
thresholds versus a supremum norm. Choosing among them here would substitute an unstated theorem.

The intake cites Berry's 1941 paper only as an uninspected discovery candidate and has no pinpoint
for Esseen. Those references therefore cannot authorize ordered binders, assumptions, constant
dependencies, or boundary conventions. This is the rev-5.6 section 5 hard stop: without the exact
human claim there can be no faithful canonical expression hash, credited transports, or meaningful
removed-hypothesis, changed-domain, changed-binder-scope, and boundary mutations.

The legacy declaration
`AwesomeTheorems.Stage1.S1_M_271.StatementShape` does not resolve the ambiguity. It quantifies over
`BerryEsseenIIDData`, whose `constant` is supplied separately for every data package. Because the
conclusion must then hold even for `constant = 0`, it is not the usual claim that there exists one
absolute universal constant. It also commits to the i.i.d. specialization without a source
pinpoint. Adopting it would preserve a material constant-quantifier mismatch rather than elaborate
the exact catalog theorem.

No canonical Lean file, proxy predicate, assumed conclusion, broadened conjunction, or substituted
special case was introduced. The successful legacy elaboration below is substrate/discovery
evidence only. The dossier remains `planned` with `[H1, M3, R3]`; statement acceptance, audit
completion, and theorem completion remain false.

## Environment fingerprint

- Repository base revision: `c6077f63d112c9e6b348b0e7e2370bc1b6024593`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Legacy discovery module SHA-256:
  `14e34f2a6f4a225a37e1d3009448317de11463392f6b910ac34526a889022aca`.

## Validation evidence

Commands ran in this worker clone. Lean used the existing symlink to the canonical pinned `.lake`
artifacts. No update, build, fetch, clone, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0991` | 0 | rank 271, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_271.lean` | 0 | legacy CDF-rate boundary and adjacent declarations elaborated; this does not establish exact source identity |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision matched the fingerprint |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_271.lean` | 0 | all three hashes matched the fingerprint |

## Retry condition

Provide an immutable primary-source edition and a pinpoint theorem and pages, including referenced
definitions and errata. Crosswalk whether the intended result is i.i.d. or merely independent, the
moment and variance normalizations, positivity and nondegeneracy conditions, CDF convention,
positive-integer range, and the exact universal-constant quantification. A later statement run can
then encode that claim with minimal pinned imports, check transports to any alternate formulation,
fingerprint the elaborated expression, and run all four required mutation classes.

Until then the assigned phase cannot be genuinely self-tested to its completion gate. Consequently
no `.stage1-worker-selftest.json` is emitted, and no downstream state is advanced.
