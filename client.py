# -*- coding: utf-8 -*-
"""
GenPark A2A Dating Client
Pure Python Standard Library (Zero External Dependencies)
Implements agent-to-agent multi-attribute affinity vector scoring,
Gale-Shapley Deferred Acceptance stable matching, and blocking pair equilibrium auditing.
"""

import math
from typing import Dict, Any, List, Optional

class GenParkA2aDating:
    """
    Autonomous agent capability matchmaking and stable contract pairing engine.
    """

    def __init__(self):
        pass

    def compute_multi_attribute_affinity_score(
        self,
        agent_a: Dict[str, Any],
        agent_b: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Computes compatibility affinity between two autonomous agents based on
        domain overlap, latency tolerance, trust rating, and complementary skill coverage.
        """
        # Skill complementarity (Jaccard similarity on required vs offered skills)
        offered_a = set(agent_a.get("offered_skills", []))
        needed_b = set(agent_b.get("needed_skills", []))
        coverage_ab = len(offered_a.intersection(needed_b)) / max(1, len(needed_b)) if needed_b else 1.0

        offered_b = set(agent_b.get("offered_skills", []))
        needed_a = set(agent_a.get("needed_skills", []))
        coverage_ba = len(offered_b.intersection(needed_a)) / max(1, len(needed_a)) if needed_a else 1.0

        skill_score = (coverage_ab + coverage_ba) / 2.0

        # Latency alignment
        lat_a = float(agent_a.get("sla_latency_ms", 100.0))
        lat_b = float(agent_b.get("sla_latency_ms", 100.0))
        lat_diff = abs(lat_a - lat_b)
        latency_score = max(0.0, 1.0 - (lat_diff / 500.0))

        # Trust score alignment
        trust_a = float(agent_a.get("trust_score", 0.9))
        trust_b = float(agent_b.get("trust_score", 0.9))
        trust_score = min(trust_a, trust_b)

        # Composite affinity
        composite = (skill_score * 0.45) + (latency_score * 0.25) + (trust_score * 0.30)
        composite = round(composite, 4)

        if composite >= 0.85:
            match_tier = "OPTIMAL_COLLABORATIVE_PARTNER"
        elif composite >= 0.65:
            match_tier = "ACCEPTABLE_COOPERATION"
        else:
            match_tier = "INCOMPATIBLE_CAPABILITIES"

        return {
            "agent_a_id": agent_a.get("id", "agent_a"),
            "agent_b_id": agent_b.get("id", "agent_b"),
            "composite_affinity_score": composite,
            "match_tier": match_tier,
            "skill_complementarity": round(skill_score, 3),
            "latency_alignment": round(latency_score, 3),
            "trust_alignment": round(trust_score, 3)
        }

    def solve_gale_shapley_stable_matching(
        self,
        proposers_preferences: Dict[str, List[str]],
        receivers_preferences: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """
        Solves the classic Gale-Shapley Deferred Acceptance algorithm for two equal groups,
        guaranteeing a stable matching without blocking pairs.
        """
        free_proposers = list(proposers_preferences.keys())
        # Track which receiver each proposer has proposed to
        proposals_made = {p: 0 for p in free_proposers}
        # Matches: receiver -> proposer
        matches = {}

        # Precompute receiver rankings for O(1) comparison
        receiver_rankings = {}
        for r, prefs in receivers_preferences.items():
            receiver_rankings[r] = {p: rank for rank, p in enumerate(prefs)}

        while free_proposers:
            p = free_proposers.pop(0)
            p_prefs = proposers_preferences[p]
            prop_idx = proposals_made[p]

            if prop_idx < len(p_prefs):
                r = p_prefs[prop_idx]
                proposals_made[p] += 1

                if r not in matches:
                    # Receiver is currently unmatched
                    matches[r] = p
                else:
                    current_p = matches[r]
                    # Compare rankings
                    r_ranks = receiver_rankings.get(r, {})
                    rank_new = r_ranks.get(p, 9999)
                    rank_curr = r_ranks.get(current_p, 9999)

                    if rank_new < rank_curr:
                        # Receiver prefers new proposer
                        matches[r] = p
                        free_proposers.append(current_p)
                    else:
                        # Receiver rejects proposal
                        free_proposers.append(p)

        # Invert to proposer -> receiver
        final_pairings = {p: r for r, p in matches.items()}

        return {
            "matching_complete": True,
            "total_matches": len(final_pairings),
            "stable_pairings": final_pairings
        }

    def audit_match_stability_and_blocking_pairs(
        self,
        matches: Dict[str, str],
        proposers_preferences: Dict[str, List[str]],
        receivers_preferences: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """
        Audits a given matching for blocking pairs:
          A pair (p, r) is a blocking pair if p prefers r to their match AND r prefers p to their match.
        """
        blocking_pairs = []
        receiver_to_proposer = {r: p for p, r in matches.items()}

        for p, p_prefs in proposers_preferences.items():
            current_r = matches.get(p)
            if current_r not in p_prefs:
                continue
            p_current_rank = p_prefs.index(current_r)

            # Check all receivers p prefers over current_r
            preferred_receivers = p_prefs[:p_current_rank]
            for r in preferred_receivers:
                r_prefs = receivers_preferences.get(r, [])
                r_current_p = receiver_to_proposer.get(r)
                if r_current_p in r_prefs:
                    r_current_rank = r_prefs.index(r_current_p)
                    if p in r_prefs and r_prefs.index(p) < r_current_rank:
                        blocking_pairs.append({"proposer": p, "receiver": r})

        is_stable = len(blocking_pairs) == 0

        return {
            "is_nash_stable": is_stable,
            "blocking_pairs_count": len(blocking_pairs),
            "blocking_pairs": blocking_pairs,
            "stability_status": "STABLE_EQUILIBRIUM" if is_stable else "UNSTABLE_DEVIATION_HAZARD"
        }
