import os
import json
import time
from openai import OpenAI
from typing import List, Dict, Any, Optional, Callable
import textwrap
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored terminal output
init()

class FuturesWheelGenerator:
    def __init__(self, 
                 branch_counts: List[int] = [4, 3, 2, 1],
                 interactive: bool = False,
                 delay_seconds: int = 0,
                 wheel_type: str = "neutral",
                 temperature: float = 0.7):
        """
        Initialize the Futures Wheel Generator.
        
        Args:
            branch_counts: Number of branches to generate at each depth level
            interactive: If True, prompt user for confirmation at each step
            delay_seconds: Delay between API calls (to avoid rate limits)
            wheel_type: Type of futures wheel to generate - "neutral", "positive", "negative", or "long_shot"
            temperature: Temperature setting for OpenAI API (higher = more creative/random)
        """
        self.branch_counts = branch_counts
        self.max_depth = len(branch_counts)
        self.interactive = interactive
        self.delay_seconds = delay_seconds
        self.custom_prompts = {}  # Store custom prompts for specific paths
        self.default_prompt = """
        For the topic "{topic}", identify {count} potential impacts or consequences.
        Provide only the impacts as a JSON array of strings. Each impact should be concise (10 words or less).
        """
        self.final_node_prompt = None  # Special prompt for final nodes
        self.business_description = None  # Business description for relevance
        
        # Set wheel type and corresponding temperature
        self.wheel_type = wheel_type.lower()
        if self.wheel_type == "long_shot":
            self.temperature = 1.0  # Higher temperature for more creative/unusual outcomes
        else:
            self.temperature = temperature
        
    def generate_wheel(self, central_topic: str) -> Dict[str, Any]:
        """
        Generate a complete futures wheel for the given central topic.
        
        Args:
            central_topic: The central topic/event to explore
            
        Returns:
            A dictionary representing the futures wheel
        """
        print(f"Generating futures wheel for: {central_topic}")
        
        # Create the root node
        wheel = {
            "topic": central_topic,
            "impacts": [],
            "path": [],  # Empty path for root
            "branch_text": central_topic  # Track the full branch text
        }
        
        # Generate the wheel recursively
        self._generate_impacts(wheel, depth=0)
        
        # Remove path keys before returning (they were just for internal use)
        self._clean_wheel(wheel)
        
        return wheel
    
    def _clean_wheel(self, node: Dict[str, Any]) -> None:
        """Remove internal path tracking from the wheel before output"""
        if "path" in node:
            del node["path"]
        if "branch_text" in node:
            del node["branch_text"]
        
        for impact in node.get("impacts", []):
            self._clean_wheel(impact)
    
    def set_custom_prompt(self, path: List[int], prompt_template: str) -> None:
        """
        Set a custom prompt template for a specific path in the wheel.
        
        Args:
            path: List of indices representing the path (e.g., [0, 1] means 
                 first branch from root, then second branch from that)
            prompt_template: Custom prompt template with {topic} placeholder
        """
        path_key = "_".join([str(p) for p in path])
        self.custom_prompts[path_key] = prompt_template
    
    def set_default_prompt(self, prompt_template: str) -> None:
        """
        Set the default prompt template to use for paths without a custom prompt.
        
        Args:
            prompt_template: Custom prompt template with {topic} and {count} placeholders
        """
        self.default_prompt = prompt_template
    
    def set_final_node_prompt(self, prompt: str) -> None:
        """
        Set a custom prompt for all final nodes (deepest level).
        
        Args:
            prompt: The prompt template to use for final nodes
        """
        self.final_node_prompt = prompt
    
    def load_business_description(self, file_path: str) -> None:
        """
        Load business description from a file to use in final node prompts.
        
        Args:
            file_path: Path to the business description file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.business_description = f.read().strip()
            print(f"Loaded business description from {file_path}")
        except FileNotFoundError:
            print(f"Warning: Business description file not found at {file_path}")
            print("Creating template file for you to fill in...")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("""# Business Description
# Replace this text with information about your business, products, services,
# target market, goals, and any other relevant information.
# This information will be used to make the futures wheel more relevant to your business.

""")
            print(f"Created template file at {file_path}")
            self.business_description = ""
    
    def _get_prompt_for_path(self, path: List[int], depth: int, branch_text: str) -> str:
        """
        Get the appropriate prompt for the given path and depth.
        
        Args:
            path: Current path in the tree
            depth: Current depth in the recursion
            branch_text: The full branch text to generate impacts for
            
        Returns:
            Prompt string
        """
        # Check if this is a final node (at max depth)
        is_final_node = depth == self.max_depth - 1
        
        # If this is a final node and we have a final node prompt and business description
        if is_final_node and self.final_node_prompt and self.business_description:
            prompt = self.final_node_prompt.format(
                topic=branch_text,
                count=self.branch_counts[depth],
                business_description=self.business_description
            )
            return prompt
        
        # Check if we have a custom prompt for this path
        path_tuple = tuple(path)
        if path_tuple in self.custom_prompts:
            return self.custom_prompts[path_tuple].format(
                topic=branch_text,
                count=self.branch_counts[depth]
            )
        
        # Otherwise use the default prompt
        return self.default_prompt.format(
            topic=branch_text,
            count=self.branch_counts[depth]
        )
    
    def _generate_impacts(self, node: Dict[str, Any], depth: int) -> None:
        """
        Recursively generate impacts for a node in the futures wheel.
        
        Args:
            node: The current node to generate impacts for
            depth: Current depth in the recursion
        """
        # Base case: stop recursion if we've reached max depth
        if depth >= self.max_depth:
            return
        
        # Get the current path and branch text
        current_path = node.get("path", [])
        branch_text = node.get("branch_text", node["topic"])
        
        # If interactive mode, ask for confirmation
        if self.interactive:
            print(f"\nCurrent topic: {node['topic']}")
            print(f"Depth: {depth}, Path: {current_path}")
            proceed = input("Generate impacts for this topic? (y/n): ").lower().strip()
            if proceed != 'y':
                print("Skipping this branch")
                return
        
        # Generate impacts using OpenAI
        impacts = self._get_impacts_from_openai(branch_text, depth, current_path)
        
        # Add impacts to the current node
        for i, impact in enumerate(impacts):
            # Create new path for this impact
            new_path = current_path + [i]
            
            # Create new branch text that includes the entire branch history
            new_branch_text = f"{branch_text} -> {impact}"
            
            impact_node = {
                "topic": impact,
                "impacts": [],
                "path": new_path,
                "branch_text": new_branch_text
            }
            node["impacts"].append(impact_node)
            
            # Show progress
            indent = "  " * (depth + 1)
            print(f"{indent}Processing: {impact} (Path: {new_path})")
            
            # Add delay to avoid rate limits if specified
            if self.delay_seconds > 0:
                time.sleep(self.delay_seconds)
            
            # Recursively generate impacts for this new node
            self._generate_impacts(impact_node, depth + 1)
    
    def _get_impacts_from_openai(self, branch_text: str, depth: int, path: List[int]) -> List[str]:
        """
        Use OpenAI to generate impacts for a given topic.
        
        Args:
            branch_text: The full branch text to generate impacts for
            depth: Current depth in the recursion
            path: Current path in the tree
            
        Returns:
            List of impact statements
        """
        # Get the appropriate prompt for this path and depth
        prompt = self._get_prompt_for_path(path, depth, branch_text)
        
        # Add wheel type instructions to the prompt
        if self.wheel_type == "positive":
            prompt = prompt.replace("potential impacts or consequences", 
                                   "potential POSITIVE impacts or consequences (benefits, opportunities, advantages)")
        elif self.wheel_type == "negative":
            prompt = prompt.replace("potential impacts or consequences", 
                                   "potential NEGATIVE impacts or consequences (risks, challenges, disadvantages)")
        elif self.wheel_type == "long_shot":
            prompt = prompt.replace("potential impacts or consequences", 
                                   "potential UNUSUAL or SURPRISING impacts or consequences (low-probability but high-impact)")
        
        # Display the prompt in a visually appealing way
        self._display_prompt(prompt, path, depth)
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            temperature=self.temperature,
            messages=[
                {"role": "system", "content": "You are a futures thinking expert."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract and return the impacts
        try:
            content = response.choices[0].message.content
            impacts_data = json.loads(content)
            impacts = impacts_data.get("impacts", [])
            
            # Ensure we get exactly the number of impacts we want
            branch_count = self.branch_counts[depth]
            if len(impacts) > branch_count:
                impacts = impacts[:branch_count]
            elif len(impacts) < branch_count:
                # Pad with placeholder impacts if we didn't get enough
                impacts.extend([f"Impact {i+1} for {branch_text}" for i in range(len(impacts), branch_count)])
                
            return impacts
        except (json.JSONDecodeError, KeyError, AttributeError) as e:
            print(f"Error parsing OpenAI response: {e}")
            print(f"Response content: {response.choices[0].message.content}")
            # Return placeholder impacts on error
            return [f"Error generating impact {i+1}" for i in range(self.branch_counts[depth])]

    def _display_prompt(self, prompt: str, path: List[int], depth: int) -> None:
        """
        Display the prompt in a visually appealing way in the terminal.
        
        Args:
            prompt: The prompt to display
            path: The current path in the tree
            depth: The current depth in the recursion
        """
        # Terminal width (adjust if needed)
        term_width = 100
        
        # Create a border with the path information
        path_str = " -> ".join([str(p) for p in path])
        header = f" Prompt for Path: [{path_str}] | Depth: {depth} "
        padding = "=" * ((term_width - len(header)) // 2)
        border = f"\n{Fore.CYAN}{padding}{header}{padding}{Style.RESET_ALL}\n"
        
        # Preserve original line breaks and wrap each line individually
        formatted_lines = []
        for line in prompt.split('\n'):
            # Skip empty lines
            if not line.strip():
                formatted_lines.append("")
                continue
                
            # Wrap this line if it's too long
            if len(line) > term_width - 4:
                wrapped = textwrap.fill(line.strip(), width=term_width - 4)
                for wrapped_line in wrapped.split('\n'):
                    formatted_lines.append(f"  {wrapped_line}")
            else:
                formatted_lines.append(f"  {line.strip()}")
        
        # Join the formatted lines
        indented_text = "\n".join(formatted_lines)
        
        # Add a footer
        footer = f"{Fore.CYAN}{'=' * term_width}{Style.RESET_ALL}\n"
        
        # Print the formatted prompt
        print(border)
        print(f"{Fore.YELLOW}{indented_text}{Style.RESET_ALL}")
        print(footer)

    def save_wheel(self, wheel: Dict[str, Any], filename: str) -> None:
        """
        Save the wheel to a PlantUML file.
        
        Args:
            wheel: The wheel data structure
            filename: The filename to save to (without extension)
        """
        # Ensure the files directory exists
        os.makedirs("files", exist_ok=True)
        
        # Construct the full path
        if not filename.startswith("files/") and not filename.startswith("files\\"):
            filename = os.path.join("files", filename)
        
        # Save as PlantUML
        with open(f"{filename}.puml", "w", encoding="utf-8") as f:
            f.write("@startmindmap\n")
            f.write("skinparam defaultTextAlignment center\n")
            f.write("skinparam wrapWidth 200\n")
            f.write("skinparam backgroundColor white\n\n")
            
            # Root node (uncolored)
            f.write(f"* {wheel['topic']}\n")
            
            # Write impacts with colors based on level
            self._write_impacts(f, wheel["impacts"], 1)
            
            f.write("@endmindmap\n")
        
        # Save as JSON
        with open(f"{filename}.json", "w", encoding="utf-8") as f:
            json.dump(wheel, f, indent=2)

    def _write_impacts(self, file, impacts, level):
        """
        Recursively write impacts to the PlantUML file with colors based on level.
        
        Args:
            file: The file to write to
            impacts: The impacts to write
            level: The current level (depth) in the tree
        """
        for impact in impacts:
            # Determine color based on level
            color_code = ""
            if level == 1:
                color_code = "[#00bcd4]"  # Cyan for level 1
            elif level == 2:
                color_code = "[#2ecc71]"  # Green for level 2
            elif level == 3:
                color_code = "[#f1c40f]"  # Yellow for level 3
            elif level == 4:
                color_code = "[#e74c3c]"  # Red for level 4
            
            # Write the impact with proper indentation and color
            file.write(f"{'  ' * level}*{color_code} {impact['topic']}\n")
            
            # Recursively write child impacts
            if impact.get("impacts"):
                self._write_impacts(file, impact["impacts"], level + 1)

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
