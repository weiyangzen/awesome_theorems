# Exact-statement gate: blocked

Item: `S56-M-1243-STATEMENT`  
Theorem: `THM-M-1243`  
Base revision: `7619d195bd4454d4084e74977cf56d86c396ab3a`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the accepted intake and repository
source record. The only inherited description is "Nash inequality" / "the relation between entropy
and energy." The intake deliberately narrows this to a candidate family, while leaving the exact
historical equation, exponents, constant normalization, dimension convention, function class,
gradient notion, and norm-versus-integral presentation unresolved. These choices determine
different propositions and different boundary behavior. Selecting one here would invent a
canonical claim rather than transcribe the repository's identified claim.

The discovery citation to Nash's 1958 paper has no immutable local copy, content hash, accepted
page/equation locator, assumption transcription, or corrections review. In particular, the
repository does not determine whether the root is the classical smooth compact-support inequality,
an extension to an `L1` Sobolev class, or an entropy-family statement suggested by the Stage0
wording. The intake explicitly makes the smooth-to-Sobolev extension a separate bridge and excludes
silently treating it as the historical statement.

Consequently the phase fails at canonical human-claim identity, before a Lean expression,
minimal-import claim, expression hash, checked representation transport, or meaningful mutation
suite can be produced. No statement receipt, machine-proof credit, audit completion, or theorem
completion is claimed. The machine status remains `M4` as recorded by the intake.

## Repository and pinned-environment inspection

The target manifest confirms execution rank 424, `planned` lifecycle, uniform `L0 / rework_required`
baseline, and an incomplete theorem. A case-insensitive search of pinned mathlib and the repository's
Lean modules found no declaration whose name mentions both Nash and inequality. That negative name
search is only discovery evidence; it is not a bounded anchor audit and does not resolve the source
ambiguity.

The pinned Lean environment is available, but there is no exact proposition on which a Lean
elaboration command could honestly operate. Running a synthetic or weakened proposition merely to
obtain exit code zero would not validate the assigned deliverable.

## Narrow validation evidence

Commands ran in this worker clone on 2026-07-12. The Lean commands only inspected the existing
pinned `.lake` artifacts; no dependency was updated, built, cloned, or fetched.

| Working directory | Command | Exit | Result |
|---|---|---:|---|
| repository root | `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| repository root | `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| repository root | `python3 scripts/stage1_target.py show THM-M-1243` | 0 | rank 424, planned, legacy artifacts unaccepted, theorem incomplete |
| `Formalizations/Lean` | `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `Formalizations/Lean` | `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `Formalizations/Lean` | `sha256sum lean-toolchain lake-manifest.json` | 0 | toolchain hash `651c8acc...b1d2`; manifest hash `321626c8...2d81` |
| `Formalizations/Lean` | `rg -n -i 'nash.*inequal\|inequal.*nash' .lake/packages/mathlib/Mathlib AwesomeTheorems` | 1 | no matching declaration name or source text found |

## Required unblock

An accountable source reviewer must preserve an immutable primary-source edition and record its
content hash, exact page/equation, surrounding definitions, ordered assumptions, normalization,
and corrections review. The review must decide the Euclidean dimension convention, scalar field,
function class, derivative notion, finite-integrability assumptions, constant quantification, exact
exponents, and treatment of the zero function and zero-dimensional space. It must also decide
whether the Stage0 entropy wording is erroneous or identifies a different Nash result.

After that source decision, a statement worker can encode precisely that proposition, minimize
imports by deletion, serialize and hash the elaborated expression and environment, implement any
credited norm/integral or smooth/Sobolev transports, and test removed-hypothesis, changed-domain,
binder-scope, and boundary mutations.

Because the assigned phase is blocked rather than genuinely self-tested, the workspace-root
`.stage1-worker-selftest.json` is intentionally absent. Master acceptance remains outstanding.
