# THM-M-1271 anchor-audit validation

Item: `S56-M-1271-ANCHOR_AUDIT`  
Audit date: `2026-07-12` (`Asia/Shanghai`)  
Base revision: `67392d9b9aeb94afc0b864b86ce8cdd8ace153ad`

## Result

The canonical proposition elaborates, but no exact proof-bearing anchor was found. Pinned mathlib
provides Frechet calculus, continuous paths, extrema on compact sets, and convergent-subsequence
machinery. These are genuine but nonterminal dependencies. The repository's legacy `S1_M_164`
module also checks several useful conditional lemmas, while explicitly leaving the deformation
argument and terminal wrapper unavailable; its statement and Palais-Smale encoding differ from the
canonical target, so it cannot receive root proof credit.

An alias search across every pinned Lake dependency found no mountain-pass theorem. The immutable,
non-truncated tree for `google-deepmind/formal-conjectures@b2e608fc52d765510915a244bb69b1a2741acc3c`
contained no matching path. Five GitHub repository-index queries returned zero results with
`incomplete_results=false`. GitHub code search was unavailable without authentication, and grep.app
returned HTTP 503. The public search is therefore bounded, not exhaustive.

The root remains `M3`: exact statement elaboration without a root proof body. This completes only
the assigned candidate audit for master review. It does not prove, validate, release, or complete
the theorem, and accepted receipts remain empty.

## Commands and results

Commands ran from the repository root unless a working directory is shown.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks passed |
| `python3 scripts/stage1_target.py show THM-M-1271` | 0 | rank 164, planned, theorem incomplete |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg` alias search over all pinned dependency source trees | 1 | no candidate match; exit 1 is ripgrep's expected no-match result |
| five GitHub repository API queries recorded in `anchor-audit.json` | 0 | counts `[0,0,0,0,0]`; every response reported `incomplete_results=false` |
| immutable GitHub recursive-tree query for Formal Conjectures | 0 | exact SHA returned, `truncated=false`, no matching path |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1271/Statement.lean` | 0 | exact target, expansion transport, and mutations elaborated |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_164.lean` | 0 | legacy partial scaffold and its explicit terminal gates elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1271/AnchorAudit.lean` | 0 | nine pinned mathlib anchor probes elaborated |
| `python3 Stage1_Instances/THM-M-1271/check_anchor_audit.py` | 0 | candidate ledger, pins, source witnesses, and open-root boundary passed |
| `python3 -m json.tool Stage1_Instances/THM-M-1271/anchor-audit.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1271 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The clone's pre-existing untracked `Formalizations/Lean/.lake` link reuses canonical pinned
artifacts. No Lake update, build, dependency clone/fetch, or `.lake` mutation occurred.
