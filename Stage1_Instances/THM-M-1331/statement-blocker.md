# Exact-statement gate: blocked

Item: `S56-M-1331-STATEMENT`

Theorem: `THM-M-1331`

Base revision: `d4646fb26544dad2bd601137067a00d47064a074`

Verdict: `blocked`

## Decision

The exact Lean 4 target cannot be truthfully selected or elaborated from the repository record.
The complete mathematical gloss is only "existence and uniqueness of solutions under a Lipschitz
condition." It does not fix the ODE, time and state domains, local region, regularity and bound
assumptions, initial data, interval, solution predicate, endpoint convention, or class in which
uniqueness holds. Each choice changes the proposition rather than merely its notation.

There is also an unresolved identity collision. The immediately adjacent `THM-M-1332` separately
names the Picard-Lindelof theorem and describes existence and uniqueness of ODE solutions. The
current dossier contains no immutable primary-source transcription and no approved decision that
the targets are distinct, aliases sharing one semantic root, or a catalogue error. Selecting the
familiar Cauchy-Lipschitz/Picard-Lindelof theorem for `THM-M-1331` would therefore invent material
assumptions and may count the same theorem twice.

The first failed substantive statement gate is exact source-statement and target identity under
rev-5.6 sections 5 and 5.1. The intake dependency is still provisional `[_]`, so master acceptance
would additionally be dependency-blocked even if the intrinsic statement ambiguity were resolved.

## Lean boundary

The pinned Lean environment is available. The existing `IntakeProbe.lean` imports only the two
adjacent ODE modules and successfully elaborates nine discovery interfaces. The relevant halves are:

- `IsPicardLindelof.exists_eq_forall_mem_Icc_hasDerivWithinAt` for local existence;
- `ODE_solution_unique_of_mem_Icc`, `_eventually`, `ODE_solution_unique`, and `_univ` for variants
  of uniqueness.

They do not supply a source-approved combined target. The existence result permits the initial time
anywhere in `Icc` and returns `HasDerivWithinAt` on that closed interval. The central uniqueness
result requires the initial time in `Ioo`, ordinary `HasDerivAt` in the interior, continuity on the
closed interval, and range membership in a time-indexed set. The right/left uniqueness variants use
`Ico`/`Ioc` with one-sided derivatives. Aligning those conventions needs mathematical choices and a
checked bridge after the source target is frozen; it is not a harmless wrapper.

Consequently no canonical declaration or expression is created. There is no honest claim of
minimal target imports, expression or canonical-environment fingerprint, alternate transport, or
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutation coverage. The
passing API probe is only `M3` feasibility evidence.

## Validation record

Commands ran in this worker clone on 2026-07-13 (`Asia/Shanghai`). The automation-provided
canonical `.lake` symlink was used read-only. No `lake update`, build, clone, fetch, or dependency
mutation was run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1331` | 0 | rank 943; planned; L0/rework-required; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, target `x86_64-unknown-linux-gnu` |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e` with Lean 4.29.0 |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree}` | 0 | revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Stage1_Instances/THM-M-1331/IntakeProbe.lean` | 0 | `651c8acc...b1d2`, `321626c8...2d81`, and `57081962...3aaf3f` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1331/IntakeProbe.lean)` | 0 | all nine discovery-only existence, uniqueness, fixed-point, flow, and autonomous-special-case interface types elaborated and printed |
| `python3 Stage1_Instances/THM-M-1331/check_intake.py` | 1 | `FileNotFoundError` for root `.stage1-worker-selftest.json`; the historical intake validator requires its prior provisional intake packet, which is absent from this phase clone |
| `python3 -m json.tool Stage1_Instances/THM-M-1331/statement-blocker.json` | 0 | finalized structured blocker is valid JSON |
| scoped prohibited-declaration `rg` scan over `Stage1_Instances/THM-M-1331/*.lean` | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |
| per-file `git diff --no-index --check /dev/null` for both new blocker files | 1 each | expected new-file difference exits with no diagnostic; no whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | the ineligible worker self-test manifest is absent |

The intake-validator failure is a known historical replay limitation, not a reason to manufacture
a root packet: this statement phase is blocked and is expressly ineligible for one. The validator
also owns a closed historical intake inventory; it is deliberately not edited to rewrite the prior
phase's evidence around this statement report.

## Retry condition

First obtain master acceptance of the intake. Then preserve and hash an immutable primary source,
select and independently approve its exact theorem and incorporated definitions, and resolve the
relationship with `THM-M-1332` as distinct statements, a deduplicated alias, or a correction. The
source review must freeze every domain, ordered binder, hypothesis, conclusion, convention, and
boundary case. A fresh statement attempt can then encode that same claim, prove any required
existence/uniqueness bridge, minimize its pinned imports, serialize and hash the elaborated
expression and environment, check alternate transports, and execute all four mutation classes.

The dossier remains `planned` at `[H1, M3, R4]`. `audit_complete` and `theorem_complete` remain
false, and all six remaining nodes remain in the root cut set. No statement completion or worker
`[_]` claim is made. Because the assigned phase did not pass its completion gate, root
`.stage1-worker-selftest.json` is deliberately absent.
