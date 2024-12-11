from autogen import ConversableAgent
import autogen

# Configure Gemini models
config_list_gemini = autogen.config_list_from_json("config.json")

# Agent 1: Enhancer
SYSTEM_MESSAGE_ENHANCER = """
Your task is to enhance the clarity and comprehensibility of the user's prompt. 
Take the initial prompt and rewrite it to make it more detailed and understandable. 
Focus on improving the structure and clarity without changing the original intent.
"""

enhancer_agent = ConversableAgent(
    name="Prompt Enhancer",
    system_message=SYSTEM_MESSAGE_ENHANCER,
    llm_config={"config_list": config_list_gemini},
    code_execution_config=False,
    human_input_mode="NEVER",
    function_map=None
)

# Agent 2: Code Generator
SYSTEM_MESSAGE_CODE_GENERATOR = """
Your task is to generate executable code based on the enhanced prompt provided to you. 
You should produce three functions that fulfill the user's request. 
Ensure the code is well-structured, efficient, and properly documented.
"""

code_generator_agent = ConversableAgent(
    name="Code Generator",
    system_message=SYSTEM_MESSAGE_CODE_GENERATOR,
    llm_config={"config_list": config_list_gemini},
    code_execution_config=False,
    human_input_mode="NEVER",
    function_map=None
)

# Agent 3: Code Evaluator
SYSTEM_MESSAGE_CODE_EVALUATOR = """
Your task is to evaluate the generated code snippets from the Code Generator. 
Select the best or most optimal solution based on clarity, efficiency, and functionality. 
Provide a brief explanation of why you chose this particular code snippet.
"""

code_evaluator_agent = ConversableAgent(
    name="Code Evaluator",
    system_message=SYSTEM_MESSAGE_CODE_EVALUATOR,
    llm_config={"config_list": config_list_gemini},
    code_execution_config=False,
    human_input_mode="NEVER",
    function_map=None
)

# User input
user_prompt = "I need functions to sort a list, filter even numbers, and calculate the sum."

# Step 1: Enhance the user prompt
enhanced_prompt_reply = enhancer_agent.generate_reply(
    messages=[{"content": user_prompt, "role": "user"}]
)

# Step 2: Generate code based on enhanced prompt
code_generation_reply = code_generator_agent.generate_reply(
    messages=[{"content": enhanced_prompt_reply["content"], "role": "user"}]
)

# Step 3: Evaluate generated code
code_evaluation_reply = code_evaluator_agent.generate_reply(
    messages=[{"content": "\n".join(code_generation_reply["content"]), "role": "user"}]
)

# Output the final evaluation
print(code_evaluation_reply["content"])