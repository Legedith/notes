import logging

from tools.llm.gemini import GeminiAI
from tools.text.text_formatter.text_formatter import TextFormatter

# Define the system instruction constant
SYSTEM_INSTRUCTION = """
For the given transcript, fix the grammar, clean the formatting and do nothing else.
Assume the content is related to computer science, project management, or technology.
"""

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ComputerScienceTextFormatter(TextFormatter):
    def __init__(self) -> None:
        super().__init__()
        self.ai = GeminiAI(system_instruction=SYSTEM_INSTRUCTION)
        logger.info("ComputerScienceTextFormatter initialized with system instruction.")

    def split_text_recursively(self, text, min_size=15000, max_size=25000) -> list:
        if len(text) <= max_size:
            return [text]

        mid = len(text) // 2
        left = text[:mid]
        right = text[mid:]

        if len(left) < min_size:
            return [text]

        return self.split_text_recursively(
            left,
            min_size,
            max_size,
        ) + self.split_text_recursively(right, min_size, max_size)

    def format_text(self, text, domain) -> str:
        logger.info("Starting text formatting process.")
        logger.info(f"Text length: {len(text)} characters.")

        batches = self.split_text_recursively(text)
        logger.info(f"Total batches created: {len(batches)}.")

        processed_batches = []
        for i, batch in enumerate(batches):
            logger.info(
                f"Processing batch {i + 1}/{len(batches)} (length: {len(batch)}).",
            )
            processed_batch = self.ai.generate_content(
                f"Domain: {domain}\nText: {batch}",
            )
            processed_batches.append(processed_batch)
            logger.info(f"Batch {i + 1} processed.")

        # Stitch the processed batches together
        stitched_text = processed_batches[0]
        for i in range(1, len(processed_batches)):
            stitched_text += processed_batches[i]
            logger.info(f"Stitched batch {i + 1} into final text.")

        logger.info("Text formatting process completed.")
        return stitched_text


# Example usage
if __name__ == "__main__":
    text = """Hi, this is Jadid Ramival, I'm a robotics and augmented reality developer with almost three years of experience in the industry. I am Sravana Lakshmi, a data scientist and an MBA graduate. Together, we are from RoboVice. So we came up with this idea of RoboVice when we were working on a robotic arm and we almost managed to kill someone because we forgot to set some parameters while testing our robot out. RoboVice gives a way to test your robot in augmented reality before running it in real world. We know that robots are safe from the risk and it is the most safest way and faster way to control the robots. So our technology is backed by Snapchat and we are currently ready with our POC with millimeter precision. RoboVice is deployable on any raw space robot in the industry from a small robotic arm to big industrial machines. And we know that having skilled experts and safety are the biggest concerns to deploy the robots in industries. With RoboVice, we plan to change that. Thank you.
"""
    domain = "Development"
    formatter = ComputerScienceTextFormatter()
    corrected_text = formatter.format_text(text, domain)
    print(corrected_text)
