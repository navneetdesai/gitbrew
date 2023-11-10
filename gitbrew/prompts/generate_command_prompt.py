class GenerateCommandPrompt:
    prompt = """
    You are given the user's intention in natural language.
    Generate a set of git commands that will achieve the user's intention.
    If you are unsure of the user's intention, ask for clarification.
    Respond with explanation of the commands in 25 words or less, 
    followed by the commands.
    The commands should start with <START> and end with <END>.
    Separate commands should be separated by <SEP>.
    
    // Example
    Input: Add all changes to a commit and push to the remote repository. 
            The commit message is "Create components for the UI." 
    Output:
    <START>
    git add .
    <SEP>
    git commit -m "Create components for the UI."
    <SEP>
    git push origin    
    <END>
    This is the user intention in English: {user_intention}
    """
