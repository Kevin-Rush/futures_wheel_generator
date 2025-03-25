from FuturesWheelGenerator import FuturesWheelGenerator
import argparse
import os

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate a futures wheel for education policy using the STEEPV framework')
    parser.add_argument('--topic', type=str, 
                        default="The closure of the US Department of Education and the devolution of education policy to the control of US States and School Boards.",
                        help='Central topic for the futures wheel')
    parser.add_argument('--interactive', action='store_true', 
                        help='Enable interactive mode to confirm each branch generation')
    parser.add_argument('--delay', type=int, default=1,
                        help='Delay in seconds between API calls (to avoid rate limits)')
    parser.add_argument('--output', type=str, default='education_futures_steepv',
                        help='Output filename prefix (without extension)')
    parser.add_argument('--type', type=str, choices=['neutral', 'positive', 'negative', 'long_shot'], 
                        default='neutral',
                        help='Type of futures wheel to generate (neutral, positive, negative, or long_shot)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Set filename based on wheel type
    output_file = f"{args.output}_{args.type}" if args.type != 'neutral' else args.output
    
    # Create generator with specific configuration - now with 6 primary branches for STEEPV
    generator = FuturesWheelGenerator(
        branch_counts=[6, 3, 2, 1],  # 6→3→2→1 branching pattern 
        interactive=args.interactive,  
        delay_seconds=args.delay,
        wheel_type=args.type,
        temperature=1.0 if args.type == 'long_shot' else 0.7
    )
    
    # Set custom prompts for specific branches to focus on different aspects - STEEPV framework
    
    # First level branches - Different domains (STEEPV)
    generator.set_custom_prompt([0], """
    For the topic "{topic}", identify 3 potential SOCIAL impacts or consequences.
    Focus on community effects, social cohesion, cultural aspects, ways of life, 
    demographic structures, and social inclusion issues.
    Provide only the impacts as a JSON array of strings. Each impact should be concise (20 words or less).
    """)
    
    generator.set_custom_prompt([1], """
    For the topic "{topic}", identify 3 potential TECHNOLOGICAL impacts or consequences.
    Focus on digital divide, educational technology, innovation, rates of tech progress,
    pace of diffusion, and technology-related problems & risks.
    Provide only the impacts as a JSON array of strings. Each impact should be concise (20 words or less).
    """)
    
    generator.set_custom_prompt([2], """
    For the topic "{topic}", identify 3 potential ECONOMIC impacts or consequences.
    Focus on financial aspects, market changes, economic inequality, level & distribution of economic growth,
    industrial structures, markets & financial issues.
    Provide only the impacts as a JSON array of strings. Each impact should be concise (20 words or less).
    """)
    
    generator.set_custom_prompt([3], """
    For the topic "{topic}", identify 3 potential ENVIRONMENTAL impacts or consequences.
    Focus on sustainability, climate change, localized environmental issues, resource usage, ecological impacts.
    Provide only the impacts as a JSON array of strings. Each impact should be concise (20 words or less).
    """)
    
    generator.set_custom_prompt([4], """
    For the topic "{topic}", identify 3 potential POLITICAL impacts or consequences.
    Focus on governance, policy changes, political movements, dominant political viewpoints,
    regulation, lobbying.
    Provide only the impacts as a JSON array of strings. Each impact should be concise (20 words or less).
    """)
    
    generator.set_custom_prompt([5], """
    For the topic "{topic}", identify 3 potential VALUES impacts or consequences.
    Focus on attitudes to working life, preferences for leisure, culture, social relations,
    deference to authority, changing value systems.
    Provide only the impacts as a JSON array of strings. Each impact should be concise (20 words or less).
    """)
    
    # Set default prompt for all other branches - focus on continuing the train of thought
    generator.set_default_prompt("""
    Continue the train of thought for this branch: "{topic}"
    
    Consider the entire chain of consequences shown above, not just the most recent impact.
    Identify {count} logical next-order impacts or consequences that would follow.
    
    Provide only the impacts as a JSON array of strings. Each impact should be concise (20 words or less).
    """)
    
    print(f"Generating {args.type} futures wheel using STEEPV framework for topic:")
    print(f'"{args.topic}"')
    print()
    
    # Generate the wheel
    wheel = generator.generate_wheel(args.topic)
    
    # Save to PlantUML file
    generator.save_wheel(wheel, output_file)
    
    print(f"\nFutures wheel saved to {output_file}.puml")
    print("To view the diagram, use a PlantUML viewer or online service like http://www.plantuml.com/plantuml/")

if __name__ == "__main__":
    main()
