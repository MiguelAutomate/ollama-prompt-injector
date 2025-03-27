import argparse
from pathlib import Path
import ollama
from colorama import Fore, Style, init

init(autoreset=True)

class PromptTester:
    def __init__(self, model: str = "llama2"):
        self.model = model

    def load_prompts(self, file: str) -> list[str]:
        """Load prompts from file, ignoring comments/empties"""
        try:
            path = Path("prompts") / file
            return [
                line.strip() for line in path.read_text().splitlines() 
                if line.strip() and not line.startswith("#")
            ]
        except Exception as e:
            print(f"{Fore.RED}Error loading prompts: {e}{Style.RESET_ALL}")
            return []

    def test(self, prompt: str) -> str:
        """Test a single prompt"""
        try:
            response = ollama.generate(model=self.model, prompt=prompt)
            return response['response']
        except Exception as e:
            return f"{Fore.RED}Error: {e}{Style.RESET_ALL}"

def main():
    parser = argparse.ArgumentParser(description="Test prompt injections against Ollama")
    parser.add_argument("--model", default="llama2", help="Ollama model name")
    parser.add_argument("--file", default="basic_injections.txt", help="Prompt file to test")
    args = parser.parse_args()

    tester = PromptTester(args.model)
    prompts = tester.load_prompts(args.file)

    print(f"\n{Fore.CYAN}Testing {len(prompts)} prompts on model '{args.model}'{Style.RESET_ALL}\n")
    
    for i, prompt in enumerate(prompts, 1):
        print(f"{Fore.YELLOW}Test #{i}:{Style.RESET_ALL} {prompt}")
        print(f"{Fore.BLUE}Response:{Style.RESET_ALL} {tester.test(prompt)}\n")

if __name__ == "__main__":
    main()