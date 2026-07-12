# THM-M-0338 anchor-audit validation

Item: `S56-M-0338-ANCHOR_AUDIT`  
Base revision: `bd0d227173ac95971603f633607751754850337e`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

The exact repo-local artifact is the elaborated proposition
`Stage1.THM_M_0338.KadisonSingerStatement`, not a theorem body. Pinned mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies positive-linear-map, GNS,
C-star-subalgebra, continuous-linear-map, and Hilbert-basis infrastructure. The eight retained
APIs elaborate in `AnchorAudit.lean`, but neither the audited modules nor the full pinned mathlib
source name/alias scan contains a terminal Kadison-Singer declaration.

No external Lean 4 proof candidate was located by the bounded public searches. Sourcegraph and
GitHub repository search returned zero results. Unauthenticated GitHub code search returned HTTP
401, so that lane is recorded as blocked rather than negative. The complete 1204-entry Git tree of
`google-deepmind/formal-conjectures@b2e608fc52d765510915a244bb69b1a2741acc3c` contains no
Kadison-Singer, paving, or Weaver path. Public response hashes are discovery evidence, while only
the mathlib and Formal Conjectures inspections are bound to immutable commits.

The root therefore remains `M4` with `formalization_debt`: the mathematics is known, but this audit
found no Lean 4 proof body to integrate. This completes the bounded anchor-audit phase only. It is
not a claim of global absence and provides no H0, proof, M0, audit-completion, or theorem-completion
credit.

## Commands and exact outcomes

All Lean commands used the existing pinned Lake environment. No `lake update`, build, dependency
clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Outcome |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0338/AnchorAudit.lean` | 0 | Eight pinned supporting declarations elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0338/Statement.lean` | 0 | Exact canonical statement re-elaborated and printed |
| `python3 Stage1_Instances/THM-M-0338/check_anchor_audit.py` | 0 | Exact statement-only boundary, eight probes, mathlib pin, and bounded pinned-source scan agreed; root `M4` |
| `rg -n -i 'kadison.?singer\|anderson.?paving\|weaver.?conjecture\|interlacing families\|mixed characteristic polynomial\|paving conjecture' Formalizations/Lean/.lake/packages --glob '*.lean'` | 1 | Expected no-match exit; no named candidate in pinned dependency source |
| Sourcegraph stream query over Kadison-Singer, KadisonSinger, paving, and Weaver Lean aliases | 0 | `matchCount=0`; response SHA-256 `13845a5e...fb650` |
| GitHub REST repository search for `"Kadison-Singer" lean` | 0 | `total_count=0`, complete response; SHA-256 `08c082fd...600b2` |
| GitHub REST code search for `"Kadison-Singer" language:Lean` | 0 | Captured HTTP 401 authentication blocker; response SHA-256 `b7dbd173...5e29e` |
| GitHub immutable recursive tree query for `google-deepmind/formal-conjectures@b2e608fc...3c` | 0 | `truncated=false`, 1204 entries, no relevant path; response SHA-256 `76fa3f96...efc61` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target projection valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks; all uniform L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0338` | 0 | rank 831, planned, historical artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0338/anchor-audit.json` | 0 | Structured audit is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0338 .stage1-worker-selftest.json` | 0 | No whitespace errors |

## Open integration gate

Reopen integration only after locating a canonical remote, immutable revision, Lean toolchain and
dependency graph, module, declaration, exact normalized type or checked transport, and license.
The terminal proof body must then pass placeholder, axiom, unsafe/oracle, provenance, and local
wrapper checks before any `M0` credit is possible.
