import os
from FuturesWheelGenerator import FuturesWheelGenerator

def main():
    # Set the topic
    topic = "The closure of the US Department of Education and the devolution of education policy to the control of US States and School Boards."
    
    # Create generator with specific configuration - now with 6 primary branches for STEEPV
    generator = FuturesWheelGenerator(
        branch_counts=[6, 3, 2, 1],  # 6→3→2→1 branching pattern 
        interactive=False,           # Non-interactive mode
        delay_seconds=1              # 1 second delay between API calls
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
    industrial structures, and markets & financial issues.
    Provide only the impacts as a JSON array of strings. Each impact should be concise (20 words or less).
    """)
    
    generator.set_custom_prompt([3], """
    For the topic "{topic}", identify 3 potential ENVIRONMENTAL impacts or consequences.
    Focus on sustainability, climate change, localized environmental issues, 
    resource usage, and ecological impacts of education policy changes.
    Provide only the impacts as a JSON array of strings. Each impact should be concise (20 words or less).
    """)
    
    generator.set_custom_prompt([4], """
    For the topic "{topic}", identify 3 potential POLITICAL impacts or consequences.
    Focus on governance, policy changes, political movements, dominant political viewpoints,
    regulation, and lobbying related to education.
    Provide only the impacts as a JSON array of strings. Each impact should be concise (20 words or less).
    """)
    
    generator.set_custom_prompt([5], """
    For the topic "{topic}", identify 3 potential VALUES impacts or consequences.
    Focus on attitudes to working life, preferences for leisure, culture, social relations,
    deference to authority, and changing value systems in education.
    Provide only the impacts as a JSON array of strings. Each impact should be concise (20 words or less).
    """)
    
    # Set a default prompt for all subsequent branches that focuses on continuing the train of thought
    generator.set_default_prompt("""
    Consider this chain of consequences of: {topic}
    
    Based on this progression of impacts, identify {count} logical next-order consequences or effects 
    that would naturally follow from this chain of events.
    
    Think about how each previous impact builds upon the others and what further effects might emerge.
    Ensure your response follows logically from the entire chain, not just the most recent impact.
    
    Provide only the impacts as a JSON array of strings. Each impact should be concise (20 words or less).
    """)
    
    # Generate wheel
    print(f"Generating custom futures wheel using STEEPV framework for: {topic}")
    wheel = generator.generate_wheel(topic)
    
    # Save the wheel
    generator.save_wheel(wheel, "education_futures_steepv.puml")
    
    print("STEEPV futures wheel generation complete!")

if __name__ == "__main__":
    main()
