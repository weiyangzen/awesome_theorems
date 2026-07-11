# THM-M-0119 anchor-audit validation

Item: `S56-M-0119-ANCHOR_AUDIT`  
Date: 2026-07-12  
Base revision: `b11e1f5a1a404420eee7320a845fdb9df48bec0c`

## Decision

The exact repo-local target remains a proposition definition over explicit
interfaces, without a theorem or proof body. The legacy `S1_M_038.lean` module
is a broader parameterized statement shape and a tautological premise wrapper;
it is not the frozen klt-pair target and receives no inherited proof credit.

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`
provides schemes, proper morphisms, sheaves of modules, a general sheaf
cohomology object, and module-theoretic local cohomology. The ten passing Lean
probes record these genuine nearby APIs. They do not supply scheme Q-divisors,
klt pairs, `K_X + Delta`, nef-and-big positivity, the divisorial sheaf
`O_X(D)`, or Kawamata--Viehweg vanishing. The title in mathlib's `1000.yaml` is
a project-tracking entry, not a declaration.

A complete search of the locally materialized `flt-regular` direct dependency
found no relevant source. Bounded Sourcegraph and GitHub repository searches
returned no candidate. GitHub code search was rate-limited and requires an
authenticated lane, so this is recorded as a limitation rather than converted
into proof-absence evidence. There is consequently no exact external proof to
pin/import/check and no repo-local integration debt to discharge in this node.

The root stays `M3`: an elaborated statement interface plus supporting anchors,
with no root closure. This record is a self-tested candidate inventory pending
master acceptance, not human-source audit completion, theorem proof, global
absence evidence, or theorem completion.

## Commands and results

All commands ran inside this worker clone. Lean used the existing pinned
`.lake` artifacts; no update, fetch, clone, or build was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-0119` | 0 | rank 38; planned; rework required; theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | exact manifest pin `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i --glob '*.lean' 'kawamata\|viehweg\|log.?canonical\|\\bklt\\b\|kodaira.?vanish' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | expected no-match status in pinned mathlib Lean source |
| `rg -n -i --glob '*.lean' --glob '*.md' --glob '*.yaml' 'kawamata\|viehweg\|log.?canonical\|\\bklt\\b\|kodaira.?vanish' Formalizations/Lean/.lake/packages/flt-regular` | 1 | expected no-match status in the complete pinned dependency source |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0119/AnchorAudit.lean` | 0 | ten nearby pinned declarations elaborated and printed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0119/Statement.lean` | 0 | frozen exact target and mutations re-elaborated |
| `python3 Stage1_Instances/THM-M-0119/check_anchor_audit.py` | 0 | pins, statement boundary, bounded negative source check, and fail-closed verdict agreed |
| `curl ... sourcegraph.com/.api/search/stream ...` | 0 | `matchCount=0`; response SHA-256 `4e974db5eaf8ba56c397de6126ab247ee582d71dde531a769a33492a581a3c21` |
| `curl ... api.github.com/search/repositories ...` | 0 | `total_count=0`, complete response; SHA-256 `08c082fdf7ca87ba911a2aabb0f0cf2d3e482a6feeaac9713e4578c20b2600b2` |
| `curl ... api.github.com/search/code ...` | 0 | HTTP 403 response captured; rate-limited blocked lane, not negative evidence |
| `python3 -m json.tool Stage1_Instances/THM-M-0119/anchor-audit.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0119 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Reopen condition

Reopen integration when a concrete Lean 4 candidate supplies a repository URL,
immutable revision, pinned toolchain and dependencies, exact module and
declaration, checked transport to the frozen root, terminal proof-body and
placeholder provenance, trust and license audits, and a successful repo-local
elaboration check.
