# Statement phase blocker

Item: `S56-M-0731-STATEMENT`

Base revision: `f12b1ccbda307337d488a2993eddbf883b722be6`.

## Verdict

The exact Lean 4 target cannot be elaborated truthfully from the repository source. The complete
source wording for this UID is the title `去随机化` and the gloss `随机算法的确定化` (turning
randomized algorithms into deterministic ones). It does not specify a proposition.

In particular, it leaves open the randomized machine model, input and randomness encodings,
success threshold and error mode, resource measure and bound, quantifier order, uniformity, advice,
hardness assumptions, and whether the deterministic object may depend on an input, an input length,
or neither. These omissions distinguish materially different claims, including finite seed fixing,
non-uniform simulation such as `BPP` contained in `P/poly`, conditional hardness-versus-randomness
results, and the unproved unconditional claim `BPP = P`. Selecting any one of them would broaden or
substitute the repository target rather than elaborate it.

Consequently there is no canonical declaration or expression to place in a Lean file, no exact
type to hash, and no sound hypothesis/domain mutation suite to run. `IntakeProbe.lean` remains only
an elaborated vocabulary check and is not promoted to a target statement. No `sorry`, `axiom`,
placeholder proposition, or theorem packaged as a hypothesis was introduced.

## First failed gate

The rev-5.6 exact-statement freeze fails before Lean elaboration: no immutable source passage
identifies a unique theorem and all of its assumptions. To unblock this node, source work must
independently select and inspect a pinpoint theorem, edition or immutable revision, page or theorem
identifier, definitions, assumptions, proof boundary, and errata, and must justify why that theorem
matches this repository UID rather than a neighboring derandomization result.

The phase is therefore `blocked`, remains at `[H5, M4, R4]`, and makes no audit-complete or
theorem-complete claim. Because the assigned deliverable was not genuinely completed, no
`.stage1-worker-selftest.json` is written.

## Validation evidence

The existing pinned `.lake` artifacts were used without update, build, clone, or fetch.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets validated |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets with ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0731` | exit 0; rank 768, lifecycle `planned`, theorem completion false |
| `rg -n -C 8 '去随机化|随机算法的确定化' Docs/researches/math_theorems.md` | exit 0; both duplicate records contain only the title, collective attribution, decade, gloss, importance, and untrusted status label |
| `sed -n '19920,20020p' Docs/Stage0_Blueprint.md` | exit 0; exact definitions, premises, proof route, axioms, and formal artifact are all `待补充` or `待选` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0731/IntakeProbe.lean)` | exit 0; the six API checks elaborate under the pinned Lean 4.29.0 environment; this checks vocabulary only |
| `rg -n --glob '*.lean' '\b(sorry|admit|axiom)\b' Stage1_Instances/THM-M-0731; test $? -eq 1` | exit 0; no prohibited token occurs in the owned Lean files |
| scoped Python assertions over `instance.json` | exit 0; canonical claim and formal expression are null and status is `open_due_to_source_statement_ambiguity` |
