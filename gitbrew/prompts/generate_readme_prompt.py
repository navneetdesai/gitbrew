class GenerateReadmePrompt:
    system_prompt = """
    You are given a summary of the code in a github repository.
    Generate a readme for the repository.
    """
    user_prompt = """
    Assume the role of an author and write a readme for the repository.
    Generate a beautiful readme for the repository using the summaries. The readme should have beautiful visual elements. Write the readme as if you are the author of the repository.
    The following is an example template / index for a readme:
    ### Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
   Only fill the details that you can verify from the information provided. Wherever necessary you may say "#To be written by you".
    Take your time to write a good readme.
    This is the summary of the code in the repository: {summary}
    """
