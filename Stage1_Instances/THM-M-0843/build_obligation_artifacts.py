#!/usr/bin/env python3
"""Build the frozen THM-M-0843 obligation registry and typed graphs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ITEM = "S56-M-0843-OBLIGATION_TREE"
THEOREM = "THM-M-0843"
PREFIX = "M0843-"
MATHLIB_REVISION = "8a178386ffc0f5fef0b77738bb5449d50efeea95"
TERMINAL_BODY = (
    "mathlib:8a178386:Mathlib.Combinatorics.SimpleGraph.Regularity.Lemma"
    "#szemeredi_regularity"
)


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def spec(
    oid: str,
    kind: str,
    risk: str,
    claim: str,
    formal: str,
    output: str,
    source: str,
    budget: int,
) -> dict:
    return {
        "id": oid,
        "kind": kind,
        "risk": risk,
        "claim": claim,
        "formal": formal,
        "output": output,
        "source": source,
        "budget": budget,
    }


SPECS = [
    spec("M0843-ROOT", "root", "critical", "Every admissible finite simple graph has the exact frozen bounded epsilon-uniform equipartition.", "Stage1Instances.THM_M_0843.SzemerediRegularityTarget", "The canonical proposition at arbitrary universe u.", "Statement.lean; expression sha256 3fe13f3562cb642e45e467687508ac44f945e9848ff53d22b9cf068d7ec11219", 12),
    spec("M0843-S-TARGET", "definition", "high", "Freeze graph, decidability, tolerance, lower bound, full-vertex finpartition, equitability, explicit bound, and uniformity interfaces.", "Stage1Instances.THM_M_0843.SzemerediRegularityTarget", "The exact elaborated root interface.", "Statement.lean:20-36", 22),
    spec("M0843-S-BOUNDARY", "definition", "high", "Retain epsilon positivity and l <= card alpha exactly, including l = 0 and empty or singleton types when the premise permits them.", "the ordered binders and hypotheses of SzemerediRegularityTarget", "No strengthened or omitted boundary premise.", "Statement.lean:24-36; statement.json encoding_decisions.boundaries", 18),
    spec("M0843-S-FOUNDATION", "certificate", "critical", "Account for classical choice, quotient soundness, propositional extensionality, Lean, mathlib, imports, and the no-oracle policy.", "#print axioms szemeredi_regularity and the exact local adapters", "A versioned foundation and TCB boundary.", "ObligationTree.lean axiom probes; anchor-audit.json immutable_environment", 24),
    spec("M0843-N-BOUNDS", "normalization", "high", "Relate l, initialBound epsilon l, iterated stepBound, and bound epsilon l with positivity and monotonicity.", "planned signature: l <= initialBound epsilon l /\\ 7 <= initialBound epsilon l /\\ 0 < initialBound epsilon l /\\ initialBound epsilon l <= bound epsilon l /\\ (forall n, n <= stepBound n) /\\ Monotone stepBound", "All cardinal bounds used by the large-graph construction.", "Regularity/Bound.lean:167-200; Regularity/Lemma.lean:85-87,105-109,135-146", 42),
    spec("M0843-B-CARD-SPLIT", "branch", "high", "Split card alpha <= bound epsilon l from bound epsilon l <= card alpha and recombine exhaustively.", "le_total (Fintype.card alpha) (SzemerediRegularity.bound epsilon l)", "Either the singleton partition route or the iterative route.", "Regularity/Lemma.lean:79-84", 12),
    spec("M0843-B-SMALL", "branch", "normal", "For card alpha <= bound epsilon l, use the bottom singleton partition and prove all four conclusions.", "Finpartition.bot_isEquipartition; card_bot; card_univ; Finpartition.bot_isUniform", "An admissible partition in the small-cardinality branch.", "Regularity/Lemma.lean:80-83", 18),
    spec("M0843-B-LARGE", "branch", "high", "For bound epsilon l <= card alpha, construct the initial partition and run the tolerance split.", "planned signature: bound epsilon l <= Fintype.card alpha -> exists P : Finpartition univ, P.IsEquipartition /\\ l <= P.parts.card /\\ P.parts.card <= bound epsilon l /\\ P.IsUniform G epsilon", "An admissible partition in the large-cardinality branch.", "Regularity/Lemma.lean:84-155", 16),
    spec("M0843-C-INITIAL", "construction", "high", "Construct an equipartition of univ with exactly initialBound epsilon l parts.", "Finpartition.exists_equipartition_card_eq", "dum with IsEquipartition and exact part cardinality.", "Regularity/Equitabilise.lean:195; Regularity/Lemma.lean:85-89", 26),
    spec("M0843-B-EPS-SPLIT", "branch", "high", "Split 1 <= epsilon from epsilon <= 1 and recombine the easy and energy routes.", "le_total 1 epsilon", "An epsilon-uniform bounded equipartition in either tolerance branch.", "Regularity/Lemma.lean:90-155", 12),
    spec("M0843-B-EPS-GE-ONE", "branch", "normal", "When 1 <= epsilon, enlarge one-uniformity of the initial equipartition by monotonicity.", "Finpartition.isUniform_one; Finpartition.IsUniform.mono", "The initial equipartition is epsilon-uniform.", "Regularity/Lemma.lean:91-93", 18),
    spec("M0843-C-ENERGY-INVARIANT", "construction", "critical", "For every i construct an equipartition between t and stepBound^[i] t that is uniform or has energy at least epsilon^5/4*i.", "the local suffices h invariant in szemeredi_regularity", "The induction invariant consumed by the terminal energy contradiction.", "Regularity/Lemma.lean:94-101,116-155", 30),
    spec("M0843-B-INDUCT-ZERO", "branch", "normal", "Establish the energy invariant at i = 0 from the initial partition and energy nonnegativity.", "Finpartition.energy_nonneg", "The i = 0 invariant instance.", "Regularity/Lemma.lean:119-123", 16),
    spec("M0843-B-INDUCT-SUCC", "branch", "critical", "At i+1 split whether the current partition is already uniform, preserving it or incrementing it.", "by_cases huniform : P.IsUniform G epsilon", "The successor invariant instance.", "Regularity/Lemma.lean:124-155", 18),
    spec("M0843-B-ALREADY-UNIFORM", "branch", "normal", "If P is uniform, reuse P and enlarge its iterate bound by le_stepBound.", "Function.iterate_succ_apply'; SzemerediRegularity.le_stepBound", "The successor invariant with its uniform disjunct.", "Regularity/Lemma.lean:127-131", 14),
    spec("M0843-B-NONUNIFORM", "branch", "critical", "If P is nonuniform, derive the numerical side conditions and use its increment to raise energy.", "planned signature: not (P.IsUniform G epsilon) -> epsilon^5 / 4 * i <= P.energy G -> exists Q, Q.IsEquipartition /\\ t <= Q.parts.card /\\ Q.parts.card <= (stepBound^[i+1]) t /\\ epsilon^5 / 4 * (i+1) <= Q.energy G", "The successor invariant with its energy disjunct.", "Regularity/Lemma.lean:132-155", 24),
    spec("M0843-N-ITERATION", "normalization", "critical", "Derive 100 <= 4^card(P.parts)*epsilon^5, i <= 4/epsilon^5, the terminal iterate bound, and the graph-cardinality side condition.", "planned signature: 100 <= 4^P.parts.card * epsilon^5 /\\ (i : Real) <= 4 / epsilon^5 /\\ P.parts.card <= (stepBound^[floor(4/epsilon^5)]) t /\\ P.parts.card * 16^P.parts.card <= Fintype.card alpha", "All hypotheses needed by card_increment and energy_increment.", "Regularity/Lemma.lean:134-146", 48),
    spec("M0843-C-INCREMENT", "construction", "critical", "Construct the refinement P.increment and assemble its equitability, cardinal bounds, and raised-energy result.", "SzemerediRegularity.increment", "A successor-stage equipartition satisfying the invariant.", "Regularity/Increment.lean:52-59; Regularity/Lemma.lean:147-155", 22),
    spec("M0843-L-INCREMENT-EQUIP", "core_lemma", "high", "Show that gluing the equitable chunks produces an equipartition.", "SzemerediRegularity.increment_isEquipartition", "(increment hP G epsilon).IsEquipartition.", "Regularity/Increment.lean:79-86", 18),
    spec("M0843-L-INCREMENT-CARD", "core_lemma", "high", "Compute the increment partition cardinality as stepBound of the old part count.", "SzemerediRegularity.card_increment", "card(increment.parts) = stepBound card(P.parts).", "Regularity/Increment.lean:65-77", 32),
    spec("M0843-L-ENERGY-INCREMENT", "core_lemma", "critical", "Raise energy by epsilon^5/4 for a large enough nonuniform equitable partition.", "SzemerediRegularity.energy_increment", "energy(P)+epsilon^5/4 <= energy(increment P).", "Regularity/Increment.lean:138-182", 28),
    spec("M0843-C-CHUNK-REFINEMENT", "construction", "critical", "Break each old part along nonuniform witnesses, equitabilise it, and bind all chunks into increment.", "SzemerediRegularity.chunk; Finpartition.equitabilise; SzemerediRegularity.increment", "A controlled refinement whose pieces have size m or m+1.", "Regularity/Chunk.lean:62-71,172-187; Regularity/Equitabilise.lean:149-195; Regularity/Increment.lean:52-86", 88),
    spec("M0843-C-EQUITABILISE", "construction", "high", "Equitabilise a finite partition using the quotient/remainder cardinal decomposition and retain exact small/big part counts.", "Finpartition.equitabilise; Finpartition.equitabilise_isEquipartition; Finpartition.card_parts_equitabilise", "An equipartition with controlled part count and sizes.", "Regularity/Equitabilise.lean:45-195", 72),
    spec("M0843-C-CHUNK-WITNESSES", "construction", "critical", "Form the star families from nonuniformity witnesses and show they lie in the chunk partition.", "SzemerediRegularity.star; SzemerediRegularity.biUnion_star_subset_nonuniformWitness; SzemerediRegularity.star_subset_chunk", "Witness-aligned subfamilies of every chunk.", "Regularity/Chunk.lean:62-120", 70),
    spec("M0843-L-CHUNK-CARD", "core_lemma", "high", "Prove exact chunk part count and the m to m+1 cardinal bounds for every member.", "SzemerediRegularity.card_chunk; SzemerediRegularity.card_eq_of_mem_parts_chunk; SzemerediRegularity.m_le_card_of_mem_chunk_parts; SzemerediRegularity.card_le_m_add_one_of_mem_chunk_parts", "Controlled chunk cardinality and member sizes.", "Regularity/Chunk.lean:172-187", 36),
    spec("M0843-C-DISTINCT-PAIRS", "construction", "high", "Index chunk pairs over old off-diagonal pairs, prove containment in the new off-diagonal set, and prove pairwise disjointness.", "SzemerediRegularity.distinctPairs and its two private support theorems", "A disjoint reindexing domain for the energy sum.", "Regularity/Increment.lean:88-121", 44),
    spec("M0843-C-DISTINCT-CONTAIN", "construction", "high", "Show the union of chunk-pair families is contained in the increment partition's off-diagonal pair set.", "SzemerediRegularity.distinctPairs_increment (private theorem)", "Containment needed for monotonicity of the nonnegative energy sum.", "Regularity/Increment.lean:96-106", 28),
    spec("M0843-C-DISTINCT-DISJOINT", "construction", "high", "Show chunk-pair families indexed by different old off-diagonal pairs are pairwise disjoint.", "SzemerediRegularity.pairwiseDisjoint_distinctPairs (private lemma)", "Disjointness needed by sum_biUnion.", "Regularity/Increment.lean:108-121", 32),
    spec("M0843-L-CHUNK-DENSITY", "core_lemma", "critical", "For uniform and nonuniform old pairs, bound the normalized sum of squared chunk densities with the required epsilon gain or loss.", "le_sum_distinctPairs_edgeDensity_sq using edgeDensity_chunk_uniform and edgeDensity_chunk_not_uniform", "The pointwise squared-density inequality for each old pair.", "Regularity/Increment.lean:125-136; Regularity/Chunk.lean:335-509", 96),
    spec("M0843-L-CHUNK-AVERAGE", "core_lemma", "critical", "Bound the weighted average density of chunk pairs near the old total density using size control.", "SzemerediRegularity.average_density_near_total_density (private theorem)", "The average-density approximation used in both pair cases.", "Regularity/Chunk.lean:190-357", 86),
    spec("M0843-L-CHUNK-AUX", "core_lemma", "critical", "Bound the square of the old pair density by the square of the average chunk density, up to epsilon^5/25.", "SzemerediRegularity.edgeDensity_chunk_aux (private theorem)", "The common squared-average lower bound used by both chunk density branches.", "Regularity/Chunk.lean:335-360", 48),
    spec("M0843-L-DENSITY-STAR", "core_lemma", "critical", "Control star-family density and prove its witness subsets are large enough for nonuniformity.", "SzemerediRegularity.abs_density_star_sub_density_le_eps; SzemerediRegularity.eps_le_card_star_div; SzemerediRegularity.edgeDensity_star_not_uniform", "A density-separated star subfamily for every nonuniform pair.", "Regularity/Chunk.lean:362-452", 90),
    spec("M0843-L-DENSITY-NONUNIFORM", "core_lemma", "critical", "Convert the star density separation into a squared-density gain for a nonuniform old pair.", "SzemerediRegularity.edgeDensity_chunk_not_uniform", "The nonuniform-pair chunk inequality.", "Regularity/Chunk.lean:454-503", 78),
    spec("M0843-L-DENSITY-UNIFORM", "core_lemma", "high", "Use convexity of squares and the average-density approximation to prevent excessive energy loss for a uniform old pair.", "SzemerediRegularity.edgeDensity_chunk_uniform", "The uniform-pair chunk inequality.", "Regularity/Chunk.lean:505-522", 42),
    spec("M0843-L-NONUNIFORM-COUNT", "core_lemma", "critical", "Convert failure of partition uniformity and the seven-part lower bound into the cardinal inequality that pays for the epsilon^5/4 gain.", "Finpartition.IsUniform definition; offDiag_card; the arithmetic tail of energy_increment", "A lower bound on the contribution of nonuniform pairs.", "Regularity/Uniform.lean:196-235; Regularity/Increment.lean:159-182", 58),
    spec("M0843-L-ENERGY-RECOMPOSE", "core_lemma", "critical", "Rewrite old and new energies as squared-density sums, reindex the disjoint chunk pairs, and compare to the full new off-diagonal sum.", "Finpartition.coe_energy; sum_biUnion; sum_le_sum_of_subset_of_nonneg", "The global energy inequality from the pointwise chunk bounds.", "Regularity/Energy.lean:38-63; Regularity/Increment.lean:143-169", 70),
    spec("M0843-L-ENERGY-COE", "core_lemma", "high", "Rewrite rational partition energy as a real normalized off-diagonal squared-density sum.", "Finpartition.coe_energy", "A real-valued sum representation of energy.", "Regularity/Energy.lean:38-63", 28),
    spec("M0843-L-ENERGY-SUM", "core_lemma", "high", "Reindex the sum over pairwise-disjoint distinctPairs families and compare the contained subfamily to the full increment off-diagonal sum.", "Finset.sum_biUnion; Finset.sum_le_sum_of_subset_of_nonneg", "The global new-partition sum bound.", "Regularity/Increment.lean:147-157", 38),
    spec("M0843-B-ENERGY-CONTRADICTION", "branch", "critical", "Choose floor(4/epsilon^5)+1, rule out its energy alternative using strict growth and energy <= 1, and discharge the final bound.", "Nat.lt_floor_add_one; Finpartition.energy_le_one; SzemerediRegularity.bound", "The uniform partition returned by the energy route.", "Regularity/Lemma.lean:100-115", 42),
    spec("M0843-T-UPSTREAM", "terminal", "critical", "Compose the cardinal split, initial construction, tolerance split, energy induction, increment engine, and contradiction.", "szemeredi_regularity", "The literal pinned mathlib proposition.", "Regularity/Lemma.lean:74-155", 34),
    spec("M0843-T-ADAPTER", "transport", "high", "Apply the literal pinned terminal proposition at the exact canonical binders.", "Stage1Instances.THM_M_0843_Obligations.terminal_adapter", "The exact frozen root proposition.", "ObligationTree.lean: terminal_adapter and compose_root", 12),
    spec("M0843-X-SOURCE", "terminal", "high", "Map every material node to reviewed human sources with edition, page, assumptions, proof steps, and errata.", "node-specific primary-source crosswalk remains open", "Human-source coverage without machine proof credit.", "source-statement-crosswalk.md; anchor-audit.json source_leads", 36),
    spec("M0843-X-PROVENANCE", "certificate", "critical", "Bind wrapper, terminal and support bodies, immutable source hashes, licenses, direct dependencies, and replay evidence without duplicate credit.", "anchor-audit.json candidate M0843-C01 plus a future transitive closure packet", "Proof-body provenance without mathematical proof credit.", "anchor-audit.json; anchor-audit-receipt.json", 38),
    spec("M0843-X-TRUST", "certificate", "critical", "Audit the transitive Lean/mathlib declaration closure, compiled artifacts, executables, unsafe/oracle boundaries, and independent replay.", "Lean 4.29.0; mathlib 8a178386; release trust closure pending", "Release-grade trust inventory without mathematical proof credit.", "anchor-audit.json immutable_environment and foundation_assessment", 40),
]


REQUIRES = {
    "M0843-ROOT": ["M0843-T-ADAPTER", "M0843-T-UPSTREAM"],
    "M0843-T-UPSTREAM": ["M0843-B-CARD-SPLIT"],
    "M0843-B-CARD-SPLIT": ["M0843-B-SMALL", "M0843-B-LARGE"],
    "M0843-B-LARGE": ["M0843-N-BOUNDS", "M0843-B-EPS-SPLIT"],
    "M0843-B-EPS-SPLIT": ["M0843-C-INITIAL", "M0843-B-EPS-GE-ONE", "M0843-B-ENERGY-CONTRADICTION"],
    "M0843-B-ENERGY-CONTRADICTION": ["M0843-C-ENERGY-INVARIANT"],
    "M0843-C-ENERGY-INVARIANT": ["M0843-B-INDUCT-ZERO", "M0843-B-INDUCT-SUCC"],
    "M0843-B-INDUCT-SUCC": ["M0843-B-ALREADY-UNIFORM", "M0843-B-NONUNIFORM"],
    "M0843-B-NONUNIFORM": ["M0843-N-ITERATION", "M0843-C-INCREMENT"],
    "M0843-N-ITERATION": ["M0843-N-BOUNDS"],
    "M0843-C-INCREMENT": ["M0843-L-INCREMENT-EQUIP", "M0843-L-INCREMENT-CARD", "M0843-L-ENERGY-INCREMENT"],
    "M0843-L-ENERGY-INCREMENT": ["M0843-C-CHUNK-REFINEMENT", "M0843-C-DISTINCT-PAIRS", "M0843-L-CHUNK-DENSITY", "M0843-L-NONUNIFORM-COUNT", "M0843-L-ENERGY-RECOMPOSE"],
    "M0843-C-CHUNK-REFINEMENT": ["M0843-C-EQUITABILISE", "M0843-C-CHUNK-WITNESSES", "M0843-L-CHUNK-CARD"],
    "M0843-C-DISTINCT-PAIRS": ["M0843-C-DISTINCT-CONTAIN", "M0843-C-DISTINCT-DISJOINT"],
    "M0843-L-CHUNK-DENSITY": ["M0843-L-CHUNK-AVERAGE", "M0843-L-DENSITY-STAR", "M0843-L-DENSITY-NONUNIFORM", "M0843-L-DENSITY-UNIFORM"],
    "M0843-L-CHUNK-AUX": ["M0843-L-CHUNK-AVERAGE", "M0843-L-CHUNK-CARD"],
    "M0843-L-DENSITY-NONUNIFORM": ["M0843-L-CHUNK-AUX", "M0843-L-DENSITY-STAR"],
    "M0843-L-DENSITY-UNIFORM": ["M0843-L-CHUNK-AUX", "M0843-L-CHUNK-CARD"],
    "M0843-L-ENERGY-RECOMPOSE": ["M0843-L-ENERGY-COE", "M0843-L-ENERGY-SUM", "M0843-C-DISTINCT-CONTAIN", "M0843-C-DISTINCT-DISJOINT"],
}

SOURCE_NA = {"M0843-S-TARGET", "M0843-S-BOUNDARY", "M0843-S-FOUNDATION", "M0843-X-PROVENANCE", "M0843-X-TRUST"}
MACHINE_SPECIAL = {
    "M0843-X-SOURCE": "not_applicable",
    "M0843-X-PROVENANCE": "informational",
    "M0843-X-TRUST": "informational",
}
BODY_IDS = {
    "M0843-T-UPSTREAM": TERMINAL_BODY,
    "M0843-L-INCREMENT-EQUIP": "mathlib:8a178386:Regularity.Increment#increment_isEquipartition",
    "M0843-L-INCREMENT-CARD": "mathlib:8a178386:Regularity.Increment#card_increment",
    "M0843-L-ENERGY-INCREMENT": "mathlib:8a178386:Regularity.Increment#energy_increment",
    "M0843-C-EQUITABILISE": "mathlib:8a178386:Regularity.Equitabilise#Finpartition.equitabilise",
    "M0843-C-CHUNK-WITNESSES": "mathlib:8a178386:Regularity.Chunk#SzemerediRegularity.star",
    "M0843-L-CHUNK-CARD": "mathlib:8a178386:Regularity.Chunk#SzemerediRegularity.card_chunk",
    "M0843-C-DISTINCT-CONTAIN": "mathlib:8a178386:Regularity.Increment#SzemerediRegularity.distinctPairs_increment",
    "M0843-C-DISTINCT-DISJOINT": "mathlib:8a178386:Regularity.Increment#SzemerediRegularity.pairwiseDisjoint_distinctPairs",
    "M0843-L-CHUNK-AVERAGE": "mathlib:8a178386:Regularity.Chunk#SzemerediRegularity.average_density_near_total_density",
    "M0843-L-CHUNK-AUX": "mathlib:8a178386:Regularity.Chunk#SzemerediRegularity.edgeDensity_chunk_aux",
    "M0843-L-DENSITY-STAR": "mathlib:8a178386:Regularity.Chunk#SzemerediRegularity.edgeDensity_star_not_uniform",
    "M0843-L-DENSITY-NONUNIFORM": "mathlib:8a178386:Regularity.Chunk#SzemerediRegularity.edgeDensity_chunk_not_uniform",
    "M0843-L-DENSITY-UNIFORM": "mathlib:8a178386:Regularity.Chunk#SzemerediRegularity.edgeDensity_chunk_uniform",
    "M0843-L-ENERGY-COE": "mathlib:8a178386:Regularity.Energy#Finpartition.coe_energy",
}


spec_by_id = {row["id"]: row for row in SPECS}
assert len(spec_by_id) == len(SPECS)
INTERFACE_TYPES = {
    "M0843-T-ADAPTER": "Stage1Instances.THM_M_0843_Obligations.MathlibTerminal.{u} -> Stage1Instances.THM_M_0843.SzemerediRegularityTarget.{u}",
    "M0843-T-UPSTREAM": "Stage1Instances.THM_M_0843_Obligations.MathlibTerminal.{u}",
}
statement = json.loads((HERE / "statement.json").read_text(encoding="utf-8"))
expression_hash = statement["canonical_formal_target"]["elaborated_expression_sha256"]
statement_hash = hashlib.sha256((HERE / "Statement.lean").read_bytes()).hexdigest()
anchor_hash = hashlib.sha256((HERE / "anchor-audit.json").read_bytes()).hexdigest()


def body_id_for(oid: str) -> str | None:
    if oid in BODY_IDS:
        return BODY_IDS[oid]
    if oid in REQUIRES:
        return None
    row = spec_by_id[oid]
    if "planned signature:" in row["formal"] or "ordered binders" in row["formal"]:
        return None
    primary = row["formal"].split(";")[0].strip()
    if not primary or " " in primary:
        return None
    return "mathlib:8a178386:declaration#" + primary


obligations = []
for row in SPECS:
    oid = row["id"]
    if oid in {"M0843-ROOT", "M0843-S-TARGET"}:
        fingerprint = "lean-expression-sha256:" + expression_hash
    elif oid in INTERFACE_TYPES:
        fingerprint = "lean-declaration-type-sha256:" + digest(INTERFACE_TYPES[oid])
    else:
        fingerprint = "source-step:v1:sha256:" + digest([oid, row["kind"], row["claim"], row["formal"], row["output"]])
    machine = MACHINE_SPECIAL.get(oid, "required")
    obligations.append({
        "obligation_id": oid,
        "statement_fingerprint": fingerprint,
        "kind": row["kind"],
        "root_relevant": True,
        "machine_eligibility": machine,
        "human_source_eligibility": "not_applicable" if oid in SOURCE_NA else "required",
        "readable_eligibility": "required",
        "risk_class": row["risk"],
        "exclusion_reason": "support_overlay_no_proof_credit" if oid in MACHINE_SPECIAL else None,
        "terminal_proof_body_id": body_id_for(oid),
    })

DENOMINATOR_FIELDS = (
    "obligation_id", "statement_fingerprint", "kind", "root_relevant",
    "machine_eligibility", "human_source_eligibility", "readable_eligibility",
    "risk_class", "exclusion_reason", "terminal_proof_body_id",
)
denominator = digest([{key: row[key] for key in DENOMINATOR_FIELDS} for row in obligations])
ids = [row["obligation_id"] for row in obligations]

registry = {
    "schema_version": "stage1-obligation-registry/1.0",
    "registry_id": "THM-M-0843-OBLIGATIONS-v1",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_version": 1,
    "frozen_at": "2026-07-13T00:00:00+08:00",
    "freeze_basis": "The exact statement and bounded immutable anchor inventory determine the cardinality, tolerance, energy-induction, increment, terminal, source, provenance, and trust architecture. Eligibility is assigned before any proof-phase closure credit.",
    "frozen_against_statement_sha256": statement_hash,
    "frozen_against_anchor_audit_sha256": anchor_hash,
    "root_obligation_id": "M0843-ROOT",
    "denominator_sha256": denominator,
    "frozen_denominators": {
        "inventory": ids,
        "required_machine": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "required"],
        "required_human_source": [row["obligation_id"] for row in obligations if row["human_source_eligibility"] == "required"],
        "required_readable": ids,
        "informational_overlays": [row["obligation_id"] for row in obligations if row["machine_eligibility"] == "informational"],
    },
    "delta_policy": "Any correction, split, merge, exclusion, eligibility, risk, or proof-body identity change requires registry version 2 and an append-only old/new ID delta.",
    "append_only_delta": [],
    "obligations": obligations,
    "status_observed_after_freeze": {
        "closed_obligations": [],
        "accepted_root_machine_debt": "M3",
        "candidate_route": "M0843-C01 is an exact pinned M0-W candidate with only E2 worker evidence; it is not accepted closure.",
        "human_source_debt": "H1",
        "readability_debt": "R4",
    },
    "status_boundary": "Frozen architecture only. No obligation receives closure credit; the exact candidate remains E2 pending proof-phase receipts and master acceptance, and the accepted root remains H1/M3/R4.",
}


def ledger(row: dict) -> list[dict]:
    oid = row["id"]
    children = REQUIRES.get(oid, [])
    steps = []
    for index, child in enumerate(children, 1):
        steps.append({
            "step_id": f"{oid}-STEP-{index:02d}",
            "premise_ids": [child],
            "inference": "consume the exact typed child output",
            "source_locator": spec_by_id[child]["source"],
            "output": spec_by_id[child]["output"],
            "outgoing_use": f"composition of {oid}",
        })
    steps.append({
        "step_id": f"{oid}-STEP-{len(steps) + 1:02d}",
        "premise_ids": children if children else ["frozen-formal-context"],
        "inference": row["formal"],
        "source_locator": row["source"],
        "output": row["output"],
        "outgoing_use": "declared proof parent or non-proof typed support edge only",
    })
    return steps


LEAF_LEDGERS = {
    "M0843-C-EQUITABILISE": [
        (["frozen-finite-partition-context"], "Euclidean division of card s by the requested part size supplies small/big part counts.", "Regularity/Equitabilise.lean:45-148", "A cardinal decomposition a*m+b*(m+1)=card s."),
        (["M0843-C-EQUITABILISE-STEP-01"], "Finpartition.equitabilise groups singleton parts into blocks of the two allowed sizes.", "Regularity/Equitabilise.lean:149-153", "A finpartition equitabilise P h of s."),
        (["M0843-C-EQUITABILISE-STEP-02"], "Membership and filter-count lemmas identify every new part size and count the big/small parts.", "Regularity/Equitabilise.lean:154-182", "Exact size alternatives and filter cardinalities."),
        (["M0843-C-EQUITABILISE-STEP-03"], "card_parts_equitabilise and equitabilise_isEquipartition package the construction invariants.", "Regularity/Equitabilise.lean:158-188", "An equipartition with controlled part count."),
    ],
    "M0843-C-CHUNK-WITNESSES": [
        (["frozen-nonuniform-pair-witnesses"], "chunk equitabilises the Boolean-atom refinement cut out by all nonuniform witnesses.", "Regularity/Chunk.lean:62-70", "A finpartition chunk hP G epsilon hU."),
        (["M0843-C-CHUNK-WITNESSES-STEP-01"], "star selects chunk parts lying inside the chosen nonuniform witness.", "Regularity/Chunk.lean:71-80", "The star hP G epsilon hU V family."),
        (["M0843-C-CHUNK-WITNESSES-STEP-02"], "biUnion_star_subset_nonuniformWitness proves witness containment.", "Regularity/Chunk.lean:81-86", "The union of star parts lies inside the witness."),
        (["M0843-C-CHUNK-WITNESSES-STEP-02"], "star_subset_chunk proves every selected set is an actual chunk part.", "Regularity/Chunk.lean:87-89", "star is a subfamily of chunk.parts."),
        (["M0843-C-CHUNK-WITNESSES-STEP-03"], "Remainder and cardinal estimates show star covers enough of the witness for later density separation.", "Regularity/Chunk.lean:90-170", "A lower bound for card star relative to the witness."),
    ],
    "M0843-L-CHUNK-AVERAGE": [
        (["M0843-L-CHUNK-CARD"], "Bound the total cardinality of selected chunk parts using the m and m+1 size window.", "Regularity/Chunk.lean:190-212", "Upper and lower selected-cardinality estimates."),
        (["M0843-L-CHUNK-CARD"], "Convert m and m+1 ratios to real inequalities from the graph-cardinality hypothesis.", "Regularity/Chunk.lean:213-241", "Multiplicative ratio bounds."),
        (["M0843-C-CHUNK-WITNESSES"], "Compare old density minus epsilon to the weighted density sum over chunk pairs.", "Regularity/Chunk.lean:242-278", "A lower weighted-density estimate."),
        (["M0843-C-CHUNK-WITNESSES"], "Compare the weighted density sum to old density plus epsilon.", "Regularity/Chunk.lean:279-317", "An upper weighted-density estimate."),
        (["M0843-L-CHUNK-AVERAGE-STEP-03", "M0843-L-CHUNK-AVERAGE-STEP-04"], "Combine both directions into average_density_near_total_density.", "Regularity/Chunk.lean:318-357", "Absolute average-density error at most epsilon."),
    ],
    "M0843-L-DENSITY-STAR": [
        (["M0843-L-CHUNK-AVERAGE"], "Bound the density of the union of star parts near the selected witness density.", "Regularity/Chunk.lean:362-373", "Star-union density error at most epsilon."),
        (["M0843-C-CHUNK-WITNESSES", "M0843-L-CHUNK-CARD"], "Use the graph-cardinality bound to prove epsilon <= card star / card chunk.parts.", "Regularity/Chunk.lean:374-416", "The star family is a sufficiently large fraction."),
        (["M0843-L-DENSITY-STAR-STEP-01", "M0843-L-DENSITY-STAR-STEP-02"], "Combine witness density separation, containment, and size to obtain a nonuniform star rectangle.", "Regularity/Chunk.lean:417-452", "edgeDensity_star_not_uniform."),
    ],
    "M0843-L-CHUNK-AUX": [
        (["M0843-L-CHUNK-AVERAGE"], "If the old density is small, compare its square with epsilon^5/25 and use square nonnegativity.", "Regularity/Chunk.lean:341-346", "The auxiliary inequality in the small-density branch."),
        (["M0843-L-CHUNK-AVERAGE", "M0843-L-CHUNK-CARD"], "Otherwise lower-bound the average chunk density by old density minus epsilon^5/50 and normalize the chunk counts.", "Regularity/Chunk.lean:347-360", "The auxiliary squared-average inequality."),
    ],
    "M0843-L-NONUNIFORM-COUNT": [
        (["frozen-nonuniform-partition-context"], "Unfold Finpartition.IsUniform and negate the cardinal inequality.", "Regularity/Uniform.lean:196-235; Regularity/Increment.lean:159", "A strict lower bound on the number of nonuniform ordered pairs."),
        (["M0843-L-NONUNIFORM-COUNT-STEP-01"], "Rewrite offDiag cardinality and use 7 <= card P.parts.", "Regularity/Increment.lean:170-180", "A 6/7 fraction lower bound for off-diagonal pairs."),
        (["M0843-L-NONUNIFORM-COUNT-STEP-01", "M0843-L-NONUNIFORM-COUNT-STEP-02"], "Normalize coefficients and multiply by epsilon powers.", "Regularity/Increment.lean:171-182", "The epsilon^5/4 contribution is covered by nonuniform-pair gain minus loss."),
    ],
    "M0843-L-ENERGY-COE": [
        (["frozen-finpartition-context"], "Expand rational energy as the normalized sum of squared edge densities.", "Regularity/Energy.lean:38-41", "A rational normalized off-diagonal sum."),
        (["M0843-L-ENERGY-COE-STEP-01"], "Cast numerator, denominator, sums, and squares into the ordered field.", "Regularity/Energy.lean:59-63", "Finpartition.coe_energy."),
    ],
    "M0843-L-ENERGY-SUM": [
        (["M0843-C-DISTINCT-DISJOINT"], "Apply sum_biUnion to replace the nested old-pair/chunk-pair sum by its union.", "Regularity/Increment.lean:149-156", "A sum over the union of distinctPairs families."),
        (["M0843-C-DISTINCT-CONTAIN"], "Use containment and square nonnegativity to compare the union sum with the full increment offDiag sum.", "Regularity/Increment.lean:153-157", "The global new-partition sum upper bound."),
    ],
}


def semantic_ledger(row: dict) -> list[dict]:
    oid = row["id"]
    if oid not in LEAF_LEDGERS:
        return ledger(row)
    result = []
    for index, (premises, inference, locator, step_output) in enumerate(LEAF_LEDGERS[oid], 1):
        result.append({
            "step_id": f"{oid}-STEP-{index:02d}",
            "premise_ids": premises,
            "inference": inference,
            "source_locator": locator,
            "output": step_output,
            "outgoing_use": row["output"] if index == len(LEAF_LEDGERS[oid]) else f"{oid}-STEP-{index + 1:02d}",
        })
    return result


nodes = []
for row, obligation in zip(SPECS, obligations):
    oid = row["id"]
    is_candidate_body = oid not in {"M0843-S-TARGET", "M0843-S-BOUNDARY", "M0843-S-FOUNDATION"} and oid not in MACHINE_SPECIAL
    nodes.append({
        "node_id": THEOREM + "-" + oid.removeprefix(PREFIX),
        "obligation_id": oid,
        "kind": row["kind"],
        "human_statement": row["claim"],
        "formal_target": row["formal"],
        "output": row["output"],
        "human_debt": "H1" if obligation["human_source_eligibility"] == "required" else "H2",
        "machine_debt": "M3" if obligation["machine_eligibility"] != "not_applicable" else "M5",
        "readability_debt": "R4",
        "evidence_ids": ["M0843-C01-E2-UNACCEPTED"] if is_candidate_body else [],
        "source_crosswalk_id": "SRC-M0843-ITP2022-PARTIAL" if obligation["human_source_eligibility"] == "required" else "not-applicable",
        "provenance_id": "PROV-M0843-C01-PARTIAL" if is_candidate_body else "none",
        "foundation_profile": "Lean4-mathlib-classical candidate: propext, Classical.choice, Quot.sound; acceptance open",
        "tcb_profile": "Lean-4.29.0+mathlib-8a178386; transitive declaration and release closure open",
        "computation_record": "none; no external computation, native evaluation, certificate, or oracle closes this node",
        "step_budget": row["budget"],
        "semantic_step_ledger": semantic_ledger(row),
        "public_readable_target": f"Stage1_Instances/THM-M-0843/obligation-tree.md#{oid.lower()}",
        "validation_spec_id": "VAL-M0843-OBLIGATION-BUNDLE",
        "status_boundary": "Frozen architecture and unaccepted E2 candidate mapping only; no M0, E1, H0, R0, proof acceptance, audit completion, or theorem completion is credited.",
        "task_ids": [ITEM],
        "owned_sources": ["Stage1_Instances/THM-M-0843/ObligationTree.lean"] if oid in {"M0843-ROOT", "M0843-T-ADAPTER", "M0843-T-UPSTREAM"} else [],
        "owner": "THM-M-0843 execution lane",
        "reviewer": "independent Stage1 integration lane",
        "validity": {
            "validated_at": "2026-07-13",
            "review_due": "before proof acceptance",
            "invalidation_inputs": ["statement hash", "anchor hash", "registry hash", "mathlib revision", "terminal body", "toolchain"],
            "revocation_state": "not-accepted",
        },
    })


def edge(eid: str, source: str, typ: str, target: str, reciprocal: str | None = None) -> dict:
    result = {"edge_id": eid, "from": source, "type": typ, "to": target}
    if reciprocal is not None:
        result["reciprocal_edge_id"] = reciprocal
    return result


proof = []
for parent, children in REQUIRES.items():
    for child in children:
        req = "REQ-" + parent + "-" + child
        comp = "CMP-" + child + "-" + parent
        reverse_type = "composes" if parent == "M0843-ROOT" else "logical_decomposition"
        proof.extend([
            edge(req, parent, "proof_requires", child, comp),
            edge(comp, child, reverse_type, parent, req),
        ])

workflow_tasks = [
    "S56-M-0843-ANCHOR_AUDIT", ITEM, "S56-M-0843-PROOF",
    "S56-M-0843-VALIDATION", "S56-M-0843-RELEASE",
]
graph_edges = {
    "proof": proof,
    "refinement": [
        edge("REF-ROOT-TARGET", "M0843-ROOT", "logical_decomposition", "M0843-S-TARGET"),
        edge("REF-ROOT-BOUNDARY", "M0843-ROOT", "logical_decomposition", "M0843-S-BOUNDARY"),
    ],
    "provenance": [],
    "evidence": [],
    "trust": [
        edge("TRUST-FOUNDATION", "M0843-ROOT", "trusts", "M0843-S-FOUNDATION"),
        edge("TRUST-RELEASE", "M0843-ROOT", "trusts", "M0843-X-TRUST"),
    ],
    "documentation": [],
    "workflow": [
        edge("FLOW-TREE-ANCHOR", ITEM, "workflow_depends_on", "S56-M-0843-ANCHOR_AUDIT"),
        edge("FLOW-PROOF-TREE", "S56-M-0843-PROOF", "workflow_depends_on", ITEM),
        edge("FLOW-VALIDATION-PROOF", "S56-M-0843-VALIDATION", "workflow_depends_on", "S56-M-0843-PROOF"),
        edge("FLOW-RELEASE-VALIDATION", "S56-M-0843-RELEASE", "workflow_depends_on", "S56-M-0843-VALIDATION"),
    ],
}

for oid in ids:
    if oid != "M0843-X-SOURCE" and next(
        row["human_source_eligibility"] for row in obligations
        if row["obligation_id"] == oid
    ) == "required":
        graph_edges["provenance"].append(
            edge("SOURCE-MAP-" + oid, oid, "source_map", "M0843-X-SOURCE")
        )
    if oid not in {"M0843-X-PROVENANCE", "M0843-X-SOURCE", "M0843-X-TRUST"}:
        graph_edges["provenance"].append(
            edge("PROVENANCE-" + oid, "M0843-X-PROVENANCE", "provenance_of", oid)
        )
        graph_edges["evidence"].append(
            edge("EVIDENCE-" + oid, "M0843-X-PROVENANCE", "evidence_for", oid)
        )
    if oid != "M0843-X-SOURCE":
        graph_edges["documentation"].append(
            edge("DOCUMENT-" + oid, "M0843-X-SOURCE", "documents", oid)
        )

graphs = {}
for name, edges in graph_edges.items():
    incoming: dict[str, list[str]] = {}
    outgoing: dict[str, list[str]] = {}
    for item in edges:
        outgoing.setdefault(item["from"], []).append(item["edge_id"])
        incoming.setdefault(item["to"], []).append(item["edge_id"])
    graphs[name] = {"edges": edges, "out": outgoing, "in": incoming}

composition_certificates = []
decomposition_plans = []
for parent, children in REQUIRES.items():
    if parent == "M0843-ROOT":
        declaration = "Stage1Instances.THM_M_0843_Obligations.compose_root"
        kind = "lean_abstract_child_harness"
        composition_certificates.append({
            "certificate_id": "COMP-" + parent,
            "parent_obligation_id": parent,
            "parent_statement_fingerprint": next(
                row["statement_fingerprint"] for row in obligations
                if row["obligation_id"] == parent
            ),
            "required_child_ids": children,
            "required_child_statement_fingerprints": {
                child: next(
                    row["statement_fingerprint"] for row in obligations
                    if row["obligation_id"] == child
                ) for child in children
            },
            "checked_declaration": declaration,
            "certificate_kind": kind,
            "status": "provisionally_elaborated_not_accepted",
            "introduces_undeclared_premises": False,
        })
        continue
    if parent == "M0843-L-ENERGY-INCREMENT":
        declaration = "SzemerediRegularity.energy_increment"
    else:
        declaration = "szemeredi_regularity"
    decomposition_plans.append({
        "plan_id": "DECOMP-" + parent,
        "parent_obligation_id": parent,
        "planned_child_ids": children,
        "source_declaration": declaration,
        "status": "source_body_decomposition_unverified_as_child_to_parent_composition",
        "required_future_certificate": "An exact abstract-child harness must bind these fingerprints and consume every child before parent closure.",
    })

proof_children = {child for children in REQUIRES.values() for child in children}
proof_parents = set(REQUIRES)
proof_leaves = sorted(proof_children - proof_parents)
bundle = {
    "schema_version": "stage1-typed-graphs/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "registry_id": registry["registry_id"],
    "registry_denominator_sha256": denominator,
    "root_node_id": "THM-M-0843-ROOT",
    "edge_direction": "Proof requirements run parent to child; reciprocal composes edges run child to parent. Workflow dependencies run task to prerequisite.",
    "workflow_task_nodes": workflow_tasks,
    "nodes": nodes,
    "graphs": graphs,
    "composition_certificates": composition_certificates,
    "unverified_decomposition_plans": decomposition_plans,
    "closure_boundary": {
        "closed_obligations": [],
        "root_closed": False,
        "accepted_root_machine_debt": "M3",
        "audit_complete": False,
        "theorem_complete": False,
        "proof_leaf_cut_set": proof_leaves,
        "remaining_release_cut_set": ["M0843-X-SOURCE", "M0843-X-PROVENANCE", "M0843-X-TRUST", "R0 reconstruction", "hermetic replay", "independent verification", "master acceptance"],
        "distinct_known_terminal_body_ids": sorted({row["terminal_proof_body_id"] for row in obligations if row["terminal_proof_body_id"]}),
        "candidate_evidence": "M0843-C01/E2 is exact and locally checked but not an E1 accepted proof receipt.",
        "reason": "This phase freezes and structurally checks the architecture. Only the exact root composition harness is checked; all internal source decompositions require future exact composition certificates. The downstream proof phase must obtain node-specific accepted closure, and the E2 anchor does not close any obligation.",
    },
}

recipes = {
    "schema_version": "stage1-validation-specs/1.0",
    "item_id": ITEM,
    "theorem_id": THEOREM,
    "recipes": [{
        "recipe_id": "VAL-M0843-OBLIGATION-BUNDLE",
        "cwd": ".",
        "argv": ["python3", "-B", "Stage1_Instances/THM-M-0843/check_obligation_tree.py"],
        "env_allowlist": {
            "PATH": "runner-provided tool path",
            "HOME": "runner-provided toolchain home",
            "TMPDIR": "runner-provided temporary directory",
            "PYTHONDONTWRITEBYTECODE": "1"
        },
        "timeout_seconds": 180,
        "network_policy": "denied",
        "covered_obligation_ids": ids,
        "covered_declarations": [
            "Stage1Instances.THM_M_0843.SzemerediRegularityTarget",
            "szemeredi_regularity",
            "Stage1Instances.THM_M_0843_Obligations.terminal_adapter",
            "Stage1Instances.THM_M_0843_Obligations.compose_root"
        ],
        "coverage_boundary": "The recipe structurally covers every registry node, but kernel declaration coverage is limited to the four named declarations. Internal node types and child-to-parent compositions remain open.",
        "expected_outputs": [
            {"path_or_stream": "stdout", "semantic_hash_policy": "contains structural PASS line with generated obligation, edge, and ledger counts"},
            {"path_or_stream": "stdout", "semantic_hash_policy": "contains accepted root H1/M3/R4, zero closed obligations, theorem_complete=false"}
        ],
        "expected_exit": 0,
    }],
}

markdown = [
    "# THM-M-0843 frozen obligation architecture",
    "",
    f"Item: `{ITEM}`.",
    "",
    f"Registry version 1 freezes {len(ids)} canonical obligations before proof-phase closure credit.",
    "The proof graph follows the actual pinned `szemeredi_regularity` body through its cardinality",
    "and tolerance splits, energy induction, increment construction, chunk-density engine, terminal",
    "body, and exact adapter. Typed provenance, evidence, trust, documentation, and workflow edges",
    "are separate and cannot act as proof premises.",
    "",
    "## Proof route",
    "",
    "The full planned reciprocal edge set is in `typed-graphs.json`. Only the root's exact abstract-",
    "child composition is checked in this phase; every internal relation remains an explicitly",
    "unverified source-body decomposition until an exact child-to-parent harness is accepted. The",
    "main route is:",
    "",
    "```text",
    "ROOT -> exact adapter -> pinned upstream body -> cardinality split",
    "  small graph -> bottom singleton equipartition",
    "  large graph -> bounds -> tolerance split",
    "    epsilon >= 1 -> initial equipartition is uniform",
    "    epsilon <= 1 -> energy invariant -> zero/successor branches",
    "      nonuniform successor -> iteration bounds -> increment",
    "        equipartition + cardinality + energy increment",
    "          chunk refinement + distinct pairs + density + count + sum recomposition",
    "    terminal floor-plus-one energy contradiction",
    "```",
    "",
    "## Node ledger",
    "",
]
for row in SPECS:
    markdown.extend([
        f"### {row['id'].lower()}",
        "",
        row["claim"],
        "",
        f"Formal target: `{row['formal']}`. Output: {row['output']} Source boundary: {row['source']}.",
        f"Budget: {row['budget']} substantive steps maximum; structured ledger: {len(semantic_ledger(row))} recorded step(s).",
        "",
    ])
markdown.extend([
    "## Freeze boundary",
    "",
    "All machine obligations remain open at accepted `M3`. Candidate `M0843-C01` is exact, pinned,",
    "sorry-free, and locally elaborated at `E2`, but rev-5.6 requires an accepted `E1` receipt before",
    "`M0-W`; the downstream proof task and master acceptance are therefore not preempted. Primary-source",
    "`H0`, readable `R0`, transitive provenance/TCB, hermetic replay, independent verification, audit",
    "completion, and theorem completion remain open. Any architectural or eligibility change requires",
    "a new registry version and append-only delta.",
    "",
])

outputs = {
    "obligation-registry.json": json.dumps(registry, indent=2, ensure_ascii=True) + "\n",
    "typed-graphs.json": json.dumps(bundle, indent=2, ensure_ascii=True) + "\n",
    "validation-specs.json": json.dumps(recipes, indent=2, ensure_ascii=True) + "\n",
    "obligation-tree.md": "\n".join(markdown),
}
for name, content in outputs.items():
    (HERE / name).write_text(content, encoding="utf-8")

print(f"wrote {len(ids)} obligations and {sum(len(graph['edges']) for graph in graphs.values())} typed edges")
print(f"registry denominator sha256: {denominator}")
