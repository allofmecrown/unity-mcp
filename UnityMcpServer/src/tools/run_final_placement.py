from mcp.server.fastmcp import FastMCP, Context
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM

def register_run_placement_agent(mcp: FastMCP):

    @mcp.tool()
    async def run_final_placement(ctx: Context) -> dict:
        """
        Reads the final_object_layout and lets Claude complete the placement using Unity tools.
        """
        layout = ctx.session.memory.get("final_object_layout")

        if not layout:
            return {"success": False, "message": "final_object_layout not found."}

        # Claude용 프롬프트 생성
        prompt = "Place the following objects in Unity using manage_gameobject.\n\n"
        for obj in layout:
            name = obj["name"]
            pos = obj["position"]
            rot = obj["rotation"]
            anim = obj.get("animation")
            prompt += f"- Object: {name}\n"
            prompt += f"  - Position: {pos}\n"
            prompt += f"  - Rotation: {rot}\n"
            if anim:
                prompt += f"  - Animation: {anim}\n"
            prompt += "\n"

        # Claude에게 넘길 agent 구성
        agent = Agent(
            name="placement_agent",
            instruction="Use Unity tools to place each object into the scene based on the provided layout.",
            server_names=["manage_gameobject"],  # 여기에 필요한 MCP 툴만 노출
        )

        async with agent:
            llm = await agent.attach_llm(OpenAIAugmentedLLM)
            result = await llm.generate_str(message=prompt)
            return {
                "success": True,
                "message": "Placement executed.",
                "data": result
            }
