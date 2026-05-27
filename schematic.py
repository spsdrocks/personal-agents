import os
import json
import anthropic

# Client

anthropic_client = anthropic.Anthropic()



# Tool Definitions

agent_tools = [
    {
        "name" : "tool_name",
        "description" : "Description for client to read",
        "input_schema" : {
            "type" : "input type",
            "properties" : {
                "variable_name" : {"type" : "input type", "description" : "Description for client to read"}
            },
            "required" : []   # Use to list required inputs
        }
    }
]



# Tool Implementations

def tool_name(variable_name: str) -> str:   # Replace with real variable
    return

def run_tool(name: str, inputs: dict) -> str:
    if name == "tool_name":
        return tool_name(inputs["variable_name"])
    # Add more tools here as elif statements
    return "Unknown tool"



# Agent Definition

def run_agent(agent_task: str):   #Add other parameters for different tool properties
    agent_behaviour = f""""""   # Here write the instructions for your agent describing it's general purpose and the rules it should abide by

    input_message = [{"role" : "user", "content" : agent_task}]

    print(f"...")   # Inform user that agent is active/running

    while True:
        agent_response = anthropic_client.messages.create(
            model = "claude-sonnet-4-6",   # Replace with desired model
            max_tokens = 4096,   # Change as desired
            system = agent_behaviour,
            tools = agent_tools,
            messages = input_message
        )

        input_message.append({"role" : "Agents role/title", "content" : agent_response.content})

        if agent_response.stop_reason == "end_turn":
            for response_block in agent_response.content:
                if hasattr(response_block, "text"):
                    print(response_block.text)
            break

        elif agent_response.stop_reason == "tool_use":
            tool_results = []

            for response_block in agent_response.content:
                if response_block.type == "tool_use":
                    print(f"[tool] {response_block.name}({response_block.input})")

                    single_result = run_tool(response_block.name, response_block.input)

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": response_block.id,
                        "content": single_result
                    })

            input_message.append({"role": "user", "content": tool_results})



# Run Agent

if __name__ == "__main__":
    # Add loop to have multiple question -> answer cycles
    run_agent(task="Specific task")   # Add other parameters if used
