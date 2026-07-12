# THM-M-0773 anchor-audit validation

Item: `S56-M-0773-ANCHOR_AUDIT`  
Base revision: `9864b47f2fbf53d0b642c54f12039877d4635056`  
Validation date: `2026-07-12` (`Asia/Shanghai`)

## Result

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`
contains `Order.IsOfFiniteCharacter.exists_maximal` in
`Mathlib.Order.TeichmullerTukey`. Its pointed conclusion is stronger than the
frozen target. The checked `target_of_mathlib` wrapper chooses a seed from the
required nonempty family and forgets only the returned subset witness.

Lean elaborated the exact expanded target and reported `propext`,
`Classical.choice`, and `Quot.sound` for both the upstream declaration and the
wrapper. The source body applies the pinned Zorn implementation; scoped source
scans found no placeholder, bodyless axiom declaration, or unsafe marker.
This is an `M0-W` / `E1` exact completion anchor, not a new local terminal body.

Repo-local and pinned-source searches found no competing body. Unauthenticated
GitHub code search returned `401`, and grep.app returned a `429` security
checkpoint, so this audit does not claim exhaustive absence of other public
Lean 4 formalizations. That access limitation does not weaken the locally
checked exact mathlib candidate.

## Commands and exact outcomes

| command | exit | outcome |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 slots, and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks and targets passed |
| `python3 scripts/stage1_target.py show THM-M-0773` | 0 | rank 781; planned; L0/rework-required; theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package tree clean |
| scoped `rg` searches for canonical names and aliases | 0/1 | exact candidate located in pinned mathlib; no separate repo-local proof body found (exit 1 is the expected no-match result for the exclusion query) |
| GitHub code-search API query for `IsOfFiniteCharacter` | 0 transport / HTTP 401 | authentication required; response hash recorded in `anchor-audit.json` |
| grep.app queries for `IsOfFiniteCharacter.exists_maximal` and `Teichmuller-Tukey` | 0 transport / HTTP 429 | Vercel security checkpoint; response hashes recorded in `anchor-audit.json` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0773/AnchorAudit.lean` | 0 | exact wrapper elaborated; upstream and wrapper axiom reports both equal `[propext, Classical.choice, Quot.sound]` |
| `python3 Stage1_Instances/THM-M-0773/check_anchor_audit.py` | 0 | immutable revision/tree, clean package, file hashes, body markers, and fail-closed status assertions passed |
| `python3 -m json.tool Stage1_Instances/THM-M-0773/anchor-audit.json` | 0 | structured audit ledger is valid JSON |
| placeholder scan over owned Lean files | 1 | expected no-match exit; no `sorry`, `admit`, or axiom declaration found |
| `git diff --check -- Stage1_Instances/THM-M-0773 .stage1-worker-selftest.json` | 0 | no whitespace errors |

No `lake update`, build, clone, fetch, or `.lake` mutation was performed. The
anchor-audit phase is self-tested pending master acceptance. Obligation-tree,
full trust/provenance, human-source, readability, hermetic, and independent
release gates remain downstream; `theorem_complete` remains false.
