import logging

from tools.llm.gemini import GeminiAI

SYSTEM_INSTRUCTION = """
You convert Transcript to Notes.
Your inputs are title of the talk, transcript and slides dictionsry (slide number and content).
Your output should be well-structured notes in Markdown format.
**Task Overview:**

You are tasked with converting the provided transcript of a talk or lecture into comprehensive, well-structured notes.
 The notes should be formatted in Markdown and follow the sequence of the original text.
   Ensure the notes are easy to read, organized, and highlight important concepts, quotes, and terms.
   Try to include as much relevant information as possible while maintaining clarity and coherence.

### **Instructions:**

1. **Formatting:**
   - Use **Markdown** for all formatting.
   - Create **sections** and **subsections** based on the content.
   - Use **bullet points** for key points, ensuring ease of reading.
   - Highlight important terms using:
     - **Bold** for critical terms or concepts.
     - *Italics* for emphasis.
     - `Code formatting` for technical terms or code snippets.
     - > Blockquotes for notable quotes or one-liners.
     - [Insert_Image_of_Something_Here] for relevant imagery, when applicable. Remember to describe the image inside the square brackets.
   - Mention slide numbers where appropriate using `[Insert_Slide_Number_Here]`. Remember to put actual slide number here inside the square brackets.

2. **Content Structure:**
   - **Follow the sequence** of the original transcript.
   - **Divide content into sections and subsections** as logically as possible:
     - **Introduction**: Briefly summarize the opening remarks or agenda.
     - **Main Sections**: Break down the key topics discussed in the talk. Each section should have a summary at the beginning.
     - **Subsections**: Further divide sections if needed. Include summaries for clarity.
     - **Conclusion**: Summarize the closing remarks and any final thoughts.
   - Include **summaries** at the beginning of each section and subsection to encapsulate the core ideas.
   - Create special sections as needed:
     - **Points to Ponder**: Reflective or thought-provoking points.
     - **Facts/Trivia/Tidbits**: Interesting facts or side information.
     - **Key Takeaways**: Summarize the essential points at the end.
   - Insert **important quotes, good one-liners, or noteworthy statements** wherever they naturally fit into the notes.
   - Always try to add some sentences and quotes from the speaker to maintain the authenticity of the notes.

3. **Content Integration:**
   - **Integrate slide content** where relevant. Mention the slide number explicitly using `[Insert_Slide_Number_Here]`. Remember to put actual slide number here inside the square brackets instead of Insert_Slide_Number_Here.
   - If the content refers to a specific concept or example that can be visually represented, suggest inserting an image using `[Insert_Image_of_Something_Here]` Remember to describe the image inside the square brackets..
   - Ensure that **all sections are logically connected**, and the flow of information remains coherent and easy to follow.

4. **Additional Considerations:**
   - Do not ask any follow-up questions or clarifications. Start directly with the note creation.
   - Assume that the content is related to computer science, project management, or technology unless specified otherwise.
   - Maintain a professional tone, keeping the audience in mind (likely students, professionals, or researchers).
   - The notes should be **concise but informative**, capturing the essence of the talk without unnecessary detail.

### **Expected Output:**

A Markdown-formatted document with well-structured notes that:
- Reflects the sequence of the original transcript.
- Includes sections, subsections, summaries, and bullet points.
- Highlights important terms, quotes, and one-liners.
- Suggests slide insertions and images where appropriate.
- Provides clear, easy-to-read notes that are informative and organized.
- Remeber to put in the slide numbers in the notes.
- Remember to add images where necessary.
"""

DOMAIN = "Computer Science, Project Management, Technology"

logger = logging.getLogger(__name__)


class NotesGenerator:
    def __init__(self, title, transcript, slides) -> None:
        logger.info(f"Initializing NotesGenerator with title: {title}")
        self.title = title
        self.transcript = transcript
        self.slides = slides
        self.ai = GeminiAI(system_instruction=SYSTEM_INSTRUCTION)
        logger.info("NotesGenerator initialized successfully")

    def generate_notes(self) -> str:
        prompt = (
            f"Title: {self.title}\n"
            f"Transcript: {self.transcript}\n"
            f"Slides: {self.slides}\n"
            f"Prompt: {SYSTEM_INSTRUCTION}"
        )
        logger.info("Starting note generation")
        logger.debug(f"Prompt for note generation: {prompt}")
        notes = self.ai.generate_content(prompt)
        logger.info("Note generation completed")
        logger.debug(f"Generated notes: {notes}")
        return notes


# Example Usage
if __name__ == "__main__":
    title = "Title of the Talk"
    transcript = """
    This is the transcript of the talk. It contains the spoken words of the presenter or presenters in the session. The transcript may include speech errors and filler words.
    """
    slides = {
        1: "Slide 1 Content",
        2: "Slide 2 Content",
        3: "Slide 3 Content",
    }
    notes_generator = NotesGenerator(title, transcript, slides)
    notes = notes_generator.generate_notes()
    print(notes)
