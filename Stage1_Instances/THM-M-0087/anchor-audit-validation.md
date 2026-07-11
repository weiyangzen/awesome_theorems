# Anchor-audit validation record

Item: `S56-M-0087-ANCHOR_AUDIT`  
Base revision: `c8855fd0eb87514348ace46003c6075c576fbfb6`

## Result

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`
contains the full, faithful, tensor-Hom adjunction, and finite-limit-preservation
anchors needed by the frozen `Statement`. `AnchorAudit.exactMathlibCandidate`
composes those declarations against a verbatim dossier-local copy of that type.
The upstream proof bodies are
source-visible in `GabrielPopescu.lean`; the module has no placeholder, axiom
declaration, or unsafe token, and Lean reports only `propext`,
`Classical.choice`, and `Quot.sound` in the wrapper's axiom closure.

A bounded external search found only the same mathlib theorem family, indexed at
later immutable commit `12b4b4adf73c3bf0917409bb4b9dd4c8b96f4e8f`.
GitHub repository search returned no separate project, while GitHub code search
was authentication-blocked and is not reported as a negative result. The local
historical wrapper is discovery-only and receives no rev-5.6 credit.

Thus the frozen embedding/exact-left-adjoint target has an exact pinned
`M0-P_candidate`. This is candidate audit evidence, not accepted proof-phase or
theorem-completion evidence. In particular, it does not construct the classical
named Serre quotient or its equivalence.

## Commands and results

Commands ran on 2026-07-12 inside this worker clone. Lean used only the existing
pinned `.lake` artifacts; no dependency update, fetch, clone, or build occurred.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard consistent; 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0087` | 0 | Rank 133; planned; legacy artifacts unaccepted; theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0087/AnchorAudit.lean` | 0 | Six pinned anchors and the exact candidate elaborated; axiom closure printed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0087/Statement.lean` | 0 | Frozen target re-elaborated |
| `python3 Stage1_Instances/THM-M-0087/check_anchor_audit.py` | 0 | Audit boundary, six probes, manifest pin, and installed mathlib HEAD agreed |
| `rg -n '\\b(sorry|admit|axiom|unsafe)\\b' .../GabrielPopescu.lean` | 1 | Expected no-match exit: no forbidden source token |
| `curl ... sourcegraph ... 'GabrielPopescu lang:Lean'` | 0 | Seven matches, all mathlib4; response SHA-256 `711e18551fbde039057bbfa1f18ddfcdcf8410006f7a3f52bb2cb5859ace880a` |
| `curl ... api.github.com/search/repositories?q=\"Gabriel-Popescu\"+lean` | 0 | Zero complete repository results; response SHA-256 `08c082fdf7ca87ba911a2aabb0f0cf2d3e482a6feeaac9713e4578c20b2600b2` |
| `curl ... api.github.com/search/code?q=GabrielPopescu+language:Lean` | 0 | HTTP 401 blocker captured; response SHA-256 `b7dbd173f33b19650f61b1c528737e2037cf768d90076fdfce5d32541765e29e` |
| `python3 -m json.tool Stage1_Instances/THM-M-0087/anchor-audit.json >/dev/null` | 0 | Structured audit is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0087 .stage1-worker-selftest.json` | 0 | No whitespace errors |

## Open gate

The obligation-tree phase must model the imported proof bodies and exact
composition before proof acceptance. Trust, source, readability, hermetic
replay, and independent verification remain open. Any future explicit
Serre-quotient equivalence also needs a separately checked statement transport.
