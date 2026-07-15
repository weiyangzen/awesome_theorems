# Current-base proof recheck

Item: `S56-M-1419-PROOF`

Theorem: `THM-M-1419`

Base revision: `350285c48208616b6e3ad74154d9183d16523cfa`

Base tree: `c4edebc115ec954e4940ed5faaa3ffacd4e56091`

Attempt date: `2026-07-15` (`Asia/Shanghai`)

Worker: Stage1 rev-5.6 automation clone `slot61`

## Verdict

`blocked`; the assigned proof phase remains `[ ]`. No proof body, axiom,
placeholder, weakened theorem, dependency, frozen authority artifact, receipt,
or task state was added or changed. Because the phase is not genuinely
self-tested, no `.stage1-worker-selftest.json` is emitted.

## First failed gate

Exact-target fidelity fails at `M1419-S-INTERFACE`. The frozen target quantifies
a plain equivalence `T : Omega Equiv Omega`. Its `Ergodic T mu` hypothesis
supplies `Measurable T`, but no frozen hypothesis supplies
`Measurable T.symm`. Pinned mathlib's `Ergodic.symm` instead requires
`T : Omega MeasurableEquiv Omega`, whose structure stores forward and inverse
measurability separately.

This is material rather than a missing convenience lemma. A countermodel is the
two-sided fair Bernoulli shift equipped only with the future-coordinate sigma
algebra and the measurable triangular cocycle
`A(omega) = [[4, 0], [omega_0, 1]]`. Forward measurability, preservation,
ergodicity, invertibility, and both bounded moment hypotheses hold. Any claimed
measurable equivariant splitting would force its fast line to be
`span (1, u(omega))`, with
`u(T omega) = (u(omega) + omega_0) / 4`. Backward iteration identifies `u`
almost everywhere with `sum_(r >= 1) 4^(-r) omega_(-r)`, which depends on past
coordinates and is not measurable in the future sigma algebra. This run does
not include a kernel formalization of that countermodel, so the machine debt
remains `M3`; it does establish why importing a theorem with a bimeasurable base
cannot prove the frozen proposition.

The prose freeze is inconsistent with the Lean expression: `statement.md` and
`source-statement-crosswalk.md` say inverse measurability was retained, while
the Lean target retains only measurability of the matrix inverse, not the base
inverse. A proof worker cannot silently add the missing premise. The statement
must first be reopened, corrected to use a measurable equivalence or an
explicit inverse-measurability hypothesis, and accepted with a new expression
fingerprint and obligation-registry version.

## Candidate update

During this attempt a collaborative read-only scratch port reached all 62
ordered transitive modules and produced
`ErgodicTheory/TwoSided/SplittingAssembly.olean` under Lean 4.29. Its
terminal declaration `ErgodicTheory.oseledets_splitting` reports only
`propext`, `Classical.choice`, and `Quot.sound`. This is useful discovery, but
it receives no proof credit here:

- the scratch tree is outside the repository and pinned Lake closure;
- 26 of its 62 transitive sources differ from upstream due compatibility edits;
- it has not been vendored, provenance-reconstructed, or cleanly replayed as a
  target-owned immutable dependency;
- the theorem requires `T : X MeasurableEquiv X`, pointwise `Measurable A`, and
  pointwise nonzero determinant, unlike the frozen assumptions;
- exact transports remain for AE representatives, Pi versus Euclidean norms,
  measurable-subspace APIs, direct-sum and finrank facts, cocycle products,
  growth limits, and output indexing.

In particular, the 62-module closure defines a measurable subspace through
orthogonal-projection matrices and contains no checked bridge to the target's
`Metric.infDist` predicate on an arbitrary measurable base. A nearby upstream
`infDist` result assumes additional Polish/Borel structure, so it cannot be
silently applied to this target.

The terminal source is byte-identical to upstream commit
`ed3fa6b8a30594eeb791160563942ba115581aa0` and has SHA-256
`e47ced0d869724a402369352f0ac0bd1f4bb8e57cfd7cefc2a44fa071c6e9407`.
The scratch terminal olean has SHA-256
`3f3165b7a9a58ab36f769fa03d68c4d520fec734dc45a7672c6733a3d3067197`;
the ordered 62-olean aggregate hash is
`08acecc22f5c8dd7098eb48d7c70a737c2f2f070938a92982f5ea3b25cf6227f`.
Those hashes identify non-credit scratch evidence, not a repository proof body.

## Frozen architecture

The obligation-tree validator still passes 14 obligations and 41 typed edges
with denominator
`ad6916330e2b03519a1c387301c0b7a418ed53c487c42d86691de96e56639599`,
but explicitly leaves the root at `M3`. Twelve of thirteen machine-required
obligations have no terminal proof-body ID. The only recorded Lean composer,
`target_of_construction_package`, consumes a package definitionally equal to
the entire root, so it is a conditional identity wrapper and does not consume
the four frozen proof children.

`S56-M-1419-OBLIGATION_TREE` remains provisional `[_]`, not master accepted.
Six earlier recheck packets for this unchanged proof node are present at bases
`3a40b196`, `63a9ed9c`, `dc0f0264`, `21798c9c`, `b05dfe30`, and `48fb6596`.
The authoritative DAG nevertheless still records `attempts: 0`; this is a
master reconciliation defect, not a worker state change. If those six packets
are accepted as execution ticks, section 10.2 requires the master to split the
node rather than relaunch it unchanged.

## Fresh validation

No `lake update`, `lake build`, dependency clone/fetch, or deliberate `.lake`
mutation was performed. The automation-provided untracked `.lake` symlink was
reused read-only.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, passed. |
| `python3 scripts/stage1_target.py show THM-M-1419` | 0 | Rank 688; planned; rework required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1419/check_obligation_tree.py` | 0 | 14 obligations and 41 typed edges passed; root explicitly remains open `M3`. |
| Fresh temporary replay of `OseledetsStatement.lean` and `ObligationTree.lean` via `lake env lean --trust=0 -t0` | 0, 0 | Exact target and conditional wrapper elaborated; olean hashes were `f5222f...9169` and `4fd543...850a6`; wrapper axioms were exactly `[propext, Classical.choice, Quot.sound]`; temporary outputs were removed. |
| Pinned mathlib API inspection | 0 | `MeasurePreserving` stores forward measurability; `MeasurableEquiv` separately stores inverse measurability; `Ergodic.symm` requires `MeasurableEquiv`. |
| Token-anchored prohibited-device scan over owned Lean files | 1 | Expected no-match exit: no `sorry`, `admit`, axiom declaration, unsafe proof injection, `native_decide`, `implemented_by`, or `extern` occurs. |
| Read-only scratch source/olean audit | 0 | All 62 ordered modules had oleans; 26 sources differed from upstream; the terminal source matched upstream; terminal axiom output was `[propext, Classical.choice, Quot.sound]`. |

The scratch audit used an ephemeral, non-public `SCRATCH` root and matching
immutable `UP` source root supplied by the automation environment:

```bash
set -euo pipefail
: "${SCRATCH:?automation scratch root required}"
: "${UP:?immutable upstream root required}"
modified=0
missing=0
while IFS= read -r module; do
  rel="${module//.//}.lean"
  olean="$SCRATCH/${module//.//}.olean"
  cmp -s "$UP/$rel" "$SCRATCH/$rel" || modified=$((modified+1))
  test -f "$olean" || missing=$((missing+1))
done < "$SCRATCH/order.txt"
aggregate="$({
  while IFS= read -r module; do
    sha256sum "$SCRATCH/${module//.//}.olean"
  done < "$SCRATCH/order.txt"
} | sha256sum | cut -d' ' -f1)"
cmp -s "$UP/ErgodicTheory/TwoSided/SplittingAssembly.lean" \
  "$SCRATCH/ErgodicTheory/TwoSided/SplittingAssembly.lean"
printf 'MODULES=%s MISSING=%s MODIFIED=%s AGGREGATE=%s\n' \
  "$(awk 'NF {n++} END {print n+0}' "$SCRATCH/order.txt")" \
  "$missing" "$modified" "$aggregate"
sha256sum "$SCRATCH/ErgodicTheory/TwoSided/SplittingAssembly.lean" \
  "$SCRATCH/ErgodicTheory/TwoSided/SplittingAssembly.olean" \
  "$SCRATCH/compile-module62-slot33-attempt1.log"
rg -n '^[[:space:]]*(sorry|admit)([[:space:]]|$)|sorryAx|^[[:space:]]*axiom[[:space:]]|^[[:space:]]*unsafe[[:space:]]+(def|theorem)|native_decide|implemented_by|^[[:space:]]*extern[[:space:]]' \
  "$SCRATCH/ErgodicTheory" --glob '*.lean'
```

The final `rg` was run separately because its expected no-match exit is `1`; it
is a defensive token scan, not a substitute for the kernel axiom audit.

The exact terminal axiom probe was:

```bash
PROBE=$(mktemp)
printf '%s\n' \
  'import ErgodicTheory.TwoSided.SplittingAssembly' \
  '#check ErgodicTheory.oseledets_splitting' \
  '#print axioms ErgodicTheory.oseledets_splitting' \
  > "$PROBE"
cd Formalizations/Lean
LEAN_PATH="$SCRATCH:$(lake env printenv LEAN_PATH)" \
  LEAN_NUM_THREADS=1 lake env lean --trust=0 -t0 \
  -R "$SCRATCH" "$PROBE"
rm -f "$PROBE"
```

It exited `0`; the captured output SHA-256 was
`6f3cf56109f0550a4bb056bf00d37fa510927ec249ad9479be701b6de01198f1`.
The exact terminal lines were:

```text
ErgodicTheory.oseledets_splitting ...
'ErgodicTheory.oseledets_splitting' depends on axioms: [propext, Classical.choice, Quot.sound]
```

The output hash and ordered-olean aggregate are explicitly observational
scratch fingerprints. The aggregate hashes ordered `sha256sum` lines, including
the automation-private path spelling; it is not claimed as a portable receipt
or durable content address.

## Retry condition

The master must reopen `S56-M-1419-STATEMENT`, add inverse base measurability,
accept a new exact expression and registry version, and rerun the
source/mutation/anchor/tree gates. It must separately reconcile the six
observed recheck packets with the authoritative zero-attempt record and split
the proof frontier if more than five qualify as execution ticks. After those
gates, an owned integration task can vendor and validate the compatible
Oseledets port and implement the exact transports and typed four-child
composer.

This is current-base blocker evidence only. Accepted receipt IDs are empty;
the root remains `[H2, M3, R3]`; audit completion, theorem completion,
validation, release, and master acceptance remain open.
