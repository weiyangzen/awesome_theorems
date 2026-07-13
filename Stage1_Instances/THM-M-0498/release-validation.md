# THM-M-0498 release decision

Item `S56-M-0498-RELEASE` has the exact verdict **blocked**. The lifecycle
remains `planned`; the reconciled root vector remains `H3/M4/R4`; and both
`AUDIT-Z` and `THEOREM-Z` are blocked. `audit_complete=false`,
`theorem_complete=false`, and no receipt is accepted. Provisional `[_]` means
only that this negative release decision was implemented and self-tested; it
does not mean release, theorem completion, or master acceptance.

## Evidence reconciliation

The strongest machine evidence is partial and conditional. `Proof.lean`
checks a local exact-type wrapper over pinned mathlib's von Mangoldt
logarithmic-derivative theorem. `ObligationTree.lean` and the separately
written `Validation.lean` composition probe reach the exact frozen root only
when supplied the still-unproved analytic explicit-formula package. Therefore
they do not close the root or any whole frozen proof obligation. The
root-critical cut is `M0498-T-ANALYTIC`, including the Perron bridge, contour
shift and estimates, residue families, trivial-zero correction, and ordered
nontrivial-zero convergence. No checked inhabitant or realizability witness
for `NontrivialZeroEnumeration` exists either.

The authoritative validation dependency is only `[_]`. Its receipt is
provisional, `accepted=false`, `release_grade=false`, and contains no accepted
receipt or accepted obligation. Thus the first release workflow failure is
`S56-10.2-DEPENDENCY-ACCEPTANCE`. The next theorem gate is exact root kernel
closure, which fails at M4.

The intake-era `H2/M3/R3` projection predates the frozen statement and typed
graph. The later typed graph and validation receipt agree on the conservative
`H3/M4/R4` boundary and therefore govern this reconciliation. The source
phrase remains too broad to grant H0 without a primary-source edition,
pinpoint statement and assumptions, errata crosswalk, and independent review.
Required node-by-node R0 reconstruction and independent reader review are
also absent, so `AUDIT-Z` remains false independently of the open machine
root.

The validation phase observed only `propext`, `Classical.choice`, and
`Quot.sound` on the checked terminal, wrappers, and conditional compositions,
with no local prohibited proof device in the inspected boundary. That is
useful provisional evidence, not accepted complete provenance, foundation,
axiom, TCB, or SBOM closure.

The first intrinsic release failure is `S56-10.6-HERMETIC-COLD-BUILD`. The
available replay reuses the scheduler-provided shared warm `.lake` symlink,
which prior validation already classified as contaminated after an unrelated
`flt-regular` reconciliation left its compiled artifacts missing. There is no
immutable empty-cache cold build, offline archive restoration, complete
SBOM/license closure, two distinct signed clean-runner attestations,
independently implemented minimal verifier, protected critical mutation suite,
or build-twice deterministic content-addressed release bundle.

## Commands and results

Commands ran on 2026-07-14 from base revision
`bad90e2e2479d376609447202eb4f437789d0d11` (tree
`df3ade7b4d06057f8aac33369c3d69bd391aa05a`).

```text
$ python3 Docs/tools/check_stage1_standard.py
exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546
uniform-L0 Lean 4 targets passed

$ python3 scripts/stage1_target.py check
exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required

$ python3 scripts/stage1_target.py show THM-M-0498
exit 0; rank 258, planned lifecycle, legacy artifacts unaccepted,
theorem_complete=false

$ python3 -B Stage1_Instances/THM-M-0498/check_obligation_tree.py
exit 0; 15 obligations and 33 typed edges passed; root remains open M4 with
M0498-T-ANALYTIC as the analytic-package cut

$ set -euo pipefail
$ root=$PWD
$ tmp=$(mktemp -d /tmp/stage1-m0498-release-statement.XXXXXX)
$ out=$(mktemp /tmp/stage1-m0498-release-output.XXXXXX)
$ cleanup() { rm -rf "$tmp" "$out"; }
$ trap cleanup EXIT
$ cp Stage1_Instances/THM-M-0498/Statement.lean "$tmp/Statement.lean"
$ (cd Formalizations/Lean && LEAN_NUM_THREADS=1 lake env lean --trust=0 \
    --root "$tmp" "$tmp/Statement.lean") >"$out" 2>&1
$ sha256sum "$out"
$ wc -l <"$out"
$ rg -q 'def Stage1Instances\.THM_M_0498\.RiemannVonMangoldtTarget : Prop' \
    "$out"
exit 0; output SHA-256
d6d5184e00daeb31f3dc5aa1aa11821733217de35969d42e1e24b1fe8abc57c1;
40 output lines; the printed fully elaborated declaration begins
`def Stage1Instances.THM_M_0498.RiemannVonMangoldtTarget : Prop :=`.
The temporary directory and captured output were removed after the command.

$ python3 -B Stage1_Instances/THM-M-0498/check_release.py \
    --worker-packet .stage1-worker-selftest.json
exit 0; dependency nonacceptance, current H3/M4/R4 root, empty accepted sets,
false AUDIT-Z/THEOREM-Z, complete blocker cut, and prohibited-device scan agree

$ python3 -m json.tool \
    Stage1_Instances/THM-M-0498/release-decision.json >/dev/null
$ python3 -m json.tool .stage1-worker-selftest.json >/dev/null
exit 0 for both JSON documents

$ PYTHONPYCACHEPREFIX=/tmp/stage1-m0498-release-pycache \
    python3 -m py_compile Stage1_Instances/THM-M-0498/check_release.py
exit 0; checker syntax compiled outside the repository

$ rg -n '\b(sorry|admit|sorryAx|native_decide|implemented_by|extern)\b|^[[:space:]]*(axiom|constant|opaque|unsafe)\b' \
    Stage1_Instances/THM-M-0498 --glob '*.lean'
exit 1 with empty output; pass, because ripgrep returns 1 when no prohibited
source token is found

$ git diff --check -- Stage1_Instances/THM-M-0498 \
    .stage1-worker-selftest.json
exit 0; no whitespace errors
```

An additional independent attempt compiled the same temporary statement with
exit 0. Its subsequent `Validation.lean` invocation was interrupted before an
exit code was captured and is therefore not credited as a pass. No `lake
update`, `lake build`, dependency clone/fetch, or `.lake` mutation is part of
this release work.

The independent attempt first invoked `lake env lean --trust=0 -o
/tmp/thm-m-0498-release-review.IHhSRu/Statement.olean
/tmp/thm-m-0498-release-review.IHhSRu/Statement.lean`; it exited nonzero with
`input file ... must be contained in root directory (.../Formalizations/Lean/)`.
The corrected statement invocation added `--root` and exited 0. This failed
setup attempt supplies no evidence and is recorded only for completeness.

Retry requires placeholder-free closure of `M0498-T-ANALYTIC` and its frozen
supporting obligations, zero-enumeration realizability, accepted node-scoped
state and dependency receipts, H0/R0 review, complete provenance/foundation/
TCB evidence, and separately provisioned cold offline and independent release
validation culminating in a deterministic bundle and master reconciliation.
