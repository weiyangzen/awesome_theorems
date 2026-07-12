# Exact-statement gate: blocked

Item: `S56-M-0354-STATEMENT`  
Theorem: `THM-M-0354`  
Worker base revision: `396f523f7db5499e43d86728d9cfe073ac081dfa`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
entire mathematical statement available for this target is `L^2[0,1]`'s "complete orthogonal
wavelet basis". Stage0 explicitly leaves the precise definitions and assumptions open, and the
intake correctly records that no exact source passage has been selected or inspected.

That gloss does not determine a single proposition. In particular, it leaves open:

1. real versus complex scalars and the concrete Lean model of `L^2[0,1]`;
2. whether the constant scaling function is a separate index and the exact scale/translation index
   type;
3. normalization of each Haar function and half-open versus closed endpoint conventions;
4. whether "basis" means an orthonormal Hilbert basis, orthogonality plus dense span, a Parseval
   identity, or an expansion theorem.

These choices change the ordered binders, definitions, and conclusion. Endpoint choices require an
explicit almost-everywhere transport rather than definitional equality. Selecting convenient
conventions or an abstract existence theorem would therefore substitute mathematics not fixed by
the source. There is consequently no canonical expression to serialize or hash, no credited
alternate encoding to transport, and no sound removed-hypothesis, changed-domain, changed-scope,
or boundary mutation suite. The rev-5.6 section 5.1 statement gate fails before proof evidence may
be inspected.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated using the pinned environment. It confirms only
that mathlib exposes the unit-interval measure, `Lp`/`MemLp`, and Hilbert/orthonormal-basis APIs. A
narrow name search of pinned mathlib found uses of Haar *measure* but no Haar wavelet declaration.
Neither observation supplies the missing mathematical statement, and the probe receives no
statement or proof credit.

The environment is Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, with pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Existing canonical `.lake` artifacts were used read
only. No update, build, clone, fetch, or dependency mutation was run.

## Exact validation record

Commands ran in this worker clone on 2026-07-12 (`Asia/Shanghai`).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets; ranks 1 through 1546; all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0354` | 0 | rank 847; planned; legacy artifacts unaccepted; theorem incomplete |
| `rg -n -C 5 'THM-M-0354\|哈尔小波基\|Haar wavelet basis\|L\^2\\[0,1\\].*完备正交' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Docs/Stage1_Targets_rev-5.6.json` | 0 | found only the short gloss, untrusted status, and explicitly open definitions/assumptions |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean version and commit reported above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision reported above |
| `rg -n 'haar\|Haar\|wavelet' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | matches concern Haar measure; no theorem-specific wavelet target was identified |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0354/IntakeProbe.lean)` | 0 | six substrate API checks elaborated; no canonical target asserted |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0354 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom found |
| `python3 -m json.tool Stage1_Instances/THM-M-0354/instance.json` | 0 | intake JSON is syntactically valid |
| `python3 -m json.tool Stage1_Instances/THM-M-0354/task-dag.json` | 0 | task DAG JSON is syntactically valid |

## Retry condition and status boundary

The first unblocker is an immutable, independently inspected source passage that fixes the scalar
field, unit-interval measure model, scaling function, dyadic index ranges, normalization, endpoint
policy, and precise completeness formulation. A later statement worker can then encode that same
claim, minimize imports, preserve the elaborated expression and environment fingerprint, compile
all required transports, and run the four mutation classes.

This node remains `[ ]`, blocked at `M4`; the root remains `[H3, M4, R4]`, with
`audit_complete: false` and `theorem_complete: false`. The assigned statement deliverable is not
genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
