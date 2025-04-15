# object_selector.py

from mcp.server.fastmcp import FastMCP, Context
from typing import Dict, Any
import json
from pathlib import Path

PREFAB_JSON_PATH = Path("data/prefab_definitions.json")

def load_prefabs():
    with open(PREFAB_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def register_object_selector_tools(mcp: FastMCP):
    """Register tool for selecting necessary objects based on hazard."""

    @mcp.tool()
    def select_objects_from_hazard(ctx: Context, hazard_scenario: str) -> Dict[str, Any]:
        """
        Automatically selects required prefabs based on the given hazard scenario.

        Args:
            hazard_scenario: The selected hazard description (string).

        Returns:
            Dictionary with selected object list.
        """
        try:
            prefabs = load_prefabs()
            selected = []

            for prefab in prefabs:
                # 간단한 예: prefab 이름 또는 애니메이션 스크립트에 hazard 키워드 포함 여부로 판단
                if hazard_scenario.lower() in prefab["name"].lower() or \
                   any(hazard_scenario.lower() in anim.lower() for anim in prefab.get("animation_scripts", [])):
                    selected.append(prefab)

            return {
                "success": True,
                "message": f"{len(selected)} prefab(s) selected based on hazard.",
                "data": selected
            }

        except Exception as e:
            return {"success": False, "message": f"Error selecting objects: {str(e)}"}
