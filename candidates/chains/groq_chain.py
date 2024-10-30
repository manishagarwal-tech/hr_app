import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class HRChain:
    def __init__(self):
        # Initialize the ChatGroq model
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.1-70b-versatile"
        )

    def extract_skills_and_experience(self, resume_text):
        """
        Uses Groq to extract skills and experience from resume text.
        """
        prompt_extract = PromptTemplate.from_template(
            """
            ### RESUME TEXT:
            {resume_data}
            ### INSTRUCTION:
            Extract the candidate's primary skills, secondary skills, and experience level in years from the resume text.
            Return the result in JSON format with the following keys: `primary_skills`, `secondary_skills`, `experience`.
            ### VALID JSON:
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"resume_data": resume_text})
        try:
            json_parser = JsonOutputParser()
            extracted_data = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Error parsing skills and experience.")
        return extracted_data

    def generate_interview_questions(self, skill, expertise):
        prompt = PromptTemplate.from_template(
            """
            ### INSTRUCTION:
            Generate 5 interview questions based on the following skill and expertise level.
            Skill: {skill}
            Expertise Level: {expertise}
            Respond only with a numbered list of questions in HTML list format without preambles, explanations, or additional formatting.

            ### QUESTIONS (NO PREAMBLE):
            """
        )
        # prompt = PromptTemplate.from_template(
        #     """
        #     ### INSTRUCTION:
        #     Generate 5 interview questions based on the following skill and expertise level.
        #     Skill: {skill}
        #     Expertise Level: {expertise}
        #
        #     Provide at least 2-3 questions that involve coding or writing queries related to the expertise level.
        #
        #     Respond only with a numbered list of questions in HTML list format, without explanations or extra formatting.
        #
        #     ### QUESTIONS (NO PREAMBLE):
        #     """
        # )

        # Combine the prompt with the input
        chain = prompt | self.llm
        response = chain.invoke(input={"skill": skill, "expertise": expertise})

        # Assuming the output is plain text, split it into a list of questions
        questions = response.content
        return questions

if __name__ == "__main__":
    # Testing API key loading
    print(os.getenv("GROQ_API_KEY"))