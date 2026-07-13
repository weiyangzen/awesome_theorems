# Exact-statement gate: blocked

Item: `S56-M-1458-STATEMENT`

Theorem: `THM-M-1458`

Base revision: `2d82479e32843fd52283dcd9bb305954729c1199` (tree
`30134b43ab41e973d2558be90371bf18d6edb259`).

## Decision

The statement item remains `[ ]`. Its prerequisite `S56-M-1458-INTAKE` has provisional worker
state `[_]`, not master-accepted state `[x]`; its receipt has `accepted: false` and no accepted
receipt ID. Rev-5.6 section 10.2 permits provisional preparation of a later node, but accepted
closure remains dependency ordered.

Independently, the exact-statement gate cannot pass. The complete repository record is the label
`fast Fourier transform`, attribution to Cooley and Tukey in 1965, and the gloss `a fast algorithm
for the DFT`. It supplies no truth-valued proposition, bibliography, DFT formula, domain, ordered
binder, premise, algorithm, correctness relation, cost model, conclusion, proof boundary,
correction history, or boundary convention. The catalog's `verified` label is untrusted under
rev-5.6.

Materially inequivalent statements fit that gloss. The DFT may use positive or negative
exponents, forward or inverse normalization, and `Fin N`, `ZMod N`, vectors, arrays, or matrices.
The length may be an arbitrary composite, a product `N1 * N2`, or a power of two. The algorithm
may be an algebraic Cooley-Tukey decomposition, radix-2 recursion, mixed radix, decimation in time
or frequency, or an in-place implementation with a particular permutation and layout. The
conclusion may be a factorization identity, pointwise equality with a dense DFT, termination,
exact operation counts, or an asymptotic `O(N log N)` bound in a selected cost model. These choices
also change the treatment of zero, one, prime and non-power-of-two lengths, trivial factors, empty
and singleton input, invalid array sizes, and permutation direction.

Choosing a familiar radix-2 correctness or complexity theorem would silently resolve all of these
open decisions. It would invent, narrow, broaden, or substitute proposition-changing mathematics
rather than elaborate the exact received target.

Sections 5 and 5.1 make statement ambiguity and a missing expression fingerprint hard blockers.
There is consequently no canonical expression for which minimal imports, fixed elaboration
context, a serialized target, an environment fingerprint, checked alternate transports, or the
required removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations can
be certified. All four mutation classes are undefined, not passed. No `Statement.lean`, theorem
declaration, proof body, abstract structure storing the result, weakened special case, or broadened
interface was added. The root remains `[H5, M4, R4]`.

## Source And Lean Boundary

The repository's bibliographic lead is Cooley and Tukey, *An Algorithm for the Machine Calculation
of Complex Fourier Series*, *Mathematics of Computation* 19(90) (1965), pages 297-301, DOI
`10.1090/S0025-5718-1965-0178586-1`. Only bibliographic metadata was admitted during intake. The
catalog does not cite the article, no lawful immutable full-text edition or exact passage is in the
dossier, and no proposition, incorporated definition, premise map, proof boundary, correction
audit, or independent source review has been accepted. The lead supplies no exact-statement or
`H0` credit.

The existing `IntakeProbe.lean` imports
`Mathlib.Analysis.Fourier.FiniteAbelian.PontryaginDuality` and
`Mathlib.Analysis.Fourier.ZMod`. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, it checks eight dense-DFT, inversion, and
finite-character APIs. Those declarations are possible reference semantics only. They define no
fast algorithm, Cooley-Tukey factorization, recursion or permutation, correctness bridge, or cost
bound. The imports are sufficient for the combined discovery probe, but they cannot be called
minimal for a canonical target that does not exist.

A bounded case-insensitive search of tracked repository Lean and pinned mathlib found no declaration
named or documented as FFT, fast Fourier transform, Cooley-Tukey, radix-2, or butterfly. This is
narrow feasibility evidence, not the downstream exhaustive anchor audit or a global absence claim.

The worker environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The automation-provided
`Formalizations/Lean/.lake` symlink was used read-only. No dependency update, build, clone, fetch,
or other `.lake` mutation was run.

## Validation Record

Commands ran in this isolated worker clone on 2026-07-13 (`Asia/Shanghai`).

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1458` | 0 | rank 1135; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| pre-edit `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree appear above |
| exact reads of the blueprint, skill, manifest/DAG rows, catalog, Stage0 record, and intake dossier | 0 | confirmed the statement gate, method-only gloss, explicitly open fields, and null canonical target |
| `python3 -B Stage1_Instances/THM-M-1458/check_intake.py` | 1 | historical intake checker expects authoritative intake state `[ ]`; integration now records provisional `[_]`, so this phase records rather than rewrites stale intake evidence |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib `git rev-parse HEAD 'HEAD^{tree}'` and package status | 0 | pinned revision and tree recorded above; package worktree clean |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1458/IntakeProbe.lean` | 0 | eight adjacent APIs elaborated; stdout SHA-256 `5898e3735ce796f385476d4a3d9a7d92ff3dcd2850cd726ce31db56d43098ec8`; no canonical target |
| bounded exact-topic search in tracked project Lean (`Formalizations/Lean/AwesomeTheorems.lean` and `Formalizations/Lean/AwesomeTheorems`) and pinned mathlib | 1 | expected no-match result; no FFT/Cooley-Tukey/radix-2/butterfly declaration was located |
| prohibited-construct scan over owned Lean files | 1 | expected no-match result; no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration |

Final JSON, invariant, whitespace, and absent-self-test checks are recorded in the structured
blocker beside this report; each exited zero.

## Retry Condition And Status Boundary

The integration lane must master-accept refreshed intake evidence. Accountable reviewers must
preserve and admit an immutable exact source proposition and independently approve every
incorporated definition and its proof boundary. That selection must fix the DFT carrier, indices,
sign, primitive root and normalization; permitted lengths and factorization; algorithm, recursion,
twiddle factors, permutation, stride and layout; correctness, termination and any cost conclusion;
ordered binders; and every degenerate case.

A fresh statement worker can then encode precisely that reviewed claim, minimize its pinned
imports, serialize and hash the elaborated expression and environment, compile every credited
transport, and execute all four required mutation classes.

This blocker is the assigned phase's truthful result, not completion of the statement node or any
downstream node. Lifecycle remains `planned`; `audit_complete: false` and
`theorem_complete: false`; no debt-vector change is proposed. Because the exact-statement
deliverable did not pass, no `.stage1-worker-selftest.json`, statement receipt, worker `[_]`, or
master acceptance is claimed.
