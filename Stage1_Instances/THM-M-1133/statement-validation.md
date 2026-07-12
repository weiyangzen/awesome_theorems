# Statement validation

Base revision: `5616162cb70eb9714202c5cfe98baa99a30e95a3`.

The exact statement and its four separately named structural mutations were
kernel-elaborated using the canonical pinned Lake environment. From
`Formalizations/Lean`, the narrow check was:

```text
lake env lean ../../Stage1_Instances/THM-M-1133/Statement.lean
```

Exit code was `0`. Lean printed the fully explicit type of
`Stage1Instances.THM_M_1133.HeatEquationWeakMaximumPrinciple`; its captured
stdout SHA-256 was
`cb70ff9396c3c5fad0ea98bf234dc38f20738f5ff2accc32b4712675e90e5c3b`.
The source SHA-256 was
`63e7f31ae3f3b1a8d0a06836f6afe31960fa1cb0c461922eaf69c08cedcd7bee`.

Environment inspection returned Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. No dependency update, fetch,
clone, or build was run.

The following repository and artifact checks also exited `0`:

```text
python3 Docs/tools/check_stage1_standard.py
python3 scripts/stage1_target.py check
python3 scripts/stage1_target.py show THM-M-1133
python3 -m json.tool Stage1_Instances/THM-M-1133/statement.json
git diff --check -- Stage1_Instances/THM-M-1133 .stage1-worker-selftest.json
```

The standard validator reported 15 assurance groups, 41 legacy rows, 300
legacy slots, and 1546 uniform-L0 targets. The manifest validator reported
1546 unique ranks, and `show` confirmed rank 338, planned lifecycle, and no
theorem-completion claim.

This is statement elaboration evidence only. No theorem proof, axiom audit,
hermetic release, or master acceptance is claimed.
