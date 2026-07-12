# Anchor-audit validation record

Item: `S56-M-1061-ANCHOR_AUDIT`  
Base revision: `63dd69def57f86f9ff668f657fbd2bbef39b8068`

## Result

The exact local artifact is the proposition definition
`Stage1Instances.THM_M_1061.VaradhanIntegralLemmaTarget`, not a proof body.
Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95`
provides the topology, measure, extended-logarithm, liminf, and limsup substrate
checked by `AnchorAudit.lean`; a source-wide name search found no LDP or
Varadhan declaration.

The bounded external search found two relevant immutable source trees.
`facebookresearch/atlas-lean@34ffed396f376454c1a9b297f3fd74c5c801fb50`
uses the same Lean and mathlib pins and defines rate-function and LDP interfaces,
but its complete `LargeDeviations.lean` source contains no terminal integral
lemma. `the-omega-institute/automath@f76f46f07a1a48d5c12a20c2f8d366bb9df9330d`
contains a theorem with a hypothesis called `hVaradhan`, but inspection shows
that it is only an unrelated real-function rewrite. It is rejected rather than
substituted. GitHub code search was unavailable without authentication.

The root classification is therefore `M4`: no proof declaration exists in the
audited candidates to integrate. This is anchor-audit closure only, not theorem
closure or a claim that no external Lean proof exists anywhere.

## Commands and results

Commands ran inside this worker clone on 2026-07-12. No Lake dependency was
updated, fetched, cloned, or built.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1061/AnchorAudit.lean` | 0 | seven pinned supporting declarations elaborated |
| `python3 Stage1_Instances/THM-M-1061/check_anchor_audit.py` | 0 | four-candidate M4 boundary, probes, manifest pin, and installed mathlib HEAD agreed |
| `rg -n -i --glob '*.lean' 'Varadhan\|Laplace.?principle\|large.?deviation\|SatisfiesLDP\|IsGoodRateFunction' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | expected no-match status in pinned mathlib source |
| Sourcegraph API query recorded in `anchor-audit.json` | 0 | 18 matches in two repositories; response SHA-256 `541124ed...602b` |
| GitHub content API inspection of Atlas `LargeDeviations.lean` | 0 | immutable source SHA-256 `8074d9ec...f036`; definitions only |
| GitHub content API inspection of Automath `OracleSuccessVariationalLaplace.lean` | 0 | immutable source SHA-256 `796a3470...316d`; unrelated explicit rewrite proof |
| GitHub repository search `Varadhan Lean` | 0 | one metadata hit; response SHA-256 `7921cc87...5968` |
| GitHub code search `Varadhan language:Lean` | 0 | HTTP 401 response recorded; SHA-256 `b7dbd173...e29e` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-1061` | 0 | rank 504, planned, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1061/anchor-audit.json` | 0 | structured artifact parsed |
| `git diff --check -- Stage1_Instances/THM-M-1061 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Open machine gate

An exact proof still needs lower-bound localization, the compact-sublevel
finite-cover upper bound, bounded tail control, and extended-real limit and
supremum transports. Any later external candidate must be pinned and checked
for exact type, proof-body provenance, placeholders, axioms, unsafe/oracle
boundaries, license, and repo-local elaboration before it receives proof credit.

