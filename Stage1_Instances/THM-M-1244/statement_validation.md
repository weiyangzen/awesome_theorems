# Statement validation

Base revision: `7619d195bd4454d4084e74977cf56d86c396ab3a`.

The worktree already contained the untracked canonical `.lake` link supplied by
the worker automation clone. It was reused read-only, so this is nonrelease
evidence. No dependency update, fetch, clone, or build was run.

Commands and results:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: ok; 1546 uniform-L0 Lean 4 targets
python3 scripts/stage1_target.py check
  exit 0: ok; 1546 unique targets, ranks 1..1546
python3 scripts/stage1_target.py show THM-M-1244
  exit 0: rank 425, planned, L0/rework-required, theorem_complete false
cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1244/Statement.lean
  exit 0: canonical target, expanded target, definitional transport, and four mutations elaborated; explicit canonical expression printed
python3 Stage1_Instances/THM-M-1244/check_statement.py
  exit 0: expression sha256 eeff335a47ceaf9d469f25e1570640f17008c1f38d8173499a5429e7ab6397b3; all four mutations differed; mathlib revision 8a178386ffc0f5fef0b77738bb5449d50efeea95
cd Formalizations/Lean && lake env lean --version
  exit 0: Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740
python3 -m json.tool Stage1_Instances/THM-M-1244/statement.json
  exit 0
git diff --check -- Stage1_Instances/THM-M-1244
  exit 0
```

This validates the statement phase only. The target is proposition-valued and
has no proof body. Source audit, candidate audit, proof, trust closure, release
validation, independent review, master acceptance, and theorem completion remain open.
