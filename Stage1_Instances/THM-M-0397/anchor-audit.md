# THM-M-0397 Anchor Audit

## Verdict

The bounded rev-5.6 audit found one useful pinned composition anchor but no
terminal Baker-method application theorem. At mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `Finset.mem_filter` supplies the
last exact-enumeration step after the frozen `Application.reduce_solution` and
`Application.heightBall_spec` fields have supplied boundedness and enumeration.
`AnchorAudit.lean` checks that composition shape. Mathlib's complex exponential
and algebraicity APIs supply only the logarithmic-form object model.

No exact external Lean 4 candidate was identified. The canonical root remains
`M3`, with no proof credit, accepted receipt, or theorem-completion claim.

## Immutable Local Sources

The dependency authority is `Formalizations/Lean/lake-manifest.json`. The
canonical pre-existing `.lake` link exposes mathlib at the commit above and ten
other dependencies at their manifest commits. Searches across all their Lean
sources used this case-insensitive inventory:

```text
baker.?method|effective.*diophantine|diophantine.*effective|linear.?forms?.?in.?logarithms?|thue.?mahler|s.?unit equation
```

Both the mathlib and non-mathlib searches returned ripgrep's no-match exit `1`.
This rules out those spellings in those immutable trees, not an unnamed result.
The local legacy `S1_M_010.lean` is an abstract interface and explicitly denies
a kernel-checked Baker-method proof; it is discovery input with zero proof
credit.

## External Discovery Boundary

On 2026-07-12, GitHub repository-search queries for quoted `Baker method`,
`linear forms in logarithms`, `effective Diophantine`, and `Thue equation`, each
combined with Lean, returned zero repositories with `incomplete_results=false`.
This mutable metadata search nominated no repository whose revision, module,
declaration, toolchain, body, axioms, placeholders, or license could be audited.
It is not exhaustive public code search and does not establish global absence.
No dependency was fetched, cloned, or modified.

## Candidate Disposition

| Candidate | Exact root | Provenance and disposition |
|---|---|---|
| `Finset.mem_filter` in pinned mathlib | No | Verified final composition API; already pinned; candidate for the later proof node |
| `Complex.exp` and `IsAlgebraic` in pinned mathlib | No | Statement substrate only; no Baker lower bound or reduction body |
| Legacy `S1_M_010.lean` at base revision | No | Abstract mismatched interface; explicitly no terminal proof; zero credit |

An external candidate becomes actionable only with an immutable revision,
module and declaration, exact type or checked transport, compatible toolchain
lock, terminal body provenance, license, and placeholder/axiom/unsafe audit.

## Commands And Results

Commands ran from the repository root unless a different cwd is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks; all targets L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0397` | 0 | Rank 10, planned, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Exact pinned mathlib commit recorded above |
| pinned mathlib inventory `rg` | 1 | Expected no-match result |
| inventory `rg` over all ten other pinned packages | 1 | Expected no-match result |
| four GitHub repository API queries | 0 | Each total count zero; each complete as repository metadata search |
| `lake env lean ../../Stage1_Instances/THM-M-0397/Statement.lean` (`Formalizations/Lean`) | 0 | Canonical target elaborated |
| `lake env lean ../../Stage1_Instances/THM-M-0397/AnchorAudit.lean` (`Formalizations/Lean`) | 0 | Pinned declarations and filter composition lemma elaborated |
| `python3 Stage1_Instances/THM-M-0397/check_anchor_audit.py` | 0 | Statement hash, mathlib pin, source witness, and non-closing ledger verified |
| `python3 -m json.tool Stage1_Instances/THM-M-0397/anchor-audit.json` | 0 | Structured artifact parsed |
| forbidden-token scan of `AnchorAudit.lean` | 1 | Expected no-match result |
| `git diff --check -- Stage1_Instances/THM-M-0397 .stage1-worker-selftest.json` | 0 | No whitespace errors |

The phase inventory is self-tested at its stated cutoff. Whole-theorem audit,
proof, validation, release, and master acceptance remain open.
