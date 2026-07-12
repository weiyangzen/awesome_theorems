# Statement validation

Base revision: `3c49a04f350afa3376ed84e511f0c4e1e03dbe06`.

The worktree already contained the untracked canonical `.lake` link supplied by
the worker automation clone. It was reused read-only and makes this nonrelease
evidence. No dependency update, fetch, clone, or build was run.

Commands and results:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: ok; 1546 uniform-L0 Lean 4 targets
python3 scripts/stage1_target.py check
  exit 0: ok; 1546 unique targets, ranks 1..1546
python3 scripts/stage1_target.py show THM-M-0993
  exit 0: rank 273, lifecycle planned, theorem_complete false
cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0993/Statement.lean
  exit 0: target, checked transport, four mutations, and empty-family boundary elaborated;
  printed the explicit canonical expression
python3 Stage1_Instances/THM-M-0993/check_statement.py
  exit 0: expression sha256 ecae1a493dd8be1ab742029ee934c64ecd0595761326dc1efadfa5fb2e590669;
  all four mutations differed; mathlib revision 8a178386ffc0f5fef0b77738bb5449d50efeea95
cd Formalizations/Lean && lake env lean --version
  exit 0: Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740
python3 -m json.tool Stage1_Instances/THM-M-0993/statement.json
  exit 0
git diff --check -- Stage1_Instances/THM-M-0993
  exit 0
```

This validates the statement phase only. The declaration is proposition-valued
and has no proof body. Source audit, proof, trust closure, release validation,
and theorem completion remain open.
