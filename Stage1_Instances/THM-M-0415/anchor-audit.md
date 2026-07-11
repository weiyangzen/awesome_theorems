# THM-M-0415 Lean 4 anchor audit

Audit date: 2026-07-12. The audit is scoped to the exact frozen target
`Stage1Instances.THM_M_0415.IdealClassGroupFiniteTarget` and inventory version
`THM-M-0415-anchor-inventory/1`.

## Immutable mathlib result

The locally available mathlib checkout is clean at commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, from
`https://github.com/leanprover-community/mathlib4.git`, with toolchain
`leanprover/lean4:v4.29.0`. No dependency fetch, update, build, or mutation was
performed.

The exact candidate is
`NumberField.RingOfIntegers.instFintypeClassGroup` in
`Mathlib.NumberTheory.NumberField.ClassNumber`. For arbitrary `K`, `[Field K]`,
and `[NumberField K]`, it supplies
`Fintype (ClassGroup (NumberField.RingOfIntegers K))`. This matches the target's
domain and object and is stronger only in carrying `Fintype` data.
`AnchorAudit.lean` checks the direct wrapper to the frozen `Finite` conclusion.

The immediate mathlib body specializes
`ClassGroup.fintypeOfAdmissibleOfFinite` to `R = Q`, `L = K`, and
`AbsoluteValue.absIsAdmissible`. The latter construction lives in
`Mathlib.NumberTheory.ClassNumber.Finite` and routes through
`ClassGroup.fintypeOfAdmissibleOfAlgebraic`, a finite approximation of ideals,
and a surjection onto the class group. Exact source blobs, SHA-256 digests,
license, candidate comparison, and deduplication are recorded in
`anchor-audit.json`. The legacy `S1_M_070` theorem is only a duplicate wrapper
over this same terminal route.

The scoped owning-source scan found no `sorry`, axiom declaration, unsafe
declaration, or external oracle. Lean's axiom report for the exact wrapper is
`propext`, `Classical.choice`, and `Quot.sound`; this is discovery-stage trust
information, not a completed transitive trust or release audit.

## External Lean 4 search

Repository-local and pinned mathlib searches used declaration names, `Finite`
and `Fintype` spellings, "ideal class group", and "class number theorem". Four
GitHub repository-metadata queries returned complete zero-result responses.
Unauthenticated GitHub code search returned HTTP 401, and grep.app returned
HTTP 429. Therefore no additional credible external candidate was established,
but the audit makes no exhaustive global negative claim.

## Classification boundary

The exact pinned mathlib candidate and local audit wrapper support a proposed
`M0-W` classification for the root. This phase does not accept that status:
the obligation registry, proof node, full transitive provenance/trust checks,
hermetic validation, independent review, and master acceptance remain later
gates. Human-source fidelity remains `H1`, readability remains `R4`, and both
`audit_complete` and `theorem_complete` remain false.

## Validation record

Base revision: `1ec654c416270f261b365f46f5f2409b65d3f839`.

| Command | Exit/result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0; 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0415` | 0; rank 70, planned, L0, theorem complete false |
| `python3 Stage1_Instances/THM-M-0415/check_anchor_audit.py` | 0; three candidates classified and pinned source/blob/license hashes verified |
| `python3 -m json.tool Stage1_Instances/THM-M-0415/anchor-audit.json` | 0; valid JSON |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0415/AnchorAudit.lean` | 0; candidate route and exact wrapper elaborated; axiom sets printed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0415/Statement.lean` | 0; frozen canonical statement still elaborated |
| `git diff --check -- Stage1_Instances/THM-M-0415` | 0; no whitespace errors |

The first combined validation invocation was launched from `Formalizations/Lean`
while its two Python paths were still repository-root-relative. Those two
Python subcommands exited 2 and 1 (`file not found`); the two following Lean
subcommands in that same invocation both exited 0. The Python checks were then
rerun from the repository root as recorded above and exited 0. This was a
working-directory error, not a dependency or theorem failure.

Known failures are the bounded public-code-search limitations and every
downstream theorem gate listed above. They do not invalidate this self-tested
candidate audit and do prevent any theorem-completion claim.
