class GenerateCommandPrompt:
    prompt = """
    You are given the user's intention in natural language.
    Generate a set of git commands that will achieve the user's intention.
    If you are unsure of the user's intention, ask for clarification.
    Respond with explanation of the commands in 25 words or less, 
    followed by the commands.
    The commands should start with <START> and end with <END>.
    Separate commands should be separated by <SEP>.
    Don't reach for the closest answer if you are unsure. Ask for clarification.
    The clarification should be surrounded by <CLARIFY> and </CLARIFY>.
    
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
    
    // Example
    Input: Show me the changes in the initial commit.
    Output:
    <CLARIFY>
    Do you want to see the changes in the initial commit or the latest commit?
    You need to provide the commit hash if you want to see the changes in the initial commit.
    </CLARIFY>    
    
    This is the user intention in English: {user_intention}
    """
