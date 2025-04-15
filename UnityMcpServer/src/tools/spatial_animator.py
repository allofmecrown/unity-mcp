from mcp.server.fastmcp import FastMCP, Context
from typing import Dict, Any, List
import json
from pathlib import Path

PREFAB_JSON_PATH = Path("Assets/prefabs/prefab_definitions.json")  # Unity 프로젝트 안의 경로

def load_prefab_definitions():
    with open(PREFAB_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def register_spatial_animator(mcp: FastMCP):
    @mcp.tool()
    def handle_spatial_animation(ctx: Context) -> Dict[str, Any]:
        """Given selected objects and hazard context, assigns position, rotation, and animation."""
        try:
            hazard = ctx.session.memory.get("selected_hazard")
            objects = ctx.session.memory.get("selected_objects")

            if not hazard or not objects:
                return {"success": False, "message": "Missing hazard or selected_objects in context."}

            prefab_defs = {obj["name"]: obj for obj in load_prefab_definitions()}

            layout: List[Dict[str, Any]] = []
            base_x, base_z = 0, 0

            for i, obj_name in enumerate(objects):
                prefab = prefab_defs.get(obj_name)
                if not prefab:
                    continue

                # 예시 배치 로직 (X축으로 일정 간격 벌림)
                pos = [base_x + i * 3.0, 0.0, base_z]
                rot = [0.0, 180.0 if "worker" in obj_name.lower() else 0.0, 0.0]

                # 애니메이션 선택 (hazard 내용 + prefab animation 필드 기반)
                animations = prefab.get("animation", [])
                selected_anim = None
                for anim in animations:
                    if "walk" in anim and "approach" in hazard.lower():
                        selected_anim = anim
                        break
                    elif "idle" in anim:
                        selected_anim = anim

                layout.append({
                    "name": obj_name,
                    "position": pos,
                    "rotation": rot,
                    "animation": selected_anim
                })

            ctx.session.memory["final_object_layout"] = layout

            return {
                "success": True,
                "message": f"{len(layout)} objects processed for spatial layout.",
                "data": layout
            }

        except Exception as e:
            return {"success": False, "message": f"Spatial reasoning error: {str(e)}"}
