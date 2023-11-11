class GenerateCommandPrompt:
    prompt = """
    You are given the user's intention in natural language.
    Generate a set of git commands that will achieve the user's intention. These commands should be surrounded by <START> and <END>.
    Separate commands should be separated by <SEP>.
    
    If you are unsure of the user's intention, ask for clarification. If a git command needs information like branch name, URL, commit message or anything else, ask the user for it as a clarification.
    The clarification should be surrounded by <CLARIFY> and </CLARIFY>.
    For example, do not return `git rebase <branch_name>`. Instead ask for the branch name and then return `git rebase feature1`.
    
    // Example
    Input: Stage all changes and add to commit
    Output: <CLARIFY> What should be the commit message </CLARIFY>
    Input: Initial commit
    Output: git commit -m "Initial commit"
    
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
    
    // Example
    Input: Clone a repository
    Output:
    <CLARIFY>
    Provide the remote repository URL.
    </CLARIFY>
    
    
    This is the user intention in English: {user_intention}
    """
