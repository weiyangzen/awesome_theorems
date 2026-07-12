# THM-M-0474 release reconciliation

Item: `S56-M-0474-RELEASE`
Base revision: `2cf42e232e732b5d915dc077d91524b386861821`

## Exact verdict

`blocked`. The lifecycle remains `planned`, the accepted root vector remains `[H1, M3, R4]`, and
both `audit_complete` and `theorem_complete` are false. This worker accepts no receipt and makes no
release or theorem-completion claim.

The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`. The validation receipt is provisional
worker evidence, explicitly has `release_grade=false`, and has not been master accepted. Even if
that dependency were accepted, the accepted authority would still fail `THEOREM-Z`: the instance
and frozen graph retain an open `M3` root, while H0, R0, provenance, foundation, and TCB acceptance
remain absent.

## Evidence reconciliation

The exact natural-number statement, direct pinned mathlib wrapper, and full frozen composition
route replay under the pinned Lean toolchain. A separately written local route through Euler's
totient theorem also replays without importing `Proof` or `ObligationTree`. The proof declarations
are sorry-free, and every observed axiom report is contained in `propext`, `Classical.choice`, and
`Quot.sound`. This is substantive provisional exact-root evidence, but it ran in the same worker
clone with the shared warm dependency cache. It is neither accepted M0-W/E1 nor independent release
verification.

The weaker structured authority therefore wins. `instance.json` and `typed-graphs.json` retain no
accepted receipts, `[H1, M3, R4]`, and an open root. Primary-source fidelity remains H1 because the
catalog omits the prime, coprimality, and domain premises and no pinpoint source/errata review has
been accepted. Readability remains R4 because no complete independently reviewed reconstruction is
accepted.

Release also lacks an immutable clean snapshot, empty-cache network-denied cold build, offline
restoration archive, complete declaration/TCB and SBOM/license closure, two separately provisioned
signed attestations, an independently implemented minimal verifier, protected adversarial CI, a
build-twice deterministic content-addressed bundle, and master acceptance.

## Commands and results

Commands ran from the repository root on 2026-07-13 local time. The pre-existing untracked
`Formalizations/Lean/.lake` link was reused without mutation. No update, build, fetch, clone, or
other dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework_required. |
| `python3 scripts/stage1_target.py show THM-M-0474` | 0 | Rank 938 remains planned and theorem-incomplete. |
| `python3 Stage1_Instances/THM-M-0474/check_release.py` | 0 | The exact statement, 18 proof declarations, and 3 differential declarations replayed; the checker derived the blocked unchanged terminal decision. |
| `for f in Stage1_Instances/THM-M-0474/*.json .stage1-worker-selftest.json; do python3 -m json.tool "$f" >/dev/null; done` | 0 | Every structured artifact parsed as JSON. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0474-release-pycache python3 -m py_compile Stage1_Instances/THM-M-0474/check_release.py` | 0 | The release checker compiled outside the repository tree. |
| `rg -n '\b(sorry\|admit\|sorryAx\|implemented_by\|native_decide\|extern\|opaque)\b\|^[[:space:]]*(axiom\|unsafe)\b' Stage1_Instances/THM-M-0474/{Statement,ObligationTree,Proof,Validation}.lean` | 1 | Expected no-match result: no placeholder, bodyless axiom, unsafe declaration, oracle, or native shortcut. |
| `git diff --check -- Stage1_Instances/THM-M-0474 .stage1-worker-selftest.json` | 0 | No tracked whitespace errors. |
| `git diff --no-index --check /dev/null "$f"` for each new release artifact and the root handoff | 1 per file, empty diagnostics | Expected new-file diff status with no whitespace diagnostics. |

`check_release.py` copies the four Lean modules to a temporary directory, compiles the local import
chain with `lake env lean`, checks the sorry/axiom output counts, binds the pinned toolchain,
mathlib tree, source and olean hashes, verifies the provisional receipt chain and authoritative
negative state, and confirms the exact changed-path handoff. Temporary outputs are removed and the
pinned mathlib checkout is clean before and after the replay.

Retry requires dependency-legal master acceptance and structured-state reconciliation, accepted
H0/R0 and trust evidence, and a separately provisioned hermetic and independent release run closing
every remaining gate. This artifact self-tests only the truthful negative release decision.
