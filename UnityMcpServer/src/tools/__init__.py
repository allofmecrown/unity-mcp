from .manage_script import register_manage_script_tools
from .manage_scene import register_manage_scene_tools
from .manage_editor import register_manage_editor_tools
from .manage_gameobject import register_manage_gameobject_tools
from .manage_asset import register_manage_asset_tools
from .read_console import register_read_console_tools
from .execute_menu_item import register_execute_menu_item_tools
from .hazard_analyzer import register_hazard_analyzer_tool
from .object_selector import register_object_selector_tools
from .run_final_placement import register_run_placement_agent
from .spatial_animator import register_spatial_animator


def register_all_tools(mcp):
    """Register all refactored tools with the MCP server."""
    print("Registering Unity MCP Server refactored tools...")
    register_manage_script_tools(mcp)
    register_manage_scene_tools(mcp)
    register_manage_editor_tools(mcp)
    register_manage_gameobject_tools(mcp)
    register_manage_asset_tools(mcp)
    register_read_console_tools(mcp)
    register_execute_menu_item_tools(mcp)
    register_hazard_analyzer_tool(mcp)
    register_object_selector_tools(mcp)
    register_run_placement_agent(mcp)
    register_spatial_animator(mcp)

    print("Unity MCP Server tool registration complete.")
