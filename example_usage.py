# -*- coding: utf-8 -*-
from client import GenParkA2aDating

a2a = GenParkA2aDating()

agent_1 = {
    "id": "buyer_agent_alpha",
    "offered_skills": ["solidity_audit", "zk_verify"],
    "needed_skills": ["compute_inference", "vector_search"],
    "sla_latency_ms": 120.0,
    "trust_score": 0.95
}

agent_2 = {
    "id": "seller_agent_beta",
    "offered_skills": ["compute_inference", "vector_search"],
    "needed_skills": ["solidity_audit"],
    "sla_latency_ms": 140.0,
    "trust_score": 0.92
}

# 1. Multi-Attribute Affinity
affinity = a2a.compute_multi_attribute_affinity_score(agent_1, agent_2)
print(f"Agent Affinity: Score={affinity['composite_affinity_score']} ({affinity['match_tier']})")
print(f"  Skill Complementarity: {affinity['skill_complementarity']}, Latency: {affinity['latency_alignment']}")

# 2. Gale-Shapley Stable Matching
proposers = {
    "agent_p1": ["rec_r1", "rec_r2", "rec_r3"],
    "agent_p2": ["rec_r2", "rec_r1", "rec_r3"],
    "agent_p3": ["rec_r1", "rec_r3", "rec_r2"]
}
receivers = {
    "rec_r1": ["agent_p2", "agent_p1", "agent_p3"],
    "rec_r2": ["agent_p1", "agent_p2", "agent_p3"],
    "rec_r3": ["agent_p1", "agent_p2", "agent_p3"]
}

matching = a2a.solve_gale_shapley_stable_matching(proposers, receivers)
print()
print(f"Gale-Shapley Stable Matches: {matching['stable_pairings']}")

# 3. Stability Audit
audit = a2a.audit_match_stability_and_blocking_pairs(matching['stable_pairings'], proposers, receivers)
print()
print(f"Matching Stability: IsStable={audit['is_nash_stable']} ({audit['stability_status']}, BlockingPairs={audit['blocking_pairs_count']})")
