# Source-statement crosswalk

## Repository source record

The source record in `Docs/Stage0_Blueprint.md` provides only the title "配边环结构" and the phrase
"配边环的代数结构". It supplies no bordism variant, formal statement, citation, assumptions, or
proof. The manifest's `已验证` label is explicitly untrusted under rev-5.6 and gives no `H` or `M`
credit.

## Candidate mathematical sources

- René Thom, "Quelques propriétés globales des variétés différentiables", *Commentarii
  Mathematici Helvetici* 28 (1954), 17-86. This is a historical primary research source for
  cobordism theory. The exact proposition(s), conventions, and pages supporting the ring laws have
  not yet been inspected.
- Robert E. Stong, *Notes on Cobordism Theory*, Princeton University Press, 1968. This is a modern
  reference candidate for the geometric bordism groups and their products. Edition-stable
  definition/theorem/page anchors and errata remain to be checked.

These entries are discovery anchors only. They do not establish `H0`, and neither is evidence of a
Lean formalization. The source audit must inspect a stable copy and record exact pages, definitions,
theorems, assumptions, proof nodes, and known errata; an independent reviewer must approve that
crosswalk.

## Provisional crosswalk

| Repository phrase | Intended component | Source fact to pin | Required Lean component | Intake status |
|---|---|---|---|---|
| "bordism classes" | quotient of closed smooth manifolds by existence of a compact bordism | exact category, boundary, and equivalence-relation definitions | representative type, bordism relation, quotient/setoid | included; variant open |
| "ring" | additive group plus compatible associative multiplication and unit | theorem(s) proving operations descend and satisfy laws | graded carrier and `AddCommGroup`/ring-style structure | included; encoding open |
| addition | disjoint union | well-definedness under bordism and inverse convention | disjoint-union operation and quotient lift | included; API open |
| multiplication | Cartesian product | product bordism and boundary/corner handling | product operation and quotient lift | included; API open |
| grading | dimension adds under products | dimension convention and direct-sum construction | graded family indexed by `Nat` | included; bundling open |
| commutativity | factor swap | oriented sign or unoriented equality | checked swap transport and sign law | included; theory-dependent |
| identities | empty manifold and point | unit/zero conventions | distinguished quotient classes | included; boundary tests open |

## Formal-source boundary

Repository search found mentions of cobordism as missing infrastructure in unrelated legacy modules,
but no artifact owned by `THM-M-0604` and no exact declaration was found. Those mentions receive no
statement or proof credit. The statement phase must first select the exact human theorem and then
elaborate that theorem using minimal pinned imports; an abstract structure carrying the desired ring
laws would be a circular substitution.
