# THM-M-0424 Lean 4 anchor audit

Audit date: 2026-07-12. This inventory is scoped to the frozen declaration
`Stage1Instances.THM_M_0424.BrauerGroupStatement` and does not broaden it to an
Azumaya group over general commutative rings or weaken it to quotient equality.

## Immutable mathlib result

The installed mathlib checkout is clean at commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`, using
`leanprover/lean4:v4.29.0`. The manifest, source blobs, file digests, and license
are recorded in `anchor-audit.json`. No dependency fetch, update, build, or
other `.lake` mutation was performed.

`Mathlib.Algebra.BrauerGroup.Defs` supplies the exact `CSA`,
`IsBrauerEquivalent`, `Brauer.CSA_Setoid`, and `BrauerGroup` definitions used by
the target. It is not a proof candidate for the target: its first explicit TODO
is to prove that the quotient is an abelian group under tensor product. The file
has no `CommGroup (BrauerGroup K)` instance and no construction matching
`BrauerGroupLawData`.

The narrow kernel probes in `AnchorAudit.lean` verify four useful boundaries:

* quotient equality is exactly the defining stable matrix equivalence;
* finite Wedderburn-Artin gives a matrix-over-division-algebra normal form;
* Brauer equivalence implies Morita equivalence using matrix Morita equivalence;
* the neighboring Azumaya API proves the base and matrix cases.

None packages `TensorProduct K A B` as a `CSA`, descends that construction with
all laws, or proves the base-field and opposite-algebra unit/inverse equations.
The legacy `S1_M_078` file checks the same supporting routes but leaves its group
data structure uninhabited, so it receives no independent proof credit.

## External Lean 4 search

All installed pinned non-mathlib Lean dependencies were searched for
`BrauerGroup`, `IsBrauerEquivalent`, "Brauer group", and "Brauer equivalence";
no hit was found. In particular, pinned `flt-regular` at
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27` contains no candidate.

The bounded public search found no GitHub repository for `brauer lean4`.
Authenticated GitHub code search was unavailable, the unauthenticated API was
rate-limited, and grep.app returned HTTP 429. Consequently the audit records no
credible external proof body, but it does not claim exhaustive global absence.
There is no project URL, immutable revision, module, declaration, and proof body
to pin or import.

## Classification boundary

The exact target remains `[H1, M3, R3]`: its statement and defining interfaces
exist, while no candidate inhabits the root. The next phase should decompose the
missing tensor-product CSA construction, congruence and quotient descent, unit,
opposite inverse, associativity, and commutativity. This bounded anchor phase is
self-tested, but `audit_complete=false` and `theorem_complete=false`; source,
proof, trust, validation, release, and master-acceptance gates remain open.

## Validation record

Base revision: `7c33ee20ed10b1c1b2a0ec7dc1daed1dc304ac4e`.

| Command | Exit/result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0; 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0424` | 0; rank 78, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0424/check_anchor_audit.py` | 0; six candidates classified, immutable mathlib sources verified, root retained at M3 |
| `python3 -m json.tool Stage1_Instances/THM-M-0424/anchor-audit.json` | 0; structured audit parsed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0424/AnchorAudit.lean` | 0; four supporting boundary probes elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0424/Statement.lean` | 0; frozen exact target still elaborated |
| `git diff --check -- Stage1_Instances/THM-M-0424 .stage1-worker-selftest.json` | 0; no whitespace errors |

Known limitations are the bounded public-code-search failures and all downstream
gates listed above. They do not turn the definition anchors into proof evidence.

An initial combined validation command was launched from `Formalizations/Lean`
with repository-root-relative Python paths; those Python checks failed with
file-not-found, and the first Lean attempt also exposed an invalid local-module
import. The Python checks were rerun from the repository root, the probe was
made self-contained with its direct mathlib import, and both final Lean commands
above exited 0. These were invocation/probe defects, not candidate proof failures.
