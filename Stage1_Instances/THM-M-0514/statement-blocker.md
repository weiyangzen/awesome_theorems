# Exact-statement gate: blocked

Item: `S56-M-0514-STATEMENT`

Theorem: `THM-M-0514`

Base revision: `e9252b1cfdc99a094324c8a10d260769df2eca15`

## Decision

The exact Lean 4 target cannot be truthfully selected from the authoritative repository material.
Its only mathematical wording is `虚二次域的类域论` ("class field theory of imaginary quadratic
fields"). This is the name of a theory, not a proposition with ordered binders, hypotheses, and a
conclusion. The accepted intake dependency accordingly leaves both the canonical claim and the
formal target null.

The missing choices are constitutive. A statement must select, for example, a first-main-theorem
generation result, a ring-class-field variant, a second-main-theorem reciprocity result, or a CM
elliptic-curve classification result. It must also fix the quadratic field or order, conductor,
discriminant and embedding conventions, modular function, normalization, exceptional unit cases,
class field, and exact conclusion. These choices give inequivalent propositions. Choosing one from
general mathematical familiarity would substitute a theorem not identified by the source.

The first failed gate is exact source-statement identification. Therefore this phase cannot freeze
a canonical declaration or expression hash, certify minimal imports, check alternate encodings, or
perform meaningful removed-hypothesis, changed-domain, binder-scope, and boundary mutations.
Machine debt remains `M4`; no statement or theorem-completion credit is claimed.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated under the pinned environment. It confirms nearby
APIs for CM number fields, maximal real subfields, class numbers, class groups, and Weierstrass
curves. A bounded exact-phrase search of pinned mathlib found no declaration mentioning complex
multiplication, a Hilbert or ring class field, singular moduli, or an Artin map. This is only a
surface assessment, not the later anchor audit. In particular, `NumberField.IsCMField` does not
express the missing class-field theorem, so neither the probe nor its imports are a canonical
statement or a minimal-import certificate.

The environment is Lean 4.29.0 (commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`), Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The `lean-toolchain` and `lake-manifest.json`
SHA-256 values are `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` and
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`. The inherited canonical
`.lake` link was used read-only; no update, build, clone, or fetch was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0514` | 0 | rank 888; planned; legacy artifacts unaccepted; theorem incomplete |
| scoped repository search for `THM-M-0514`, `复乘理论`, and `虚二次域的类域论` outside generated authorities and this dossier | 0 | only the subject-level metadata and explicitly open Stage0 fields were found; no proposition was found |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C $(readlink -f Formalizations/Lean/.lake)/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision recorded above |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0514/IntakeProbe.lean` | 0 | all five nearby substrate API checks elaborated and printed their types |
| exact-phrase `rg` search of pinned mathlib for complex multiplication and the required class-field vocabulary | 1 | expected no-match result; no target declaration found |
| `python3 -m json.tool Stage1_Instances/THM-M-0514/statement-blocker.json` | 0 | structured blocker is valid JSON |
| scoped forbidden-declaration scan of Lean artifacts | 0 | the guard passed because the search returned the expected no-match result |
| `git diff --check -- Stage1_Instances/THM-M-0514` | 0 | no whitespace errors |

## Retry condition

An accountable source reviewer must pin and approve an immutable edition and exact theorem/page,
including assumptions and errata. The statement phase can then freeze every mathematical object,
normalization, binder, hypothesis, conclusion, and boundary case; elaborate the source-faithful
target with minimized imports; serialize its expression; check transports; and perform the required
mutations.

Because the assigned statement phase is not genuinely self-tested to completion, no
`.stage1-worker-selftest.json` is emitted.
