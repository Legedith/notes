from tools.llm.gemini import GeminiAI
from tools.text.text_formatter.text_formatter import TextFormatter

# Define the system instruction constant
SYSTEM_INSTRUCTION = """
Your task is to take a poorly written text with errors in grammar, punctuation, spelling, and word choice, and transform it into a well-structured, grammatically correct, and professionally formatted version. The text will often relate to complex topics such as computer science, computer architecture, system design, software development, coding, and other technical subjects. Use your domain knowledge to replace any incorrect, misheard, or mistyped words with the appropriate jargon and terminology. Ensure that the final output is clear, concise, and tailored to a technical audience, accurately reflecting the intended meaning and context. Keep the sentence structure and tone consistent with the original text. Modify only the grammar and style, not the content or meaning of the text.
"""


class ComputerScienceTextFormatter(TextFormatter):
    def __init__(self) -> None:
        super().__init__()
        self.ai = GeminiAI(system_instruction=SYSTEM_INSTRUCTION)

    def format_text(self, text, domain) -> str:
        prompt = f"Domain: {domain}\nText: {text}"
        return self.ai.generate_content(prompt)


# Example usage
if __name__ == "__main__":
    text = """Hi, this is Jadid Ramival, I'm a robotics and augmented reality developer with almost three years of experience in the industry. I am Sravana Lakshmi, a data scientist and an MBA graduate. Together, we are from RoboVice. So we came up with this idea of RoboVice when we were working on a robotic arm and we almost managed to kill someone because we forgot to set some parameters while testing our robot out. RoboVice gives a way to test your robot in augmented reality before running it in real world. We know that robots are safe from the risk and it is the most safest way and faster way to control the robots. So our technology is backed by Snapchat and we are currently ready with our POC with millimeter precision. RoboVice is deployable on any raw space robot in the industry from a small robotic arm to big industrial machines. And we know that having skilled experts and safety are the biggest concerns to deploy the robots in industries. With RoboVice, we plan to change that. Thank you.
"""
    domain = "Development"
    formatter = ComputerScienceTextFormatter()
    corrected_text = formatter.format_text(text, domain)
    print(corrected_text)
