# THM-M-1384 statement-phase blocker

- Item: `S56-M-1384-STATEMENT`
- Base revision: `c2467750f2cdb3960045c83e819d96687253303d`
- Attempt date: 2026-07-13 (Asia/Shanghai)
- Verdict: blocked; no statement receipt or theorem-completion claim

## First failed gate

The exact-statement gate in section 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md` cannot be entered
truthfully from the received source record. `Docs/researches/math_theorems.md:10083-10088` gives
only the label `Sturm-Liouville theory`, the joint Sturm/Liouville attribution, the year 1836,
and the gloss `second-order linear boundary-value problem`. It supplies no cited proposition,
equation, definitions, hypotheses, conclusion, proof boundary, correction history, or review. The
Stage0 projection explicitly leaves the exact definitions and assumptions open.

This omission is proposition-defining. The record does not select an equation normalization, a
regular or singular domain, finite or infinite endpoints, coefficient regularity and sign
conditions, classical or weak solution semantics, an operator domain, separated or coupled
boundary forms, or a conclusion. Solvability, Green representation, self-adjointness, spectral
reality and discreteness, eigenfunction completeness, comparison, separation, oscillation,
asymptotics, variational characterizations, and transformations are materially different claims.
Selecting any familiar finite-interval spectral theorem would invent or substitute mathematics
rather than elaborate the exact received target.

The predecessor intake is provisional `[_]`, has no accepted receipt ID, and freezes the canonical
statement, formal module, exact expression, expression hash, and environment fingerprint as null at
`[H5, M4, R4]`. Its worker receipt is unsigned, unaccepted, and stale against the regenerated
blueprint and execution DAG. Consequently there is no canonical expression to elaborate, no honest
minimal-import claim, and no meaningful checked transport or removed-hypothesis, changed-domain,
changed-binder-scope, or boundary-case mutation. The statement node remains open and is not
self-tested complete.

## Source boundary

The intake inspected Sturm's 1836 memoir and linked errata, NIST DLMF Section 1.13(viii), the
Encyclopedia of Mathematics entry at immutable revision 55171, and Teschl Sections 5.3-5.6. These
sources establish a serious theorem family, but they also distinguish finite regular and singular
problems, several boundary regimes, transformations, operator and spectral results, Green
resolvents, and oscillation. The catalog cites none of them and selects no proposition within them.
No exact passage, incorporated-definition map, proof boundary, correction map, historical
attribution decision, or independent source review is accepted.

The neighboring records also prevent a topical substitution: `THM-M-1383` owns general two-point
boundary-value theory, while `THM-M-1385` through `THM-M-1392` separately own comparison,
separation, oscillation, eigenvalue, Weyl-asymptotic, Courant-min-max, Pruefer, and Green-function
targets. None can define this root or donate statement credit.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated in the pinned environment. Its four direct
imports expose thirteen adjacent derivative, ODE, eigenvalue, symmetric-operator,
compact-operator, spectrum, and Rayleigh declarations. All checks passed, but the probe explicitly
defines no Sturm-Liouville expression, solution predicate, operator domain, boundary conditions,
target, transport, or proof body. Its imports therefore are not claimed minimal for an unidentified
target.

A bounded exact-topic search found no Sturm-Liouville terminal declaration in pinned mathlib. The
only non-probe repository match was a planning string in an unrelated legacy module. This is
feasibility evidence, not the downstream anchor audit or a proof of global absence.

The environment was Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided `.lake` symlink and pinned
artifacts were used read-only. No `lake update`, `lake build`, dependency clone or fetch, or other
`.lake` mutation was run.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1384` | 0 | rank 994; `planned`; `L0/rework_required`; no legacy slot; theorem incomplete |
| `git status --short --untracked-files=all` | 0 | before this attempt, only the automation-provided `Formalizations/Lean/.lake` symlink was untracked |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | revision `c2467750f2cdb3960045c83e819d96687253303d`; tree `0f79eb697267dc28b29d41a1e282f319d758a2ac` |
| `git blame -L 10083,10088 -- Docs/researches/math_theorems.md` | 0 | all six catalog lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake versions recorded above |
| `cd Formalizations/Lean && git -C .lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision and tree recorded above; package status was clean |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | SHA-256 `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` and `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1384/IntakeProbe.lean` | 0 | all thirteen adjacent APIs elaborated; stdout 2720 bytes, SHA-256 `ac028e1169b8e992d0aac97fb938547024be09f08fea05ac3f1bbe994c2e0008`; no target or proof body |
| bounded exact-topic `rg` search in pinned mathlib and repo-local Lean | 0 | only the probe disclaimer and one unrelated legacy planning string matched; no terminal declaration found |
| `python3 -B Stage1_Instances/THM-M-1384/check_intake.py` | 1 | historical intake replay first detects its stale recorded blueprint hash; historical evidence was preserved rather than rewritten |
| prohibited-declaration scan over target Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `python3 -m json.tool Stage1_Instances/THM-M-1384/statement-blocker.json` | 0 | blocker parsed as valid JSON |
| scoped blocker-invariant validation | 0 | identity, base, current input hashes, null target, unchanged vector, four unrunnable mutations, false completion fields, owned changes, and absent worker packet agree |
| scoped whitespace checks | 0 | no whitespace diagnostics |
| `test ! -e .stage1-worker-selftest.json` | 0 | worker self-test manifest is absent as required for a blocked phase |

## Unblocking condition

An accountable source owner must preserve and hash a lawful complete source edition, select one
exact theorem or explicitly delimited conjunction and its proof boundary, transcribe every
incorporated definition, ordered binder, hypothesis, conclusion, convention, correction, and
boundary case, resolve ownership relative to neighboring targets, and obtain independent source,
history, and scope approval. A fresh statement run can then encode that same proposition, minimize
its pinned imports, serialize and hash its elaborated expression and environment, compile every
credited transport, and run all four required mutation classes. The integration lane must also
accept the refreshed intake dependency before accepting any statement transition.

Until those conditions hold, no exact statement, proof, audit completion, or theorem completion is
claimed. Because the assigned phase did not pass its completion gate, no
`.stage1-worker-selftest.json` is emitted.
