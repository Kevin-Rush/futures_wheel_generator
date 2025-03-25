import argparse
from FuturesWheelGenerator import FuturesWheelGenerator

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate a futures wheel using OpenAI')
    parser.add_argument('topic', type=str, help='Central topic for the futures wheel')
    parser.add_argument('--branches', type=str, default='4,3,2,1', 
                        help='Comma-separated list of branch counts at each level (default: 4,3,2,1)')
    parser.add_argument('--interactive', action='store_true', 
                        help='Enable interactive mode to confirm each branch generation')
    parser.add_argument('--delay', type=int, default=0,
                        help='Delay in seconds between API calls (to avoid rate limits)')
    parser.add_argument('--output', type=str, default='futures_wheel.puml', 
                        help='Output filename (PlantUML format)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Parse branch counts
    branch_counts = [int(x) for x in args.branches.split(',')]
    
    # Create generator with specified configuration
    generator = FuturesWheelGenerator(
        branch_counts=branch_counts,
        interactive=args.interactive,
        delay_seconds=args.delay
    )
    
    # Example of setting custom prompts for specific paths
    # Uncomment and modify these lines to customize prompts for specific branches
    # generator.set_custom_prompt([0], "For {topic}, what are the most disruptive technological impacts?")
    # generator.set_custom_prompt([0, 1], "For {topic}, what are the most significant economic consequences?")
    
    # Generate wheel
    wheel = generator.generate_wheel(args.topic)
    
    # Save the wheel
    generator.save_wheel(wheel, args.output)
    
    print("Futures wheel generation complete!")

if __name__ == "__main__":
    main()
