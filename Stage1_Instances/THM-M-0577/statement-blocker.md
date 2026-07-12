# Exact-statement gate: blocked

Item: `S56-M-0577-STATEMENT`  
Theorem: `THM-M-0577`  
Base revision: `9ca62658cb1c22f4da89356b73946aeea3313521`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the authoritative repository record.
The complete theorem-specific wording is the title `伍德沃德定理` ("Woodward theorem"), the
non-identifying attribution `众多数学家` ("many mathematicians"), and the description
`配边理论中的结果` ("a result in cobordism theory"). No author, publication, theorem/page,
definition, hypothesis, or conclusion is supplied. The intake dependency therefore correctly
freezes `[H4, M4, R4]` and leaves theorem identity open.

This metadata does not determine a proposition. It leaves unresolved at least the identity of
Woodward, the relevant cobordism theory and category, the objects and equivalence relation, the
dimension and finiteness or boundary conditions, any orientation or tangential structure, the
ordered quantifiers and hypotheses, and whether the conclusion is an existence, classification,
invariance, computation, or correspondence result. Different choices are inequivalent targets.
Selecting Thom, Pontryagin--Thom, h-cobordism, s-cobordism, the cobordism hypothesis, or any result
merely containing the surname Woodward would broaden or substitute the theorem rather than
elaborate the repository claim.

A scoped repository search found no additional source locator or formal statement. Exact-phrase
discovery checks of Crossref, arXiv, and OpenAlex also did not identify a matching Woodward theorem
in cobordism theory. These index checks are negative discovery evidence, not an exhaustive source
audit and not proof that no such theorem exists. The pinned mathlib source contains no occurrence
of `Woodward` or `cobordism`; more importantly, a library candidate could not resolve the absent
canonical human claim by itself.

Consequently the phase fails at canonical claim identity, before a Lean expression or minimal
import can be chosen. There is no applicable `lake env lean <file>` elaboration check: compiling an
invented proposition, a convenient special case, or an abstract structure that assumes its own
conclusion would be fake statement evidence. No canonical declaration, expression fingerprint,
checked transport, mutation-test acceptance, statement completion, audit completion, or theorem
completion is claimed. No `.stage1-worker-selftest.json` is emitted.

## Pinned environment and scoped evidence

Commands were run inside this worker clone on 2026-07-12 (Asia/Shanghai). Existing `.lake`
artifacts were read only; no update, build, clone, or fetch was performed.

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0577` | 0 | Rank 689, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C "$(readlink -f Formalizations/Lean/.lake/packages/mathlib)" rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for `伍德沃德`, `Woodward`, and `配边理论中的结果` | 0 | Found only the underspecified inventory records and this target's intake artifacts; no proposition or source locator |
| `rg -l -i 'woodward\|cobordism' Formalizations/Lean/.lake/packages/mathlib/Mathlib \| wc -l` | 0 | `0` matching files in pinned mathlib source |
| Crossref API query for exact phrase `"Woodward theorem"` plus `cobordism` | 0 | No Woodward result among the 10 returned records; returned records were unrelated cobordism works |
| arXiv API query `all:"Woodward theorem"` | 0 | `totalResults=0` |
| OpenAlex API search for exact phrase `"Woodward theorem"` plus `cobordism` | 0 | Zero results |

## Retry condition

An accountable source review must identify the intended theorem in a stable primary source and
record the full author, publication, theorem/page, exact wording, definitions, assumptions,
conclusion, corrections, and errata, together with evidence that it is the result meant by this
repository label. A later statement run can then crosswalk that claim row by row, encode and
fingerprint its exact Lean expression, minimize pinned imports, compile credited transports, and
run the required removed-hypothesis, changed-domain, binder-scope, and boundary-case mutations.
