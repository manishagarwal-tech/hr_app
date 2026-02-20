import logging
import fitz

logger = logging.getLogger(__name__)


class ResumeParserService:
    def extract_text(self, resume_file):
        resume_bytes = self.read_bytes(resume_file)
        if not resume_bytes:
            raise ValueError("Uploaded resume is empty.")
        return self.extract_text_from_bytes(resume_bytes)

    def read_bytes(self, resume_file):
        if hasattr(resume_file, "read"):
            resume_bytes = resume_file.read()
            if hasattr(resume_file, "seek"):
                resume_file.seek(0)
            return resume_bytes
        if isinstance(resume_file, (bytes, bytearray)):
            return bytes(resume_file)
        raise ValueError("Unsupported resume file type.")

    def extract_text_from_bytes(self, resume_bytes):
        try:
            with fitz.open(stream=resume_bytes, filetype="pdf") as pdf_document:
                pages = [page.get_text() for page in pdf_document]
            return "".join(pages)
        except Exception as exc:
            logger.exception("Failed to parse PDF resume")
            raise ValueError("The uploaded file is not a valid PDF.") from exc
