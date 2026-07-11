#!/usr/bin/env python3
import hashlib
import json
import re
from pathlib import Path


root = Path(__file__).resolve().parent
repo = root.parents[1]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


registry = json.loads((root / "obligation-registry.json").read_text())
graphs = json.loads((root / "typed-graphs.json").read_text())
proof_receipt = json.loads((root / "proof-receipt.json").read_text())

assert registry["theorem_id"] == graphs["theorem_id"] == "THM-M-0393"
assert proof_receipt["item_id"] == "S56-M-0393-PROOF"
assert proof_receipt["exact_declaration"] == \
    "Stage1.THM_M_0393.Proof.finite_pow_divisors"
assert proof_receipt["implemented_obligation_ids"] == ["M0393-N1"]
assert proof_receipt["result"]["root_closed"] is False
assert proof_receipt["result"]["theorem_complete"] is False

expected_hashes = {
    "Statement.lean": "456c62756bc035e675135270bf6984c00bb1203bc6687d3495ae7663131d985f",
    "Proof.lean": "a77c1d1e431a36db1bd8ae48f2511150a2519e3a88a319e84256c88229c3f29f",
    "obligation-registry.json": "57bd847a36b0883078dece89081bff185fae7b74cabf814c01daa7f7e184aa66",
    "typed-graphs.json": "3b6e634f6134346598fee300291daafa13b3d91aa2afc59dad0a66741595ae6c",
    "proof-receipt.json": "b74728f6a34837f467e2bf9beaad0aaeef7894c56c84ac3264ac3209b7372234",
}
for name, expected in expected_hashes.items():
    assert digest(root / name) == expected, f"stale validation input: {name}"

ids = {node["id"] for node in registry["obligations"]}
assert len(ids) == 17 and graphs["proof_graph"]["root"] == "M0393-ROOT"
assert registry["root_vector"] == {"human": "H3", "machine": "M4", "readability": "R3"}
assert registry["theorem_complete"] is False
assert all(node["body"] is None for node in registry["obligations"])
assert all(cert["state"] == "planned_open"
           for cert in graphs["proof_graph"]["composition_certificates"])
assert graphs["evidence_graph"]["evidence_nodes"] == []

reachable = {graphs["proof_graph"]["root"]}
edges = graphs["proof_graph"]["edges"]
while True:
    expanded = reachable | {edge["to"] for edge in edges if edge["from"] in reachable}
    if expanded == reachable:
        break
    reachable = expanded
assert reachable == ids

declarations = {
    "Proof.lean": "finite_pow_divisors",
    "Validation.lean": "independent_finite_pow_divisors",
}
for filename, declaration in declarations.items():
    source = (root / filename).read_text()
    assert re.search(rf"\btheorem\s+{declaration}\b", source)
    assert "{g : Int | g ^ n ∣ m}.Finite" in source
    forbidden = re.compile(
        r"\b(sorry|admit)\b|^[ \t]*(axiom|unsafe)\b", re.MULTILINE
    )
    assert not forbidden.search(source), f"prohibited token in {filename}"

assert digest(repo / "Formalizations/Lean/lean-toolchain") == \
    "651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2"
assert digest(repo / "Formalizations/Lean/lake-manifest.json") == \
    "321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81"

print("validation: ok (independent M0393-N1 finite-choice replay; root H3/M4/R3 open)")
