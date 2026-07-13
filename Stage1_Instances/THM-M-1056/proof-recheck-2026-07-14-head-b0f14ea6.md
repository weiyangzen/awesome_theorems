# THM-M-1056 proof recheck at `b0f14ea6`

Item: `S56-M-1056-PROOF`

Base revision: `b0f14ea655d04a569f7796528a1860935721948f`

Base tree: `5f7705bbd92801b826caed4950e24c7b942af1f3`

Attempt date: 2026-07-14 (Asia/Shanghai)

## Verdict

`blocked`; this execution added no proof body, closed no frozen obligation,
and proposes no state change. The first failed gate remains `M1056-T-CORE`.
There is no placeholder-free inhabitant of `OseledetsCorePackage` in the
repository or pinned Lake closure. In `ObligationTree.lean` that package is
definitionally the complete universal target, and
`root_of_oseledetsCorePackage` merely returns its premise.

`SanityInstance.lean` proves only the one-point identity cocycle with fiber
`Real`. It demonstrates that the statement is inhabited and not vacuous; it
does not prove the universally quantified theorem.

The root vector therefore stays `[H1, M3, R3]`, lifecycle stays `planned`, the
minimal open root cut stays `M1056-T-CORE`, and there are no accepted receipt
IDs. Because this proof phase is not genuinely self-tested complete, the root
`.stage1-worker-selftest.json` is deliberately absent.

## External Candidate

The immutable cached source
`marcmorningstar/lean4-ergodic-theory@ed3fa6b8a30594eeb791160563942ba115581aa0`
contains the substantive theorem `ErgodicTheory.oseledets_splitting`. It
returns measurable Euclidean submodules, an internal direct sum, nonzero
summands, subspace equivariance, and forward/backward vector growth for a
matrix cocycle. It does not directly return the exact target:

- its fiber is `EuclideanSpace Real (Fin d)`, rather than arbitrary `E`;
- its output is a family of submodules, rather than strongly measurable
  continuous-linear component projections;
- it has no supplied construction proving the component projections are
  idempotent, pairwise annihilating, sum to the identity, equivariant, and
  nonzero almost everywhere.

A possible bridge starts with orthogonal projectors `P_i` and
`S = sum_i P_i`, proves `S` invertible from the internal direct sum, and sets
`Q_i = P_i * S^-1`. The cached source has matrix determinant, inverse, and
subspace measurability infrastructure, but not the invertibility proof, the
component-projection algebra, strong measurability as continuous-linear maps,
or transport through coordinates. Exact integration must additionally
conjugate the cocycle through a finite-dimensional continuous linear
equivalence and transport measurability, inverse/determinant facts, both
log-norm integrability hypotheses, iterates, equivariance, and vector growth.
Importing only the matrix/submodule theorem would substitute a narrower
theorem.

The candidate requires Lean `4.30.0-rc2` and mathlib `34f7a6cd...`; this clone
uses Lean `4.29.0` and mathlib `8a178386...`. A read-only scratch port probe
under `/tmp/m1056-closure-compile.FFeoWc` applied only 3
`integrable_finset_sum` and 7 `integral_finset_sum` compatibility renames. The
first eight files attempted in the 62-file local closure then elaborated. File 9,
`ErgodicTheory/Ergodic/Kingman/BlockSqueeze.lean`, failed because the pinned
toolchain lacks four upstream `Tendsto` limsup/liminf APIs, with one consequent
unsolved goal. A compatible local reproof of those four calls was independently
elaborated at `/tmp/m1057-proto/KingmanBlockSqueeze.lean`; thus this particular
failure is repairable and is not presented as the fundamental blocker. The
substantial exact-wrapper work above remains absent.

No dependency was installed, fetched, or added to Lake. The pre-existing
`.lake` link was used read-only, and all port outputs remained under `/tmp`.

## Fresh Validation

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1056` | 0 | Rank 248; lifecycle `planned`; `theorem_complete: false`. |
| `python3 Stage1_Instances/THM-M-1056/check_obligation_tree.py` | 0 | 19 obligations and 49 typed edges passed; denominator `5246a9d5966e76ff5cb379c8f39f48100fafd3c2ce99bf7c7e10f953f8b57828`; root open M3 and core M4. |
| From `Formalizations/Lean`, copy `Statement.lean`, `ObligationTree.lean`, and `SanityInstance.lean` to a fresh `/tmp` directory; elaborate them in order with `LEAN_NUM_THREADS=1 lake env lean`, using the temporary directory in `LEAN_PATH`; remove the directory | 0 | All three isolated modules elaborated. `#print axioms` reported exactly `[propext, Classical.choice, Quot.sound]` for conditional composition and the sanity conclusion. |
| `rg -n '^\\s*(sorry|admit|axiom)(\\s|$)|sorryAx|^\\s*unsafe\\s' Stage1_Instances/THM-M-1056 -g '*.lean'` | 1 | Expected no-match exit; no prohibited Lean declaration token occurs. |
| `rg -n -i '(^|[^A-Za-z])(oseledets|multiplicative ergodic|kingman)([^A-Za-z]|$)' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | Expected no-match exit; pinned mathlib has no named terminal Oseledets or Kingman theorem. |
| Scratch closure compile using `LEAN_NUM_THREADS=1 LEAN_PATH=/tmp/m1056-closure-compile.FFeoWc:$(lake env printenv LEAN_PATH) lake env lean --root=<cached-upstream> -o <scratch-olean> <source>` | files 1-8: 0; file 9: 1 | After the 10 recorded identifier renames, the first 8 attempted files elaborated. `BlockSqueeze.lean` stopped at four missing limsup/liminf APIs and one consequent goal; the compatible reproof described above separately elaborated. |
| `python3 -m json.tool Stage1_Instances/THM-M-1056/proof-recheck-2026-07-14-head-b0f14ea6.json >/dev/null` | 0 | Structured blocker evidence parsed as valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-1056` | 0 | No scoped whitespace error. The two untracked artifacts were also checked with `git diff --no-index --check /dev/null <file>`; each produced only the expected new-file difference exit 1. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Self-test manifest is absent because the assigned proof phase is incomplete. |

Toolchain evidence: Lean 4.29.0 commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` and tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

Frozen artifact hashes:

- statement: `00c1ca022adb35d49369df14a420b64b4c7b77f1fe8858aba85d4df0793f3886`
- obligation tree: `4286d31290c2df8d1535cd9d58d6574ad0dad1b828fb58a78b5be3c3a5b3647c`
- obligation registry: `281d9dcd7ede39aa609c30a42649f57b14b7886d46ca9d0c767a626577316476`
- typed graphs: `50903cbdbc7208ff4d6282421fabcb9661e4575fb1298210d631b84ca468b477`

## Reopen Condition

Resume after placeholder-free bodies exist for the frozen core packages, or
after the immutable external development is compatibly ported together with
kernel-checked coordinate, measurable-component-projection, exact-type,
provenance, and trust transports. Until then this artifact is blocker evidence
only and cannot receive `[_]` or theorem-completion credit.
