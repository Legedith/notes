from tools.llm.gemini import GeminiAI
from tools.text.text_formatter.text_formatter import TextFormatter

# Define the system instruction constant
SYSTEM_INSTRUCTION = """
Your task is to take a poorly written text with errors in grammar, punctuation, spelling, and word choice, and transform it into a well-structured, grammatically correct, and professionally formatted version. The text will often relate to complex topics such as computer science, computer architecture, system design, software development, coding, and other technical subjects. Use your domain knowledge to replace any incorrect, misheard, or mistyped words with the appropriate jargon and terminology. Ensure that the final output is clear, concise, and tailored to a technical audience, accurately reflecting the intended meaning and context.
"""


class ComputerScienceTextFormatter(TextFormatter):
    def __init__(self, text, domain):
        super().__init__(text, domain)
        self.ai = GeminiAI(system_instruction=SYSTEM_INSTRUCTION)

    def format_text(self):
        prompt = f"Domain: {self.domain}\nText: {self.text}"
        formatted_text = self.ai.generate_content(prompt)
        return formatted_text


# Example usage
if __name__ == "__main__":
    text = "imma gonna be talkin bout luby on lails tday"
    domain = "Development"
    formatter = ComputerScienceTextFormatter(text, domain)
    corrected_text = formatter.format_text()
    print(corrected_text)
