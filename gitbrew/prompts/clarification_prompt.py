class ClarificationPrompt:
    """
    Prompt the LLM with the clarification provided by the user
    and the original conversation.
    `conversation` is the conversation between the user
    with the prompts and the clarification provided by the user.
    """

    template = "This is our conversation: `{conversation}`. Based on the clarification provided, generate the git commands."
