# THM-M-0451 release-phase reconciliation

Item: `S56-M-0451-RELEASE`. Base revision:
`bbe7a5bd1c72a12f3f43b79b6a4cac3f62d2085a`.

## Exact verdict

`blocked`. Lifecycle remains `planned`, the accepted root vector remains
`[H1, M3, R3]`, and both `audit_complete` and `theorem_complete` are false.
This worker accepts no receipt and makes no theorem-completion or release-grade
claim.

The first failed workflow gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`:
`S56-M-0451-VALIDATION` is only provisional `[_]` evidence with
`accepted=false` and `release_grade=false`. The exact root independently fails
at `M0451-APPROX.kernel_closure`; `M0451-ZERO-TORSION` is also open.

## Evidence reconciliation

The exact statement, conditional engine composition, eleven partial
proof-phase declarations, recursive sorry probes, and a separately written
conditional adapter elaborate at trust level zero with network denied for each
Lean subprocess. All thirteen full axiom reports contain exactly `propext`,
`Classical.choice`, and `Quot.sound`. These declarations are substantive but
nonclosing: the engine has no inhabitant and the accepted graph closes no
frozen obligation.

The accepted cut therefore remains the graph's eleven-node cut, not the
smaller cut proposed by the unaccepted proof receipt. In particular, no body
establishes the uniform elliptic height estimates or the implication from zero
canonical height to torsion. The graph also models one `M0451-APPROX` estimate
while `Proof.lean` consumes distinct doubling and approximate-parallelogram
bounds; that bridge is not authoritatively reconciled.

`AUDIT-Z` additionally fails because the source calls unscaled
`Height.logHeight` absolute although the pinned number-field formula has total
place weight `[K:Q]`. The exact Silverman normalization, possible degree
factor, fixed primary-source/errata mapping, and independent H0/R0 reviews are
unresolved.

Release assurance lacks an immutable clean input, accepted foundation and
complete transitive provenance/TCB/SBOM/license closure, a cold empty-cache
offline-restorable build, two independently provisioned signed runners, an
independently implemented minimal verifier, protected adversarial CI, and a
deterministic build-twice bundle. The automation-provided `.lake` link is a
shared warm cache and is used only for explicitly nonrelease replay.

## Commands and results

Commands ran from the worker clone. No `lake update`, `lake build`, clone,
fetch, network request, or dependency mutation was performed.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0451` | 0 | Rank 93 remains planned, rework-required, and theorem-incomplete. |
| `cd Formalizations/Lean && env LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=UTC LEAN_NUM_THREADS=1 lake env lean --trust=0 -t0 ../../Stage1_Instances/THM-M-0451/Statement.lean` | 0 | Exact target re-elaborated with the pinned toolchain. |
| `python3 Stage1_Instances/THM-M-0451/check_anchor_audit.py` | 0 | Four candidates and pinned source hashes agreed; root remains M3. |
| `python3 Stage1_Instances/THM-M-0451/check_obligation_tree.py` | 0 | Seventeen obligations and 44 typed edges passed with the root open. |
| `env LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=UTC LEAN_NUM_THREADS=1 python3 -I -B Stage1_Instances/THM-M-0451/check_release.py` | 0 | Current-snapshot network-isolated narrow Lean replay and fail-closed release reconciliation passed. |
| `python3 -m json.tool` on the release spec, decision, receipt, and worker packet | 0 | Structured artifacts parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0451-release-pycache python3 -m py_compile Stage1_Instances/THM-M-0451/check_release.py` | 0 | Checker syntax compiled outside the repository. |
| `rg -n '^\s*(sorry\|admit\|axiom)(\s\|$)' Stage1_Instances/THM-M-0451 -g '*.lean'` | 1 | Expected no-match result; no prohibited Lean declaration was found. |
| `git diff --check -- Stage1_Instances/THM-M-0451 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The historical validation checker is bound to base
`a1a7e939e58f103f5ff5d23af51437fa8658aa04` and its then-open scheduler row;
it correctly rejects current HEAD before replay. Release preserves its receipt
unchanged and performs a new direct current-snapshot narrow replay instead of
rewriting the historical validator.

Retry requires dependency-legal master acceptance, exact placeholder-free
closure of `M0451-APPROX` and `M0451-ZERO-TORSION` through the frozen root,
normalization and structured-authority reconciliation, accepted H0/R0 and
trust/provenance records, then the complete cold/offline, supply-chain,
independent-verifier, CI, deterministic-bundle, and master-release protocol.

Status boundary: this artifact self-tests only the truthful negative release
decision. It grants no `M0`, `E0/E1`, `AUDIT-Z`, `THEOREM-Z`, release,
theorem-completion, authoritative-state, or master-acceptance credit.
