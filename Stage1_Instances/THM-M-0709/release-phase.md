# THM-M-0709 release-phase reconciliation

Item: `S56-M-0709-RELEASE`. Base revision:
`ab6974ae3bcabe677e7138ff057a7c005aac12d4` (tree
`c640af240d44f02c83a29dfa2f985f601a0dfcc2`).

## Exact verdict

The release verdict is `blocked`. Lifecycle remains `planned`; the accepted
root vector remains `[H1, M4, R3]`; and both `audit_complete` and
`theorem_complete` are false. No receipt or frozen obligation is accepted.
The graph/proof view `[H1, M3, R3]` is provisional only and does not promote
the accepted instance state.

The first workflow failure is `S56-10.2-DEPENDENCY-ACCEPTANCE` at
`dependency.S56-M-0709-VALIDATION.master_acceptance`. The validation receipt is
only provisional worker evidence, explicitly has `accepted=false` and
`release_grade=false`, and has no dependency-ordered master acceptance.

## Evidence reconciliation

The exact target is binary structured PCP undecidability:
`Stage1Instances.THM_M_0709.PostCorrespondenceUndecidable`, definitionally
`not ComputablePred HasSolution`. The proof phase checks a generic many-one
pullback and the pinned fixed-input halting theorem, then reaches the exact
root only from an explicit `HaltingPredicate input <=0 HasSolution` premise.
It does not construct that reduction. The provisional mathematical cut remains
`M0709-C-MACHINE`, `M0709-C-MPCP`, `M0709-T-MPCP-PCP`,
`M0709-N-BINARY`, and `M0709-T-REDUCTION`.

The historical validation receipt records a network-isolated trust-zero narrow
replay, the axiom set `propext`, `Classical.choice`, and `Quot.sound`, and an
observed closure of 4,743 declarations across 163 modules with no bodyless
nonaxiom or unsafe declaration. This is useful provisional observation, not
accepted root closure or complete provenance/foundation/TCB evidence. Its
checker is bound to validation base `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`
and that phase's worker packet, so release does not misrepresent it as a current
recipe.

`AUDIT-Z` is separately blocked, not merely because the proof is open. Post's
1946 article is only a source locator: the exact text and hash, theorem passage,
computability convention, alphabet and modified-to-ordinary-PCP boundary,
errata, node crosswalk, and independent H0 review remain absent. No independent
R0 reconstruction is accepted. The intake instance, local all-open task
projection, frozen graph with empty evidence links, provisional receipts, and
public prose are not fully reconciled.

Release also lacks immutable clean input, a usable complete package closure,
an empty-cache network-denied cold build, offline restoration, accepted full
provenance/foundation/TCB and SBOM/license archives, two signed independently
provisioned runners, an independently implemented minimal verifier, protected
adversarial CI, and a deterministic twice-built content-addressed bundle. The
automation `.lake` link exposes shared warm state, and its unrelated
`flt-regular` checkout has no resolvable `HEAD`; this worker did not repair,
fetch, build, or update it.

## Commands and exact results

Commands ran from the worker clone on 2026-07-15 (`Asia/Shanghai`). No
`lake update`, `lake build`, dependency clone, dependency fetch, or `.lake`
mutation was performed.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and exactly 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0709` | 0 | Rank 750; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| `python3 -I -B Stage1_Instances/THM-M-0709/check_obligation_tree.py` | 0 | 18 obligations and 81 typed edges passed; root remained open M3. |
| `python3 -I -B Stage1_Instances/THM-M-0709/check_release.py` | 0 | Current authority, hashes, historical dependency boundary, smallest `lake env lean --trust=0` statement replay, and blocked terminal decisions passed. |
| `for f in Stage1_Instances/THM-M-0709/release-{spec,decision,receipt}.json .stage1-worker-selftest.json; do python3 -m json.tool "$f" >/dev/null; done` | 0 | Every release JSON artifact and the worker packet parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0709-release-pycache python3 -m py_compile Stage1_Instances/THM-M-0709/check_release.py` | 0 | Checker syntax compiled outside the repository. |
| `git diff --check -- Stage1_Instances/THM-M-0709 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The smallest Lean replay is performed by the release checker. It invokes
`lake env lean --trust=0` from the pinned mathlib workspace and extends
`LEAN_PATH` only with the already present canonical compiled roots needed to
work around the unrelated broken top-level package closure. This narrow warm
replay is explicitly nonrelease evidence.

## Status boundary

This packet self-tests only a truthful negative release decision. Proposed
`[_]` means the release-phase reconciliation is ready for master review, not
that the theorem or release is accepted. It grants no `H0`, accepted `M0`,
`E0/E1`, `R0`, `AUDIT-Z`, `THEOREM-Z`, theorem-completion, release-grade, or
master-acceptance credit.
