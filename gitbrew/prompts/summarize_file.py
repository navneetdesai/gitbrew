class SummarizeFilePrompt:
    template = """
    The end goal is for an LLM to generate a Readme for a Github repository based on individual summaries of code files.
    To achieve this, summarize the following file named {filename}: {content}. 
    """
