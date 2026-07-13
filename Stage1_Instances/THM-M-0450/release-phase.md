# THM-M-0450 release reconciliation

Item: `S56-M-0450-RELEASE`

Base revision: `db3681c9e2616e7be7e8b5fde7fe48c77d6df6fe`

## Exact verdict

`blocked`. The lifecycle remains `planned`, the recorded root vector remains
`[H1, M3, R3]`, and both `audit_complete` and `theorem_complete` are false.
This worker accepts no receipt and makes no `AUDIT-Z`, `THEOREM-Z`, release, or
theorem-completion claim.

The first failed workflow gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`.
`S56-M-0450-VALIDATION` is only provisional `[_]` worker evidence, has
`release_grade=false`, and is not master accepted. The first mathematical
failure is `M0450-B-WEAKMW`; `M0450-H-HEIGHT` is also unproved. The first
release-input failure is `S56-RELEASE-IMMUTABLE-CLEAN-INPUT`, followed by
`S56-10.6-HERMETIC-COLD-BUILD`.

## Evidence reconciliation

There is real but deliberately narrow positive evidence. The exact canonical
statement elaborates. The frozen composer, ten local proof declarations, and a
separately written conditional probe replay with network denied. Their reported
axiom set is exactly `propext`, `Classical.choice`, and `Quot.sound`, and the
scoped local placeholder/unsafe scan passes. Selected pinned mathlib sources,
compiled imports, revision, tree, and license agree with the validation receipt.

None of that proves Mordell-Weil. Both exact-target declarations are functions
from universally quantified weak-Mordell-Weil and elliptic-height packages. No
checked term in this dossier supplies either package for the curves in the
theorem's scope. The frozen
graph consequently has `root_closed=false`, accepts no newly closed obligation,
and retains the cut `M0450-B-WEAKMW`, `M0450-H-HEIGHT`,
`M0450-X-TRANSPORT`, `M0450-X-SOURCE`, `M0450-X-PROVENANCE`, and
`M0450-X-TRUST`. The authoritative planned state therefore remains
`[H1, M3, R3]`.

`AUDIT-Z` fails independently: the dossier lacks accepted complete inventory
reconciliation, pinpoint primary-source premise and errata mapping, independent
`H0` source review, a complete obligation-anchored reconstruction, independent
`R0` review, and accepted full provenance/foundation/trust records.
`THEOREM-Z` additionally lacks an unconditional root proof, immutable clean
input, empty-cache cold build, offline restoration, complete TCB/SBOM/license
closure, two independent signed runners, an independently implemented minimal
verifier, protected adversarial CI, a deterministic content-addressed release
bundle, and master acceptance.

## Validation

Commands ran from the worker clone on 2026-07-14 in the Asia/Shanghai timezone.
The automation-provided pinned `.lake` symlink was reused without mutation. No
`lake update`, `lake build`, clone, fetch, checkout, dependency mutation, or
network request was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 unique targets and ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0450` | 0 | Rank 92 remains planned, L0/rework-required, and theorem-incomplete. |
| `env LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=UTC LEAN_NUM_THREADS=1 python3 -B Stage1_Instances/THM-M-0450/check_release.py` | 0 | Reconciled authoritative state and receipt hashes, replayed the recorded network-denied narrow validation, and derived the exact blocked decision. |
| `python3 -m json.tool` on the release spec, decision, receipt, and root self-test packet | 0 | All structured artifacts parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-thm-m-0450-release-pycache python3 -m py_compile Stage1_Instances/THM-M-0450/check_release.py` | 0 | The checker compiled without adding a generated owned file. |
| Scoped prohibited-construct scan over the target Lean modules | 1 (expected) | No match after comments were removed; no placeholder, custom axiom, unsafe/opaque/native/oracle, or external implementation escape was found. |
| `git diff --check -- Stage1_Instances/THM-M-0450 .stage1-worker-selftest.json` plus new-file hygiene checks | 0 | No whitespace, CR, NUL, or terminal-newline failure. |

The release checker copies the four proof-chain Lean modules to temporary
storage through the recorded validation runner, invokes the pinned Lean
executable in a Bubblewrap network namespace, validates exact axiom reports and
source hygiene, binds current authority and evidence digests, and confirms the
pinned mathlib checkout stays clean. Temporary outputs are removed.

Retry requires dependency-legal master acceptance and truthful graph/task
reconciliation, real proofs of the weak Mordell-Weil and height packages,
complete model transport, independently reviewed `H0`/`R0` and `AUDIT-Z`, full
provenance and trust closure, and a separately provisioned hermetic and
independent release run that closes every remaining gate.

Status boundary: this artifact self-tests only the negative release decision.
It supplies no accepted root proof, `M0`, `E0`, `E1`, `AUDIT-Z`, `THEOREM-Z`,
release, theorem completion, or master acceptance.
