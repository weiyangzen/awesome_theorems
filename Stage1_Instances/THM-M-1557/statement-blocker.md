# THM-M-1557 statement-phase blocker

Item: `S56-M-1557-STATEMENT`  
Base revision: `509bacaa61c3669c81276814a33094f8f7280f78`

## Verdict

The exact Lean 4 target cannot yet be truthfully frozen or elaborated. The intake deliberately
freezes only a claim family: compatibility of a source-selected Zakharov-Shabat auxiliary system
is related to a source-normalized nonlinear Schrodinger equation. It leaves open the actual spatial
and temporal matrices, focusing or defocusing reduction, signs and scaling, spectral-parameter
domain and scope, independent-variable domains, differentiability assumptions, boundary or decay
conditions, and whether the source establishes one implication or an equivalence. Each choice
changes the proposition, its ordered binders, or its boundary cases.

The repository source record supplies only `NLS方程的Lax对` ("a Lax pair for the NLS
equation"). The intake names the 1972 Zakharov-Shabat paper as a candidate, but no immutable copy,
exact page/equation range, reviewed transcription, convention crosswalk, or errata decision is an
accepted input. Selecting equations from memory or from a later normalization would invent the
missing mathematics and could silently substitute a gauge- or scaling-related theorem.

The repo-local module `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_210.lean` elaborates in the
pinned environment, but it is negative boundary evidence rather than the target. It belongs to
`THM-M-1551`, models arbitrary Lie-algebra elements and linear evolution maps, has no concrete
Zakharov-Shabat matrices, spectral parameter, complex potential, conjugacy reduction, derivatives,
or NLS equation, and proves only that an abstract rearranged compatibility equality implies its
definition of zero curvature. Wrapping that declaration would broaden and substitute the assigned
source-specific theorem.

The first failed gate is rev-5.6 section 5 exact source-statement identification, before canonical
Lean elaboration. Consequently there is no legitimate canonical declaration, normalized expression
fingerprint, minimal exact-target import list, checked alternate transport, or four-class mutation
suite. The intake machine grade remains `M4`; statement acceptance, proof credit, audit completion,
and theorem completion remain false.

## Environment fingerprint

- Lean toolchain file: `leanprover/lean4:v4.29.0`.
- Lean executable: version 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Mathlib revision present in the pinned shared artifacts:
  `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- SHA-256 of `lean-toolchain`: `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- SHA-256 of `lake-manifest.json`: `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- SHA-256 of the legacy boundary module: `bb147a13f2a6cad568c84670b26cebbe19444f0278443152d19f08e3e1586a8b`.

## Commands and results

All commands ran in this worker clone. Lean reused the existing canonical `.lake` artifacts through
the worker link. No Lake update/build, dependency clone/fetch, or `.lake` mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard passed: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | Manifest passed: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1557` | 0 | Rank 569, planned, `hard_mathlib_anchor_and_wrapper`, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_210.lean` | 0 | Legacy abstract zero-curvature boundary elaborated; it does not elaborate the exact Zakharov-Shabat/NLS target |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_210.lean` | 0 | Hashes match the environment fingerprint above |
| `rg -n -i 'Zakharov\|Shabat\|NLS.*Lax\|nonlinear Schr.dinger.*Lax' . --glob '!Formalizations/Lean/.lake/**' --glob '!Stage1_Instances/THM-M-1557/**'` | 0 | Found terse catalogue metadata, neighboring target notes, and the abstract legacy boundary; no reviewed exact source transcription for this UID |

## Retry condition

Provide an immutable, independently reviewed primary-source edition with an exact page and equation
range, all referenced definitions and assumptions, and an errata/translation decision. A later
detailed source may be pinned only to clarify notation, with every difference crosswalked to the
selected primary equations. The next statement run can then freeze the matrices and NLS
normalization, encode all ordered binders and boundary cases, determine minimal imports, serialize
the elaborated expression, compile any normalization transports, and run the required mutations.

No `.stage1-worker-selftest.json` is emitted because this assigned phase is blocked rather than
genuinely self-tested.
