import PyPDF2
import PyPDF2.errors


class PDFReader:
    """
    Provides functionalities to read a PDF file.
    """

    @staticmethod
    def check_pdf(pdf):
        """Checks if the provided file is a valid PDF.

        Args:
            pdf (str): Path to the PDF file to be checked.

        Returns:
            bool: True if the file is a valid PDF, False otherwise.
        """
        try:
            PyPDF2.PdfReader(pdf)
            return True
        except PyPDF2.errors.PdfReadError:
            return False

    @staticmethod
    def read_pdf(pdf: str) -> str:
        """Reads a PDF file and returns a PdfReader object.

        Args:
            pdf (str): Path to the PDF file to be read.

        Returns:
            str: The text content of the PDF file.
        """

        if not PDFReader.check_pdf(pdf):
            raise ValueError(f"The file {pdf} is not a valid PDF.")

        reader = PyPDF2.PdfReader(pdf)

        return "\n".join([page.extract_text() or "" for page in reader.pages])
