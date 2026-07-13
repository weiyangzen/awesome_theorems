# THM-M-0043 release reconciliation

Item: `S56-M-0043-RELEASE`
Base revision: `59c86ca38b16fe4d3901ba66530aae4df0e881b0`

## Exact verdict

`blocked`. The lifecycle remains `planned`, the accepted root vector remains `[H1, M3, R4]`, and
both `audit_complete` and `theorem_complete` are false. This worker accepts no receipt and makes no
release or theorem-completion claim.

The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`. The validation dependency is provisional
`[_]` worker evidence with `accepted=false` and `release_grade=false`; it has not been
dependency-ordered master-accepted. The first release-specific failure is
`S56-10.6-HERMETIC-COLD-BUILD`.

## Evidence reconciliation

There is substantive but provisional positive evidence. The exact finite complex normal-matrix
target, its frozen composer, the local exact-root proof, and a same-worker duplicate route replayed at
Lean trust level zero. The five proof/differential declarations report sorry-free, the frozen
composer passes the same prohibited-construct scan, and all six observed axiom reports are exactly
`propext`, `Classical.choice`, and `Quot.sound`.

That evidence cannot promote accepted state. The proof receipt claims 23 closed proof-route IDs,
but its three composition certificates map only 22. `M0043-T-OPERATOR-DECOMP` is therefore an
uncertified closure claim and the validation receipt correctly excludes it. The authoritative
instance and frozen graph also retain no accepted receipt, `[H1, M3, R4]`, `root_closed=false`, and
the open cut recorded in `release-decision.json`. Under the fail-closed conflict rule, this weaker
accepted authority wins over provisional local kernel evidence.

`AUDIT-Z` fails separately: pinpoint H0 source fidelity and independent R0 review are absent, as
are accepted provenance, foundation, trust, and workflow records. `THEOREM-Z` additionally lacks an
immutable clean snapshot, empty-cache network-isolated cold build, offline restoration archive,
complete transitive TCB/SBOM/license closure, two independent signed runners, an independently
implemented minimal verifier, protected adversarial CI, a repeatable deterministic bundle, and
master acceptance.

## Commands and results

Commands ran from the worker clone on 2026-07-13 (Asia/Shanghai). The automation-provided pinned
`.lake` symlink was reused without mutation. No update, build, fetch, clone, dependency mutation,
or network operation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0043` | 0 | Rank 1083 remains planned, L0/rework-required, and theorem-incomplete. |
| `python3 -B Stage1_Instances/THM-M-0043/check_release.py` | 0 | The exact root, frozen composition, and duplicate route replayed; the checker derived the blocked unchanged release decision and preserved the 22/23 certificate gap. |
| `python3 -m json.tool` on all five owned release JSON artifacts plus `.stage1-worker-selftest.json` | 0 | Every structured artifact parsed as JSON. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0043-release-pycache python3 -m py_compile Stage1_Instances/THM-M-0043/check_release.py` | 0 | The release checker compiled outside the repository tree. |
| prohibited Lean construct scan over `Statement.lean`, `AnchorAudit.lean`, `ObligationTree.lean`, `Proof.lean`, and `Validation.lean` | 1 | Expected no-match result with empty output; no placeholder, bodyless axiom, unsafe declaration, oracle, or native shortcut. |
| `git diff --check -- Stage1_Instances/THM-M-0043 .stage1-worker-selftest.json` plus new-file whitespace checks | 0 / expected 1 with empty diagnostics | No whitespace diagnostics. |

The release checker binds current authority and evidence hashes, verifies the dependency and
authoritative negative state, copies the four proof-chain Lean modules to a temporary directory,
runs the pinned Lean executable with trust level zero, verifies sorry/axiom output and source
hygiene, checks the exact changed-path handoff, and confirms the pinned mathlib worktree is clean
before and after replay. Temporary outputs are removed.

Retry requires dependency-legal master acceptance and structured-state reconciliation, repair or
withdrawal of the uncertified `M0043-T-OPERATOR-DECOMP` claim, accepted H0/R0 and trust evidence,
and a separately provisioned hermetic and independent release run closing every remaining gate.
This artifact self-tests only the truthful negative release decision.
