#!/usr/bin/env bash
set -euo pipefail

lake env lean ../../Stage1_Instances/THM-M-0401/Statement.lean
lake env lean ../../Stage1_Instances/THM-M-0401/Proof.lean
