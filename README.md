# Futures Wheel Generator

A tool that uses OpenAI to recursively generate a futures wheel - a structured method for exploring the potential consequences and impacts of a central event or trend. The output is formatted as a PlantUML mindmap for easy visualization.

## Features

- **Continuous Branch History**: Each node is generated based on the entire branch history, creating a coherent thought progression
- **STEEPV Framework Support**: Organize impacts according to Social, Technological, Economic, Environmental, Political, and Values dimensions
- **Customizable Branching Pattern**: Control exactly how many branches to generate at each level (e.g., 6→3→2→1)
- **Interactive Mode**: Confirm each branch generation step-by-step
- **Custom Prompts**: Define specific prompts for individual branches to guide the exploration
- **Default Prompt System**: Set a default prompt for all branches without custom prompts
- **Path Tracking**: Each branch knows its position in the tree for targeted customization
- **Prompt Visualization**: Display formatted prompts in the terminal for debugging and optimization
- **Rate Limit Control**: Add delays between API calls to avoid OpenAI rate limits
- **PlantUML Output**: Visualize results as a mindmap diagram

## Setup

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set your OpenAI API key as an environment variable:
   ```
   # Windows
   set OPENAI_API_KEY=your_api_key_here
   
   # Linux/Mac
   export OPENAI_API_KEY=your_api_key_here
   ```

## Usage

### Basic Usage

Run the script with a central topic:

```
python main.py "Widespread adoption of autonomous vehicles"
```

### Advanced Options

- `--branches`: Comma-separated list of branch counts at each level (default: 4,3,2,1)
- `--interactive`: Enable interactive mode to confirm each branch generation
- `--delay`: Delay in seconds between API calls (to avoid rate limits)
- `--output`: Output filename in PlantUML format (default: futures_wheel.puml)

### Examples

Generate a futures wheel with the default 4→3→2→1 branching pattern:
```
python main.py "Impact of quantum computing on cybersecurity"
```

Generate a futures wheel with a custom branching pattern (5→4→3):
```
python main.py "Future of remote work" --branches 5,4,3
```

Generate a futures wheel in interactive mode with a 2-second delay between API calls:
```
python main.py "Climate change adaptation" --interactive --delay 2
```

## Customizing Prompts

You can customize prompts for specific branches by modifying the `main.py` file. Uncomment and adjust the following lines:

```python
# Example of setting custom prompts for specific paths
generator.set_custom_prompt([0], "For {topic}, what are the most disruptive technological impacts?")
generator.set_custom_prompt([0, 1], "For {topic}, what are the most significant economic consequences?")
```

The path notation works as follows:
- `[0]` refers to the first branch from the central topic
- `[0, 1]` refers to the second branch from the first branch
- And so on...

## Output

The script generates a PlantUML file containing the futures wheel structure as a mindmap. You can visualize this file using:

1. Online PlantUML server: http://www.plantuml.com/plantuml/
2. PlantUML extension for VS Code
3. PlantUML desktop application

## How It Works

The generator uses a recursive approach:
1. Start with a central topic
2. Use OpenAI to generate primary impacts (first level branches)
3. For each primary impact, generate secondary impacts (second level branches)
4. Continue recursively until reaching the maximum depth
5. Convert the hierarchical structure to PlantUML mindmap format

The recursive nature of the code is primarily in the `_generate_impacts` method, which:
- Checks if we've reached max depth (base case for recursion)
- Gets impacts from OpenAI for the current node
- For each impact, creates a new node and recursively calls itself on that node
- This creates a depth-first traversal of the futures wheel
