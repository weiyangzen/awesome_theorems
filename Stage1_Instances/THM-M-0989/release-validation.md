# THM-M-0989 release-phase reconciliation

Item: `S56-M-0989-RELEASE`

Base revision: `d9006cb9119e9419f99f143c24edb5b15d0569d8`

Decision time: `2026-07-15T02:43:04+08:00`

## Exact verdict

`blocked`. The lifecycle remains `planned`; the accepted root vector remains
`[H2, M3, R4]`; accepted receipt IDs remain empty; and both `audit_complete` and
`theorem_complete` are false. Neither `AUDIT-Z` nor `THEOREM-Z` is accepted.

The first workflow gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`, specifically
`dependency.S56-M-0989-VALIDATION.master_acceptance`. The validation receipt is
provisional `[_]` worker evidence with `accepted=false`, `release_grade=false`,
and no content-addressed release evidence. Its own nested first failure is proof
master acceptance.

## Evidence reconciliation

There is real provisional machine evidence for the exact frozen Lean target.
The current Lean-subprocess-network-isolated replay elaborates all six proof modules and the
separately written final Levy composition with `--trust=0`. It checks 25 axiom
reports as exactly `propext`, `Classical.choice`, and `Quot.sound`; five
parser-aware sorry probes pass; and the 53,251-declaration closure across 1,748
modules contains no unexpected bodyless or unsafe declaration. This supports a
warm-cache `M0-L` candidate, not accepted `M0-L` or `E0`.

The recorded validation recipe is stale at the release snapshot: its Python
checker requires the prior validation worker packet and HEAD `64ac6166...`,
while this release base is `d9006cb9...`. The release checker therefore binds
that receipt and checker as historical evidence, confirms the recorded recipe
fails, and separately invokes the smaller live `check_validation.sh` replay.

The authoritative graph still predates proof closure. It records root
`H2/M3/R4`, `root_closed=false`, no root evidence ID, and the historical cut
`{M0989-S-MEAS, M0989-T-CHARFUN}`. That is a stale authority cut, not a claim
that the current local proof lacks those packages. `intake.json` and `README.md`
also say `R3`, conflicting with the graph and proof/validation receipts at
`R4`; the weaker `R4` controls until accepted public-state reconciliation.

`AUDIT-Z` is independently blocked. The canonical expression fingerprint is
null. The broad source metadata does not select the forward normalized
triangular-array variant over converse/Feller variants, and no accepted
pinpoint `H0` mapping or independent review exists. There is likewise no
independent `R0`, accepted foundation profile, complete transitive
provenance/TCB/SBOM, immutable empty-cache cold/offline reproduction, two
distinct signed runners, independent minimal verifier, protected adversarial
CI, or deterministic release bundle. The outer release checker itself is not
network-namespaced, so whole-recipe network denial also fails closed.

## Commands and results

Commands ran from this worker clone. No `lake update`, `lake build`, dependency
clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0989` | 0 | rank 269, planned, L0/rework-required, theorem incomplete |
| `python3 Stage1_Instances/THM-M-0989/check_obligation_tree.py` | 0 | 15 obligations and 32 typed edges passed; denominator `c5d0b41c...dc15`; frozen root remains open `M3` |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-0989/Statement.lean` | 0 | exact frozen statement elaborated with no output |
| `bash Stage1_Instances/THM-M-0989/check_proof.sh` | 0 | six modules elaborated with `--trust=0`; 20 declaration axiom reports passed |
| `bash Stage1_Instances/THM-M-0989/check_validation.sh` | 0 | network-isolated exact-root/final-composition replay; 25 axiom reports, five sorry-free reports, 53,251 declarations/1,748 modules, no unsafe or unexpected bodyless declarations |
| recorded `python3 -I -B Stage1_Instances/THM-M-0989/check_validation.py` | 1 (expected stale evidence) | requires the absent prior validation packet and is also hard-bound to HEAD `64ac6166...` |
| `python3 -I -B Stage1_Instances/THM-M-0989/check_release.py` | 0 | manifest, DAG, hashes, receipts, stale authority, release cut, source hygiene, live narrow Lean replay, and blocked terminal decision passed |
| JSON parsing, Python compilation to `/tmp`, scoped prohibited-construct scan, and `git diff --check` | 0 | release artifacts parsed/compiled; no active prohibited mechanism or whitespace error |

## Retry boundary

First obtain dependency-legal acceptance and reconcile the canonical expression
fingerprint, chosen source variant, typed graph, public state, H0/R0, and full
foundation/provenance/TCB inventory. A separately provisioned release lane must
then perform clean cold offline reproduction, independent attestations and
minimal-verifier/CI checks, and deterministic bundle assembly.

This release node is self-tested only as a truthful negative reconciliation.
It grants no accepted proof, audit, theorem-completion, release, or master credit.
