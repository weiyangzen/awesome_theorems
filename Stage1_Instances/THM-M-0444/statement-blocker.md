# Statement gate blocker

Item: `S56-M-0444-STATEMENT`  
Theorem: `THM-M-0444`  
Verdict: blocked; no exact canonical Lean target is claimed.

Rechecked: `2026-07-17` (`Asia/Shanghai`) at repository base
`1cc6aa61bb055a5c032297ee457905c849af7608`.

This target-owned phase assessment is now normalized into the four HEAD contract roles:
`statement.json`, `Statement.lean`, `source_statement_crosswalk.md`, and
`statement-receipt.json`. `check_statement.py` emits the required typed negative semantic result.
Those artifacts self-test only the blocker boundary; the positive statement deliverable remains
unsatisfied, and the raw blocked result cannot support phase acceptance.

## First failed gate

The repository source record supplies only the label "Kolyvagin Euler system" and the gloss
"construction of an Euler system". It does not pinpoint a primary-source theorem or fix the base
field, elliptic curve or Galois representation, coefficient ring and prime, auxiliary indices,
field tower, cohomology groups, local conditions, Euler factors, Frobenius convention, or the
precise existence and compatibility conclusion. These choices distinguish materially different
constructions. Selecting one without a source pinpoint would invent missing mathematics and would
broaden or substitute the target.

The intake identifies Kolyvagin's 1990 *Euler systems* chapter only as a discovery candidate; no
edition page and theorem label have been accepted. The exact ordered binders, hypotheses,
conclusion, exceptional cases, canonical expression, expression fingerprint, checked transports,
and meaningful removed-hypothesis, changed-domain, changed-scope, and boundary mutations required
by rev-5.6 section 5.1 therefore cannot truthfully be produced. This is the hard statement-identity
blocker already anticipated by the accepted dependency's dossier.

The legacy discovery module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_090.lean` does elaborate in the pinned
environment, but it does not repair the blocker. Its `StatementShape` asserts nonemptiness of a
locally designed `KolyvaginEulerSystemConstructionData` structure whose index type, admissibility
predicate, norm relation, derivative operator, local condition, and Selmer conclusion are abstract
fields. The module itself calls this deliberately weaker than a terminal theorem. Treating that
user-supplied interface as Kolyvagin's construction would be a proxy-statement substitution, so it
receives no exact-statement credit.

No theorem declaration, proxy predicate, proof placeholder, custom trust declaration, broadened
target, or substituted special case was introduced. Machine status remains `M4`, and statement
acceptance and theorem completion are false.

The v2 node's exact `parent_inspection_order` is empty: it has no direct hard parent, transitive hard
ancestor, incoming hard edge, reuse hint, or shared group. `dependency-reuse-ledger.json` binds that
complete empty closure to graph digest
`e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b` and context digest
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
No provider body, receipt, checkbox state, or acceptance is consumed or transferred. The absence of
admitted graph context is not a mathematical independence claim.

## Environment fingerprint

- Repository base revision: `1cc6aa61bb055a5c032297ee457905c849af7608`.
- Repository base tree: `dc3053b55c5724ccb2e6a247e7deffebca9dbb99`.
- Validation date: 2026-07-17 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Legacy discovery module SHA-256:
  `50c776ffe34f43a11629d861b17bf95368ba96d71072d40e0f34c568e9b75fb2`.

## Validation evidence

Commands ran in this worker clone using only the existing canonical pinned `.lake` artifacts. No
update, build, fetch, or clone command was used.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean --trust=0 ../../Stage1_Instances/THM-M-0444/Statement.lean` from `Formalizations/Lean` | 0 | The two pinned adjacent interfaces elaborated; the file deliberately contains no canonical target |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0444/check_statement.py` | 0 | Exactly one `stage1-validator-semantic-result/1.0` object reported `status=blocked`, `phase_accepted=false`, and the exact failed gate |
| schema-1.1 ledger validation against the exact graph digest, context, and base | 0 | The direct/transitive parent, hard-edge, hint, group, inspection, decision, and unresolved-obligation lists are all exactly empty |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0444` | 0 | Rank 90, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 Docs/tools/check_stage1_standard.py` | 1, expected worker-local inventory drift | Target-owned statement artifacts are absent from the read-only generated theorem-DAG inventory until master integration regenerates it |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1, same expected drift | Structural generation detects the new owned artifacts; this worker is forbidden to edit the projection |
| `git diff --check -- Stage1_Instances/THM-M-0444 .stage1-worker-selftest.json` | 0 | No whitespace error in the owned handoff |

## Retry condition

Provide an immutable primary-source edition and exact theorem/page pinpoint selecting the intended
Kolyvagin construction. The source transcription must fix every arithmetic datum, ordered binder,
hypothesis, indexed class, cohomology target, local condition, norm/corestriction relation, Euler
factor and Frobenius convention, including exceptional cases and errata. The next statement run can
then encode the claim with minimal pinned imports, serialize its elaborated expression, and run the
four required mutation classes.

Until that retry condition is met, the statement phase cannot satisfy its positive completion
predicate. `.stage1-worker-selftest.json` hands off a self-tested negative result only: its `[_]`
proposal remains unfinished worker state and must never be interpreted as `phase_accepted`.
