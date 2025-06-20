import json
import matplotlib.pyplot as plt

def main():
    filepath = r"backend\ai_workspace\code_generator\v2\codeGeneratorv2.json"

    # Load JSON data
    with open(filepath, "r") as f:
        data = json.load(f)

    # Extract token usage info
    token_usage = data.get("token_usage", [])
    step_names = [step["step_name"] for step in token_usage]
    total_tokens = [step["token_usage"]["total_tokens"] for step in token_usage]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.bar(step_names, total_tokens)
    plt.xlabel('Step')
    plt.ylabel('Total Tokens')
    plt.title('Gestalt Code Generator Token Count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
