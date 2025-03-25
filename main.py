import argparse
from FuturesWheelGenerator import FuturesWheelGenerator

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate a futures wheel using OpenAI')
    parser.add_argument('--topic', type=str, default='The future of education', help='Central topic for the futures wheel')
    parser.add_argument('--branches', type=str, default='4,3,2,1', 
                        help='Comma-separated list of branch counts at each level (default: 4,3,2,1)')
    parser.add_argument('--interactive', action='store_true', 
                        help='Enable interactive mode to confirm each branch generation')
    parser.add_argument('--delay', type=int, default=1,
                        help='Delay in seconds between API calls (to avoid rate limits)')
    parser.add_argument('--output', type=str, default='files/futures_wheel', 
                        help='Output filename prefix (without extension)')
    parser.add_argument('--type', type=str, choices=['neutral', 'positive', 'negative', 'long_shot'], 
                        default='neutral',
                        help='Type of futures wheel to generate (neutral, positive, negative, or long_shot)')
    parser.add_argument('--temperature', type=float, default=0.7,
                        help='Temperature setting for OpenAI API (higher = more creative/random)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Parse branch counts
    branch_counts = [int(x) for x in args.branches.split(',')]
    
    # Create generator with specified configuration
    generator = FuturesWheelGenerator(
        branch_counts=branch_counts,
        interactive=args.interactive,
        delay_seconds=args.delay,
        wheel_type=args.type,
        temperature=args.temperature
    )
    
    print(f"Generating {args.type} futures wheel for: {args.topic}")
    
    # Generate the wheel
    wheel = generator.generate_wheel(args.topic)
    
    # Save to PlantUML file
    generator.save_wheel(wheel, f"{args.output}.puml")
    
    print(f"Futures wheel saved to {args.output}.puml")
    print("To view the diagram, use a PlantUML viewer or online service like http://www.plantuml.com/plantuml/")

if __name__ == "__main__":
    main()
