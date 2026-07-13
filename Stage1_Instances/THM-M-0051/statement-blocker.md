# Exact-statement gate: blocked

Item: `S56-M-0051-STATEMENT`

Theorem: `THM-M-0051`

Base revision: `72e9e8092182121a6794921f61fcc9cae22f726d` (tree
`0d6c1fdf06d1573c256af331c6b198e5a787af43`).

## Decision

The statement item remains `[ ]`. Rev-5.6 permits dependency-ordered preparation while
`S56-M-0051-INTAKE` has provisional worker state `[_]`, but that intake receipt has
`accepted: false`, no accepted receipt ID, and no master acceptance. More importantly, its
structured scope authority deliberately leaves the canonical mathematical claim, formal target,
expression hash, and target-environment fingerprint null.

The repository source supplies only the title `格拉斯曼恒等式`, the attribution to Hermann
Grassmann in 1844, and the gloss `关于外代数的恒等式` ("an identity about exterior algebra"). It
contains no formula, edition or passage, incorporated definition, domain, ordered binder,
hypothesis, conclusion, sign or grading convention, characteristic assumption, proof boundary,
correction history, or independent review. The catalog's `已验证` label is explicitly untrusted.

The intake authenticated only bibliographic metadata for Grassmann's 1844 work family through the
2012 Cambridge reprint record, DOI `10.1017/CBO9781139237352`. No original or reprint body, exact
identity, theorem or page, proof, translation, edition relationship, correction, or erratum was
inspected. This remains an `H1` source lead, not a source-selected proposition.

Several materially different formulas fit the sparse name and gloss:

- a degree-one exterior generator squares to zero;
- two degree-one generators anticommute;
- homogeneous elements obey a graded sign rule;
- alternating products satisfy concatenation, permutation, or functoriality identities;
- Grassmann-Pluecker coordinates satisfy a decomposability relation; or
- an older Grassmann calculus identity requires a checked translation to modern exterior algebra.

Other results are also called Grassmann formulas or identities, including the subspace-dimension
formula and three-dimensional vector triple-product identities. They have different domains and
conclusions, and the catalog's exterior-algebra gloss does not license either one. Selecting any
candidate from topic similarity would invent, narrow, or substitute the requested theorem.

The unresolved choices include the coefficient ring or field and characteristic, module carrier
and universes, finite-dimensional or freeness assumptions, degree and parity, binders, equality
carrier, wedge or multiplication spelling, permutation and sign conventions, coordinate and
decomposability setup, and all zero-ring, zero-module, repeated-vector, empty-family, degree, rank,
and characteristic-two boundaries.

Rev-5.6 makes this ambiguity and the missing elaborated-expression fingerprint hard blockers.
There is no honest canonical target whose imports can be certified minimal, no credited alternate
encoding for a checked transport, and no meaningful removed-hypothesis, changed-domain,
changed-binder-scope, or boundary-case mutation suite. Those mutations are undefined, not passed.
The lifecycle stays `planned`, and the root vector stays `[H1, M4, R4]`.

## Pinned Lean Boundary

The existing discovery-only `IntakeProbe.lean` was re-elaborated with the pinned environment. Its
three direct imports expose multiple incompatible candidate surfaces:

- `Mathlib.LinearAlgebra.ExteriorAlgebra.Grading` supplies exterior-algebra construction, generator,
  universal-property, multi-wedge, and grading interfaces;
- `Mathlib.LinearAlgebra.FiniteDimensional.Lemmas` supplies
  `Submodule.finrank_sup_add_finrank_inf_eq`; and
- `Mathlib.LinearAlgebra.CrossProduct` supplies vector triple-product identities.

The probe checks fourteen adjacent declarations. Five representative axiom reports contain only
`propext`, `Classical.choice`, and `Quot.sound` as applicable. The complete stdout has SHA-256
`91a73943e432afea0edaf522df5a4ac81a123afd207df9f9ad1bc0c53d229690`.

This is real substrate validation only. The probe declares no canonical target, checked transport,
or proof body. A bounded exact-topic search of pinned mathlib and repo-local Lean found no
catalog-identical declaration; it is discovery evidence, not a complete anchor audit or proof of
global absence. The probe imports cannot be called minimal imports for an absent target.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No update, build, dependency clone, fetch,
or other `.lake` mutation was performed.

## Validation Record

Commands ran from this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0051` | 0 | rank 1520; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `.lake` symlink was untracked; base identifiers appear above |
| `git blame -L 384,389 -- Docs/researches/math_theorems.md` | 0 | all six sparse catalog fields originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | pinned mathlib revision/tree recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --short` | 0 | empty output; pinned package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0051/IntakeProbe.lean` | 0 | fourteen adjacent APIs elaborated; five axiom reports printed; no target declaration or proof body; stdout hash recorded above |
| bounded Grassmann-identity/Grassmann-Pluecker search in pinned mathlib and repo-local Lean | 0 | only the owned probe disclaimer and unrelated Plucker prose matched; no catalog-identical target declaration was found |
| `python3 -B Stage1_Instances/THM-M-0051/check_intake.py` | 1 | historical intake validator expects the intake item to remain `[ ]`; integrated authority now records provisional `[_]`, so the checker is stale and is not statement evidence |
| prohibited-declaration `rg` scan over owned Lean files | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration was found |
| `python3 -m json.tool Stage1_Instances/THM-M-0051/statement-blocker.json` | 0 | structured blocker parsed as valid JSON |
| scoped Python blocker invariant and input-hash check (inline script reproduced by the worker log) | 0 | identity, null target/imports/fingerprints, unchanged vector, current hashes, four undefined mutations, false completion fields, and no-receipt/no-self-test boundary agree |
| scoped tracked and new-file whitespace checks | 0 | no whitespace diagnostics; each no-index exit 1 was only the expected new-file difference |
| `test ! -e .stage1-worker-selftest.json` | 0 | self-test manifest intentionally absent because the exact-statement deliverable did not pass |

The intake checker is bound to intake-time authority and was not edited to manufacture agreement.
The statement blocker is validated separately; the generated blueprint, authoritative execution
DAG, intake instance, intake receipt, and open task DAG remain unchanged.

## Retry Condition And Status Boundary

Accountable reviewers must lawfully preserve and hash an immutable original or approved
authoritative source passage and independently select one exact identity. They must transcribe
every incorporated definition, ordered binder, hypothesis, conclusion, proof boundary,
translation, edition relationship, correction, erratum, coefficient and module assumption, degree,
sign, grading, characteristic, coordinate, decomposability, and boundary convention.

A fresh statement run may then encode exactly that approved claim, minimize its pinned imports,
serialize and hash the elaborated expression and environment, compile every credited transport,
and execute the required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case
mutations. The integration lane must also revalidate and master-accept the intake before accepting
that future transition.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. `audit_complete: false` and `theorem_complete: false`; no debt-vector change is
proposed. Because the exact-statement deliverable did not pass, no `.stage1-worker-selftest.json`,
statement receipt, worker `[_]`, proof credit, or master acceptance is claimed.
