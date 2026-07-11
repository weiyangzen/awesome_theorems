# THM-M-0135 statement-phase blocker

Item: `S56-M-0135-STATEMENT`  
Base revision: `5d9a23f1666b0016d713463eef678ff50014bd37`

## Verdict

The exact Lean 4 target cannot yet be truthfully frozen or elaborated. The repository source record
identifies only "Macdonald identities" and describes them as identities on affine root systems.
Macdonald's 1972 paper is a family of identities, but the record supplies no affine type, numbered
formula, page, normalization, or specialization. Selecting one formula would therefore substitute
an unstated theorem rather than elaborate the exact target assigned by the manifest.

The missing selection controls mathematically material parts of the proposition: the affine root
datum and positive-root convention, real and imaginary root multiplicities, Weyl-vector shift and
sign, coefficient ring and completion, interpretation of the infinite product and sum, and any
Dedekind-eta specialization. It also prevents certification of a minimal import set. The intake's
primary bibliographic candidate, I. G. Macdonald, *Affine root systems and Dedekind's eta-function*,
Inventiones Mathematicae 15 (1972), 91-143, DOI `10.1007/BF01418931`, is not itself a statement
pinpoint.

The historical module `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_051.lean` elaborates under
the pinned environment, but this is negative boundary evidence only. Its `AffineMacdonaldData`
stores `denominatorProduct` and `alternatingSum` as arbitrary finite-support expressions, and
`StatementShape D` merely equates those fields. The module does not construct the source-defined
sides, model the required completed infinite expressions, or assert the universal shape. It is not
an exact formalization of any selected Macdonald identity and receives no statement credit.

First failed gate: exact source-statement identification. The statement node remains open with no
canonical declaration, elaborated-expression hash, checked transport, or theorem-completion claim.
Retry only after an immutable primary-source edition is available and one numbered identity is
selected with exact page/formula coordinates, conventions, assumptions, and errata audit. The
selected formula can then determine the native Lean encoding and minimal imports.

## Environment and validation

All commands ran in this worker clone on 2026-07-12 (Asia/Shanghai). The Lean checks used the
already materialized pinned Lake environment. No dependency update, fetch, clone, or build was run.

- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256: `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256: `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Historical module SHA-256: `c2992c827df8bfea17979690c62f72dc0528826aadddcde7e1ecffacee0ec710`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | Passed: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0135` | 0 | Rank 51; planned; legacy artifacts unaccepted; theorem incomplete |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_051.lean` | 0 | Historical statement-shape and ingredient module elaborated; not exact-target evidence |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Reported the Lean version and commit above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json AwesomeTheorems/Stage1/S1_M_051.lean` | 0 | Reported the three hashes above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Reported the pinned mathlib revision above |

No `.stage1-worker-selftest.json` is emitted because the assigned exact-statement phase is blocked,
not genuinely self-tested.
