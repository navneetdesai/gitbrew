class GenerateReadmePrompt:
    system_prompt = """
    You are an AI assistant, expert in understanding code and writing beautiful documentations in Readme.md files.
    You are asked to generate a beautiful readme for the repository using the summaries.
    You will be given a summary of the code in the repository.
    Write the readme as if you are the author of the repository. The readme should have beautiful visual elements.
    You may use open source images or gifs from the internet.
    """
    user_prompt = """
    Assume the role of an author and write a readme for the repository.
    The following is an example template / index for a readme:
    # Project Title
    Short description and tagline of the project.
    
    ### Table of Contents
        - [Introduction](#introduction)
        - [Features](#features)
        - [Technologies](#technologies)
        - [Installation](#installation)
        - [Usage](#usage)
        - [Contributing](#contributing)
        - [License](#license)
    Take your time to write a good readme. Do not manufacture missing details. If you
    are unsure about something, mark it as TODO for the developer and move on.
    This is the summary of the code in the repository: {summaries}
    """
