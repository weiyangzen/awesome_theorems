# S56-M-0082-PROOF worker evidence

Date: `2026-07-12`

Base revision: `1e6618db41628006f4ba98117f6425af1eb6a0ba`.

## Implemented proof

`Proof.lean` checks the selected pinned mathlib declaration at the exact
`GeneralRightAdjointBridge` interface frozen by the obligation registry. It
then applies the already checked `root_of_bridge` transport, yielding the exact
`GeneralRightAdjointTarget` with independent category universes and the frozen
explicit `HasLimits`, `PreservesLimitsOfSize`, and `SolutionSetCondition`
hypotheses. No hypothesis is added or removed.

Lean elaborated both proof bodies and reports the ordinary mathlib axiom
closure `[propext, Classical.choice, Quot.sound]`. The sources contain no
`sorry`, `admit`, `sorryAx`, or new `axiom`. This self-tests the assigned proof
phase pending master acceptance. It does not claim validation, source/readable
closure, release acceptance, audit completion, or theorem completion.

The obligation-tree check still prints its frozen pre-integration boundary
(`M0082-X-BRIDGE` open). That is expected: a proof worker must not rewrite the
accepted architecture artifact or its phase-specific historical result. The
new proof module supplies and checks that bridge; the later validation lane
must reconcile structured closure evidence.

## Commands and exact results

All commands ran from the worker clone. No Lake update, build, fetch, clone, or
dependency mutation was performed.

```text
$ python3 Docs/tools/check_stage1_standard.py
check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)
exit 0

$ python3 scripts/stage1_target.py check
stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)
exit 0

$ python3 scripts/stage1_target.py show THM-M-0082
execution_rank 135; baseline L0; rework_required true; planned; theorem_complete false
exit 0

$ (cd Formalizations/Lean && bash ../../Stage1_Instances/THM-M-0082/check_proof.sh)
GeneralRightAdjointTarget elaborated; root_of_bridge, generalRightAdjointBridge,
and generalRightAdjointTarget each report [propext, Classical.choice, Quot.sound]
exit 0

$ python3 Stage1_Instances/THM-M-0082/check_proof.py
PASS THM-M-0082 proof source: exact bridge and root composition present
exit 0

$ python3 Stage1_Instances/THM-M-0082/check_obligation_tree.py
PASS THM-M-0082 obligation tree: 13 obligations, 39 typed edges
registry denominator sha256: 769e9ea30a88f4aee8aba874a58059ebaffc194822e5c62f1fe79866822892a9
root closure: open (M3); exact central bridge remains M4
exit 0 (expected frozen architecture-phase boundary)

$ rg -n '\b(sorry|admit|sorryAx)\b|(^|[^[:alnum:]_])axiom[[:space:]]' Stage1_Instances/THM-M-0082/Proof.lean
no output
exit 1 (expected clean scan)

$ git diff --check -- Stage1_Instances/THM-M-0082
no output
exit 0

$ git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD
8a178386ffc0f5fef0b77738bb5449d50efeea95
exit 0

$ (cd Formalizations/Lean && lake env lean --version)
Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740
exit 0
```

Validated SHA-256 values:

```text
27d31398b0dd5bddcd8cb6f781702eac5624b91cccbce6ecffe9f16da37cff72  Statement.lean
fddcf083e91f76c89b82efccec0a6f4434cb7127f15b6eb1491aa1121184bb59  ObligationTree.lean
80ed25bf1faf53d09c00dc619af185cad711a4ae6d4688bb04799019de5c4445  Proof.lean
```

Known failures outside this phase: node-specific H/R review, provenance and
trust closure, hermetic replay, freshness receipts, and independent validation
remain open. The integration lane must also reconcile the proof result into
the structured obligation state before any M0 or theorem-completion decision.
