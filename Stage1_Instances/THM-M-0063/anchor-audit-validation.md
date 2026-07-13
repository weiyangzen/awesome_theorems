# THM-M-0063 Anchor-Audit Validation

Item: S56-M-0063-ANCHOR_AUDIT

Base revision: 59c86ca38b16fe4d3901ba66530aae4df0e881b0

Base tree: 2b8fc12c558d4fe807d7b4ac4b2c9a127002338e

Validation date: 2026-07-13 (Asia/Shanghai)

## Result

Pinned mathlib revision 8a178386ffc0f5fef0b77738bb5449d50efeea95 contains an exact
Cayley-theorem route. Equiv.Perm.subgroupOfMulAction G G specializes the generalized faithful
action theorem to the ordinary left regular action. Its result is exactly the frozen equivalence
from an arbitrary group to the range subgroup of MulAction.toPermHom G G; no finiteness,
nontriviality, decidable equality, or commutativity premise appears.

AnchorAudit.lean checks that direct specialization and a lower-level construction through
MonoidHom.ofInjective MulAction.toPerm_injective. Both close a literal copy of the frozen target.
Lean prints the direct terminal body, reports only propext, Classical.choice, and Quot.sound
for both exact adapters, and reports all three audited declarations sorry-free. The lower-level
route deduplicates to the same regular-action injectivity argument rather than adding an independent
proof body.

The bounded external search found only downstream teaching wrappers. The strongest named one,
mathematics_in_lean at dd6d752f has CayleyIsoMorphism and invokes the same mathlib declaration under
different Lean/mathlib pins; its file also contains unrelated placeholders. It adds no independent
terminal proof or integration task. GitHub code search and grep.app access limitations are recorded,
so internet-wide discovery saturation is not claimed.

The exact pinned route is an M0-W candidate with local E2 evidence. The accepted root remains
H1/M3/R4 until later proof, complete provenance/trust, validation, and master-acceptance gates
supply accepted E1 evidence. Neither AUDIT-Z nor theorem completion is claimed.

## Commands And Results

All local validation ran in this worker clone against the automation-provided canonical .lake
symlink read-only. No lake update, lake build, dependency clone/fetch, or .lake mutation ran.

| Command | Exit | Result |
|---|---:|---|
| python3 Docs/tools/check_stage1_standard.py | 0 | standard structure passed: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets |
| python3 scripts/stage1_target.py check | 0 | 1546 unique ordered targets passed |
| python3 scripts/stage1_target.py show THM-M-0063 | 0 | rank 1094; planned; L0/rework-required; theorem incomplete |
| git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD HEAD^{tree} | 0 | revision 8a1783...ea95, tree bdc39a...5c2b |
| git -C Formalizations/Lean/.lake/packages/mathlib status --porcelain=v1 --untracked-files=no | 0 | empty output; pinned dependency worktree clean |
| immutable git grep, declaration #find, and local rg over repository and every manifest-pinned package | 0/1 | direct Cayley declaration and injectivity component found in mathlib; expected no-match exit 1 outside mathlib |
| Sourcegraph bounded queries with forks and archives included | 0 | six matches across five repositories: mathlib plus four wrappers, all sharing the same mathlib terminal; response hash recorded |
| GitHub focused repository and code queries; grep.app query | 0/401/429 | focused repository query returned zero; access failures are hashed and do not support a global absence claim |
| immutable HTTPS inspection of mathematics_in_lean at dd6d752f | 0 | exact wrapper, source hash, toolchain, dependency revision, shared terminal body, and unrelated placeholder boundary matched |
| lake env lean ../../Stage1_Instances/THM-M-0063/AnchorAudit.lean from Formalizations/Lean | 0 | exact direct and composite adapters elaborated; terminal body and axiom reports matched; three sorry-free reports; stdout SHA-256 9aeb8fbb...b78 |
| python3 -B Stage1_Instances/THM-M-0063/check_anchor_audit.py --worker-packet .stage1-worker-selftest.json | 0 | manifest item, frozen statement, protocol, pins, source blobs/hashes, provenance, immutable external wrapper, Lean output, receipt, packet, and classifications matched |
| python3 -m json.tool on the three anchor JSON artifacts and worker packet | 0 | all structured artifacts parsed |
| scoped prohibited-construct scan over AnchorAudit.lean and the terminal mathlib source | 1 (expected no match) | no proof gap, custom axiom declaration, unsafe/opaque body, TODO, FIXME, or placeholder |
| git diff --check -- Stage1_Instances/THM-M-0063 .stage1-worker-selftest.json | 0 | no whitespace diagnostics |

## Search Boundary

The frozen inventory classifies four candidate groups: the direct pinned mathlib theorem, its
lower-level composite route, the principal external instructional wrapper, and the remaining
indexed duplicate-wrapper family. Public query hashes and access failures are preserved in the
ledger. These bounded results do not establish that no unindexed Lean source exists.

## Status Boundary

This phase supplies provisional self-tested anchor evidence pending master acceptance. The
obligation registry, proof-phase canonical wrapper, complete transitive provenance/trust and TCB
closure, source and readable reconstruction review, hermetic and independent validation,
deterministic release evidence, AUDIT-Z, and theorem completion remain open.
