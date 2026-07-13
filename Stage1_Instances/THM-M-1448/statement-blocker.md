# THM-M-1448 exact-statement gate: blocked

Item: `S56-M-1448-STATEMENT`

Base revision: `03bed3c211cb739ccd2629908210fda0f9adf6ca` (tree
`a48670276bfe2105ddbfb4057314b21056dae0cb`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1448-INTAKE` is only in provisional
worker state `[_]`; `intake-receipt.json` has `accepted: false` and no accepted receipt IDs. The
receipt also binds older blueprint and execution-DAG hashes, so it is not current accepted
dependency evidence.

More importantly, the intake deliberately leaves the exact human proposition, Lean module,
declaration or expression, expression hash, and canonical-target environment fingerprint
unresolved. The catalog says only "an orthogonal-triangular factorization of a matrix." It does not
fix the real or complex scalar field, square or rectangular shape, dimensions, rank hypotheses,
full or reduced QR convention, factor dimensions, orthogonal versus unitary equations,
rectangular triangularity convention, diagonal normalization, uniqueness, or empty and
rank-deficient cases. The probable duplicate `THM-M-0046` has a similarly sparse gloss and no
accepted identity decision.

Axler, *Linear Algebra Done Right*, fourth edition, Theorem 7.58 is a precise source lead for square
real or complex matrices with linearly independent columns. It asserts unique `Q` and `R`, with
`Q` unitary, `R` upper triangular with positive diagonal, and `A = Q R`. The observed author-hosted
PDF has SHA-256 `45f821b6f51e1f6c42728db6254699d89c14c90fcdb2443c1341188672815d03`,
but the catalog does not cite it, its narrower proposition has not been immutably preserved and
admitted, and no correction audit or independent source review is recorded. Selecting it would
silently narrow the catalog wording; selecting an arbitrary rectangular or rank-deficient variant
would silently broaden or otherwise substitute the theorem.

Rev-5.6 makes this ambiguity a hard statement-gate failure. There is no truthful canonical Lean
expression whose direct imports can be minimized, no expression to fingerprint, and no approved
alternate encoding to transport. The required removed-hypothesis, changed-domain,
changed-binder-scope, and boundary mutations are therefore not meaningful rather than passed. The
root vector remains `[H1, M3, R3]`.

## Pinned Lean Boundary

The discovery-only `IntakeProbe.lean` was re-elaborated against the existing pinned environment. It
checks Gram-Schmidt, orthonormal-basis, unitary-matrix, and block-upper-triangular interfaces. The
closest result, `InnerProductSpace.gramSchmidtOrthonormalBasis_inv_blockTriangular`, concerns an
input family's coefficient matrix and is an ingredient, not an exact QR factorization target. A
bounded exact-topic search found no QR decomposition or factorization declaration in repo-local
Lean or pinned mathlib. The probe imports therefore cannot establish minimal imports for a missing
canonical target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided canonical `.lake` symlink was
used read-only. No dependency update, build, clone, fetch, or other `.lake` mutation was run.

## Validation Record

Commands ran from this worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1448` | 0 | rank 1125; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `pwd; git status --short --untracked-files=all; git rev-parse HEAD 'HEAD^{tree}'` | 0 | worker clone confirmed; pre-edit status contained only the automation-provided untracked `Formalizations/Lean/.lake`; base revision and tree appear above |
| `git blame -L 10574,10579 -- Docs/researches/math_theorems.md; git blame -L 349,354 -- Docs/researches/math_theorems.md` | 0 | all twelve sparse catalog and duplicate lines originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'; git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1448/IntakeProbe.lean` | 0 | ten adjacent APIs elaborated; stdout SHA-256 `a267d192237ff7d7b566120b2ca204c1c86439906d38e454bf52178be04778a1`; representative axiom reports list only `propext`, `Classical.choice`, and `Quot.sound`; no target declaration |
| `rg -n -i 'QR (decomposition\|factorization)\|QRDecomposition\|QRFactorization\|qr_decomposition\|qr_factorization' Formalizations/Lean Stage1_Instances/THM-M-1448 --glob '*.lean' --glob '!Formalizations/Lean/.lake/**'` | 0 | only the intake disclaimer matched locally |
| same bounded search in `Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 (expected no match) | no exact pinned QR declaration matched |
| `python3 -B Stage1_Instances/THM-M-1448/check_intake.py` | 1 | historical intake validator is stale against the integration-updated intake state `[_]`; it fails at its old `[ ]` assertion and is not statement evidence |
| prohibited Lean declaration scan over `Stage1_Instances/THM-M-1448/*.lean` | 0 | inner `rg` returned the expected no-match result; no prohibited declaration was found |
| `python3 -m json.tool Stage1_Instances/THM-M-1448/statement-blocker.json` | 0 | finalized blocker is valid JSON |
| blocker invariant check | 0 | identity, null target/imports, unchanged vector, four undefined mutations, false completion flags, exact two-file scope, and no-self-test boundary agree |
| scoped whitespace checks | 0 | no whitespace diagnostics in the two blocker artifacts |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test manifest was emitted because the assigned statement deliverable did not pass |

The historical intake validator is intentionally not repaired by this statement-only assignment.
Its failure is recorded rather than hidden.

## Retry Condition

The integration lane must first accept fresh intake evidence. Accountable reviewers must then
preserve and hash a lawful immutable source, independently approve one exact QR proposition,
reconcile `THM-M-0046`, and freeze every field, shape, rank, factor, triangularity, normalization,
uniqueness, binder, hypothesis, conclusion, and boundary convention. A later statement run can
encode only that proposition, minimize its pinned imports, serialize the elaborated expression and
environment, compile every credited transport, and execute all four mutation classes.

This is a truthful blocked statement attempt, not completion of this node or any downstream node.
No statement receipt, root worker self-test packet, worker `[_]`, master acceptance, proof credit,
audit completion, or theorem completion is claimed.
