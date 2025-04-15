from mcp.server.fastmcp import FastMCP, Context
from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM
from typing import Dict, Any
import asyncio

# You may move this to a shared app instance if reused across multiple tools
app = MCPApp(name="hazard_analyzer")

def register_hazard_analyzer_tool(mcp: FastMCP):
    @mcp.tool()
    async def hazard_analyzer(ctx: Context, task_description: str) -> Dict[str, Any]:
        """
        Generates multiple possible hazard scenarios based on input,
        then asks the user to select the most relevant one.
        """
        prompt = f"""
You are a hazard analysis assistant specialized in construction safety.

Given the following task description:

"{task_description}"

Generate a list of 5 realistic and dangerous construction scenarios related to collision risks caused by equipment. Each item should be:
- 1 sentence long
- Clear, realistic, and specific
- Ordered from most to least probable

Number each item.
"""
        try:
            app = ctx.app
            llm = await ctx.get_llm()
            result = await llm.generate_str(prompt)

            # 리스트 파싱
            scenarios = result.strip().split("\n")
            scenarios = [s.strip("12345. ") for s in scenarios if s.strip()]

            # 사용자 입력 요청
            selected = await ctx.await_human_input({
                "prompt": "Which scenario should we simulate?",
                "description": "Please select one of the following scenarios to simulate:",
                "metadata": {"options": scenarios}
            })

            selected_index = int(selected) - 1 if selected.isdigit() else 0
            selected_scenario = scenarios[selected_index]

            return {
                "success": True,
                "message": f"Selected hazard: {selected_scenario}",
                "data": {
                    "selected": selected_scenario,
                    "all": scenarios
                }
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Hazard analyzer error: {str(e)}"
            }
