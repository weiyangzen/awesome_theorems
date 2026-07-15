# THM-M-0721 proof recheck at `4d389eb4` (slot47)

Item: `S56-M-0721-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T16:54:56+08:00`

Base revision: `4d389eb47e043f6f44925a418baee0d034f764ba`

Base tree: `64faabd76665273032b8cb1554b90655b5c94256`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact root
`Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage`. The proof item stays `[ ]`; lifecycle stays
`planned`; the root vector stays `[H1, M3, R4]`; audit completion and theorem completion stay
false.

The checked declaration `root_of_candidate_packages` is conditional composition. It consumes, but
does not construct, the two immediate root packages:

- `M0721-T-SAT-IN-NP`: a faithful binary SAT encoding, correct certificate verifier, polynomial
  certificate bound, and bundled polynomial-time TM2 verifier;
- `M0721-T-UNIVERSAL-HARDNESS`: arbitrary frozen-`InNP` verifier normalization, Cook-Levin
  tableaux, both correctness directions, and a bundled polynomial-time TM2 reduction.

Eleven frozen SAT and Cook-Levin obligations remain open. Their registry entries freeze planned
prose fingerprints rather than exact Lean declaration types; the only exact open terminal
interfaces are `CandidateMembership candidate` and `CandidateHardness candidate`. An append-only
registry refinement is therefore required before concrete leaf bodies can receive proof credit.

Pinned mathlib provides the `TM2ComputableInPolyTime` substrate and identity implementation, but no
NP, SAT-language, or Cook-Levin endpoint. Its apparent polynomial-time composition declaration is
source-level `proof_wanted`; trust-zero Lean reports the would-be constant as unknown. Repo-local,
pinned-mathlib, and target-history searches found no implementation of either terminal package.
The immutable anchor audit retains one supporting-only candidate and two headline candidates that
are placeholder-dependent or contract-incompatible, so none can be imported or transported to the
exact target.

There is no definitional shortcut. Empty, universal, identity, singleton, fixed-source, and
classical-choice witnesses do not produce the universally quantified polynomial-time reductions.
A reduction branching on `source input` would assume a polynomial-time decider not supplied by
arbitrary verifier-based `InNP`; a universal encoded-verifier language still requires the missing
machine serialization, polynomial-time simulation, and correctness transports.

The first failed gate is `M0721-N-SAT-ENCODING`. Because the positive proof phase is incomplete, no
`Proof.lean`, proof receipt, or `.stage1-worker-selftest.json` is emitted.

## Validation

All commands ran in this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink points to canonical pinned artifacts and was reused read-only.
No dependency update, build, clone, fetch, checkout, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all; readlink -f Formalizations/Lean/.lake` | 0 | Base `4d389eb47e043f6f44925a418baee0d034f764ba`, tree `64faabd76665273032b8cb1554b90655b5c94256`; initially only the automation-provided `.lake` symlink was untracked. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0721` | 0 | Rank 578; `planned`; L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| `LEAN_NUM_THREADS=1 timeout 600s python3 Stage1_Instances/THM-M-0721/check_statement.py` | 0 | Exact expression hash `758b1033903c92b231a24ae3fb5e01e0bbb0d6fdb0bc41f809c062deb7b4b204` matched; all four structural mutations were distinguished. |
| `timeout 180s python3 Stage1_Instances/THM-M-0721/check_obligation_tree.py` | 0 | Passed 18 obligations and 45 typed edges; denominator `375921a1792cc56322b0f0f3d241a5fa10e02345a66a9f007554978cc932b92a`; root remained M3 and both terminal packages M4. |
| `timeout 180s python3 Stage1_Instances/THM-M-0721/check_anchor_audit.py` | 0 | Local pins/hashes and all three immutable external candidate records matched; root classification remained M2 and no eligible proof body was supplied. |
| From `Formalizations/Lean`, stream exact statement and composition declarations to `LEAN_NUM_THREADS=1 timeout 300s lake env lean --trust=0 -t0 --stdin` | 0 | Exact declarations and conditional composition elaborated; `root_of_candidate_packages` reported exactly `[propext, Quot.sound]` and supplied no terminal-package inhabitant. |
| Scan owned Lean files for prohibited proof-device command tokens | 1 expected | No `sorry`, `admit`, axiom, unsafe/oracle, `proof_wanted`, `sorryAx`, `native_decide`, or `implemented_by` token occurs in owned Lean files. |
| Search other repo-local and pinned-mathlib Lean sources for the exact root/packages and NP-completeness endpoints | 1 expected | No eligible endpoint or terminal-package implementation exists outside this dossier. |
| Ask trust-zero Lean to `#print axioms Turing.TM2ComputableInPolyTime.comp` after importing its module | 1 expected | Lean reported `Unknown constant`, confirming that source-level `proof_wanted` created no checked declaration. |
| Search target Git history for `Proof.lean`, a proof receipt, or `check_proof` | 1 expected | No historical proof artifact exists under this target. |
| Inspect Lean/Lake/mathlib/flt-regular identities and hash frozen inputs | 0 | Lean 4.29.0 at `98dc76e3...740`, Lake 5.0.0, mathlib `8a178386...ea95` tree `bdc39a31...c2b`, and flt-regular `56161b6e...1a27` tree `32c9eace...c893`; dependency worktrees were clean and all recorded hashes matched. |

## Reopen Condition

Append-only refine exact Lean signatures and implement the eleven frozen SAT and Cook-Levin
packages without placeholders. Alternatively, identify an immutable compatible Lean 4 proof
already present in the pinned closure and exact-type check, transport, and provenance-audit it
without changing the dependency lock.

This is fresh current-base, warm-cache, nonrelease blocker evidence only. It does not satisfy
`S56-M-0721-PROOF`, change scheduler state, close either terminal package or the root, or claim
audit completion, theorem completion, validation, release, receipt acceptance, or master
acceptance. Because the assigned phase is not genuinely self-tested complete,
`.stage1-worker-selftest.json` remains absent.
