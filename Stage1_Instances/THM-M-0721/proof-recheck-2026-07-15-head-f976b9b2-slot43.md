# THM-M-0721 proof recheck at `f976b9b2` (slot43)

Item: `S56-M-0721-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T20:44:04+08:00`

Base revision: `f976b9b21418bfda4bc815ba2a7238e932666231`

Base tree: `6fbe6e3a73d5005115818a8f902da2b70f4aab24`

## Verdict

`blocked`. No eligible Lean 4 proof body was implemented or found for the exact root
`Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage`. The proof item stays `[ ]`; lifecycle stays
`planned`; the root vector stays `[H1, M3, R4]`; audit completion and theorem completion stay
false.

The only checked local route to the root is `root_of_candidate_packages`. It consumes, but does not
construct, the two immediate root packages:

- `M0721-T-SAT-IN-NP`: faithful binary SAT encodings, verifier correctness, a polynomial
  certificate bound, and an actual bundled polynomial-time TM2 verifier;
- `M0721-T-UNIVERSAL-HARDNESS`: normalization of every frozen `InNP` verifier, Cook-Levin
  tableaux, both correctness directions, and an actual bundled polynomial-time TM2 reduction.

Eleven SAT and Cook-Levin packages remain open. Each still has only a planned prose fingerprint,
not an exact Lean declaration type, so append-only exact-signature refinement is needed before a
worker can implement and receive proof credit for those leaves. The target-local task DAG also has
no accepted state: the obligation-tree node is worker-self-tested (`[_]`) but is not master-accepted.
Proof work can be prepared provisionally, but this proof node cannot yet be dependency-legally
accepted.

Pinned mathlib supplies the TM2 polynomial-time structure and identity implementation, but no NP,
SAT-language, or Cook-Levin endpoint. Its apparent composition declaration is source-level
`proof_wanted`; trust-zero Lean reports that the constant is unknown. Current-base, history, and
independent source scans found no inhabitant of either terminal package and no proof module,
receipt, or checker. The immutable external audit remains supporting-only, placeholder-dependent,
or contract-incompatible.

There is no definitional shortcut. `Nonempty` still requires a concrete TM2 structure with an
actual finite execution trace for every input. Classical choice cannot manufacture those traces,
and finite machine control cannot hide arbitrary language membership as an oracle. Empty,
universal, singleton, identity, membership-branching, and self-referential witnesses fail the
universal polynomial-time iff-reduction requirement. A universal encoded-verifier candidate still
requires precisely the missing serialization, normalization, correctness, and runtime proof.

## Required Split

There were already 31 target-owned dated unresolved proof JSON records before this run. Including
this recheck, the documented minimum is 32. Blueprint section 10.2 requires a split after five
unresolved execution ticks. The integration lane should accept or repair the obligation-tree
prerequisite, then replace this monolithic retry with dependency-legal child nodes for the eleven
frozen packages, beginning with an exact-signature child for `M0721-N-SAT-ENCODING`. The
authoritative DAG nevertheless still reports attempts `0` and no children; this worker did not edit
that DAG or the generated checklist.

## Validation

All commands ran in this worker clone. The pre-existing untracked `Formalizations/Lean/.lake`
symlink points to canonical pinned artifacts and was reused read-only. No `lake update`, `lake
build`, dependency clone/fetch/checkout, or `.lake` mutation was performed. The anchor validator
attempted one read-only HTTPS replay and timed out; no remote result is proof evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all; readlink -f Formalizations/Lean/.lake` | 0 | Base `f976b9b2...6231`, tree `6fbe6e3a...ab24`; initially only the automation-provided `.lake` symlink was untracked. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0721` | 0 | Rank 578; `planned`; L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| `LEAN_NUM_THREADS=1 timeout 600s python3 Stage1_Instances/THM-M-0721/check_statement.py` | 0 | Exact expression hash `758b1033...b204` matched and all four structural mutations were distinguished. |
| `timeout 180s python3 Stage1_Instances/THM-M-0721/check_obligation_tree.py` | 0 | Passed 18 obligations and 45 typed edges; denominator `375921a1...b92a`; root stayed M3 with both terminal packages M4. |
| Stream statement lines 1-94 and composition lines 11-26 to `lake env lean --trust=0 -T0 --stdin` | 0 | Exact declarations and conditional composition elaborated; `root_of_candidate_packages` reported exactly `[propext, Quot.sound]` and supplied no terminal-package inhabitant. |
| Scan owned Lean files for prohibited proof-device tokens | 1 expected | No `sorry`, `admit`, axiom, unsafe, `proof_wanted`, `sorryAx`, `native_decide`, or `implemented_by` token occurs in owned Lean files. |
| Search repository and pinned-mathlib Lean sources outside this dossier for exact packages and NP-completeness endpoints | 1 expected | No eligible endpoint or terminal-package implementation exists. |
| Ask trust-zero Lean to `#print Turing.TM2ComputableInPolyTime.comp` | 1 expected | Lean reported `Unknown constant`, confirming that `proof_wanted` created no checked declaration. |
| Trust-zero `#check` of the TM2 structure, identity implementation, and forgetful maps | 0 | All four declarations checked; none supplies either root child. |
| Search all target-history trees for `Proof.lean`, `proof-receipt.json`, or `check_proof.py` | 1 expected | No historical proof module, proof receipt, or proof checker exists under this target. |
| `timeout 240s python3 Stage1_Instances/THM-M-0721/check_anchor_audit.py` | 1 | Local checks reached immutable-source HTTPS replay; its first request timed out. No new external evidence is credited. |
| Query Lean/Lake/dependency identities and hash frozen inputs | 0 | Lean 4.29.0 at `98dc76e3...740`; Lake 5.0.0; mathlib `8a178386...ea95` tree `bdc39a31...c2b`; flt-regular `56161b6e...1a27` tree `32c9eace...c893`; dependency worktrees were clean; all recorded hashes matched. |
| Compare frozen proof inputs against prior base `69f012f9...dba` | 0 | All scoped proof inputs were byte-identical; only the prior recheck pair was integrated under this target. |
| `python3 -m json.tool` on the blocker JSON | 0 | The structured blocker artifact is valid JSON. |
| `git diff --check` on this blocker pair | 0 | No whitespace error was reported. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test is deliberately absent because the proof phase is blocked. |

## Reopen Condition

The master should first accept or repair the obligation-tree prerequisite, then split this oversized
item into dependency-legal children and append-only refine their exact Lean signatures. Workers can
then implement the eleven frozen packages without placeholders. The alternative is an immutable,
compatible Lean 4 proof already present in the pinned closure that can be exact-type checked,
transported to the frozen TM2 encodings, and provenance-audited without changing the dependency
lock; the current search found none.

This is fresh current-base, warm-cache, nonrelease blocker evidence only. It does not satisfy
`S56-M-0721-PROOF`, change scheduler state, close either terminal package or the root, or claim
audit completion, theorem completion, validation, release, receipt acceptance, or master
acceptance. Because the assigned proof phase is not genuinely complete,
`.stage1-worker-selftest.json` remains absent.
