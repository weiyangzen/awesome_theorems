# Exact-statement gate: blocked

Item: `S56-M-0108-STATEMENT`

Theorem: `THM-M-0108`

Base revision: `f3113c54b9f211684b537a151ecc735272dae987`

## Decision

No exact native Lean 4 target for Chow's theorem can be elaborated in the
pinned dependency closure without inventing a root-critical interface or
choosing among proposition-changing interpretations that the intake leaves
open. The intended claim is that every closed complex-analytic subvariety of
finite-dimensional complex projective space is algebraic. The intake does not
yet settle reduced analytic subset versus possibly nonreduced analytic
subspace, equality of carriers versus equality of structured spaces, or the
exact source convention for "variety" and "algebraic."

Pinned mathlib supplies useful but separate surfaces:

- complex-manifold and analytic-function infrastructure, including
  `IsManifold`, `MDifferentiable`, `AnalyticOnNhd`, and analytic evaluation of
  multivariate polynomials;
- the bare quotient `Projectivization Complex (Fin (n + 1) -> Complex)`, but
  not an inferred topology or complex-manifold structure on that carrier;
- homogeneous multivariate polynomials and homogeneous ideals;
- the algebraic `ProjectiveSpectrum` carrier, its Zariski topology,
  `zeroLocus`, and `vanishingIdeal`.

It does not supply a native closed complex-analytic subset/subspace object on
finite complex projective space or an analytification/comparison transport to
the algebraic `ProjectiveSpectrum` zero-locus surface. The owned
`StatementInfrastructure.lean` probe checks the available adjacent APIs and
confirms the expected failure to infer a topology on the bare finite complex
`Projectivization`. It declares no Chow target, substitute analytic predicate,
axiom, or proof. Its five imports are probe-only and are not a minimal import
claim for a canonical target that does not exist.

The legacy `AwesomeTheorems.Stage1.S1_M_032.StatementShape` cannot cure the
gap. Its analytic predicate unfolds to `Z ⊆ Set.univ`, and its algebraic
predicate unfolds to `Z = Z`; both are expressly labeled placeholders in that
module and excluded by the intake scope. Reusing them, locally recreating
abstract predicates, or treating the theorem that every Zariski-closed
`ProjectiveSpectrum` set is a zero locus as Chow's theorem would substitute a
strictly weaker and largely tautological proposition.

The canonical Lean expression, minimal imports, expression fingerprint,
checked analytic/algebraic transports, and four required mutation classes are
therefore undefined. The statement gate fails closed before proof evidence is
inspected. Lifecycle remains `planned`, the root vector remains
`[H1, M3, R4]`, and both audit and theorem completion remain false.

The predecessor is also not master-accepted: `S56-M-0108-INTAKE` is only
provisional `[_]`. Concurrent preparation permits this truthful blocker, but
no statement transition may be accepted before dependency-ordered master
review.

## Pinned environment

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
  tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`.
- The automation-provided canonical `.lake` symlink was used read-only. No
  update, build, clone, fetch, or dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-15 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0108` | 0 | rank 32, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0108/StatementInfrastructure.lean` | 0 | adjacent analytic, projective, homogeneous, and zero-locus APIs elaborated; the expected projectivization-topology synthesis failure was confirmed; stdout SHA-256 `b5cd8990b451b9054d4c321dfaf82cfc1d80adb854bd58924d3d2f0899661139` |
| bounded pinned-mathlib searches for native closed complex-analytic subspaces, analytification/GAGA/Chow comparison, and projectivization topology/manifold APIs | 1 each | expected no-match results; no root-critical native interface was located |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean and Lake versions above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` and `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 each | pinned revision and tree above; empty status output confirmed a clean package worktree |
| `python3 -m json.tool Stage1_Instances/THM-M-0108/statement-blocker.json` | 0 | structured blocker parsed as valid JSON |
| prohibited-declaration scan of the owned Lean probe | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| `git diff --check -- Stage1_Instances/THM-M-0108` plus `git diff --no-index --check /dev/null FILE` for each new owned file | 0 for tracked check; 1 for each new-file check | expected new-file difference exits had empty diagnostics; no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test packet because the exact-statement deliverable did not pass |

## Retry condition

First approve an immutable primary-source passage that fixes the theorem's
variety, reducedness, structured-versus-carrier, closedness/compactness, and
boundary conventions. Then pin or implement a native closed complex-analytic
subset/subspace API on finite complex projective space, its compatibility with
the algebraic projective-space model, and a homogeneous-zero-locus or closed-
subscheme conclusion with checked transports. A fresh statement run can then
encode only that approved claim, minimize imports, serialize the elaborated
expression and environment, compile every credited alternate encoding, and
run removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations. The intake must also receive master acceptance before the statement
node can be accepted.

This blocker is the assigned phase's truthful result, not statement completion
or theorem completion. No `.stage1-worker-selftest.json` or statement receipt
is emitted.
