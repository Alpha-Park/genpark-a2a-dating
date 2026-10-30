# -*- coding: utf-8 -*-
"""
GenPark A2A Dating MCP Server
FastMCP standard interface for multi-attribute affinity and Gale-Shapley stable matching.
"""

import json
from typing import Dict, Any, List
from client import GenParkA2aDating

try:
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("genpark-a2a-dating")
except ImportError:
    class MockFastMCP:
        def __init__(self, name):
            self.name = name
        def tool(self):
            def decorator(f):
                return f
            return decorator
    mcp = MockFastMCP("genpark-a2a-dating")

dating = GenParkA2aDating()

@mcp.tool()
def compute_multi_attribute_affinity_score(
    agent_a: Dict[str, Any],
    agent_b: Dict[str, Any]
) -> str:
    """
    Computes compatibility affinity between two autonomous agents.
    """
    res = dating.compute_multi_attribute_affinity_score(agent_a, agent_b)
    return json.dumps(res, indent=2)

@mcp.tool()
def solve_gale_shapley_stable_matching(
    proposers_preferences: Dict[str, List[str]],
    receivers_preferences: Dict[str, List[str]]
) -> str:
    """
    Solves the classic Gale-Shapley Deferred Acceptance algorithm for two groups.
    """
    res = dating.solve_gale_shapley_stable_matching(proposers_preferences, receivers_preferences)
    return json.dumps(res, indent=2)

@mcp.tool()
def audit_match_stability_and_blocking_pairs(
    matches: Dict[str, str],
    proposers_preferences: Dict[str, List[str]],
    receivers_preferences: Dict[str, List[str]]
) -> str:
    """
    Audits a given matching for blocking pairs to verify Nash stability.
    """
    res = dating.audit_match_stability_and_blocking_pairs(matches, proposers_preferences, receivers_preferences)
    return json.dumps(res, indent=2)

def main():
    print("Testing A2A Dating:")
    p = {"A": ["X", "Y"]}
    r = {"X": ["A"], "Y": ["A"]}
    print(solve_gale_shapley_stable_matching(p, r))

if __name__ == "__main__":
    main()
