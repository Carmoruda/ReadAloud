import PyPDF2
import PyPDF2.errors


class PDFReader:
    """Class for reading PDF files into smaller parts.

    Provides functionalities to read a PDF file.

    Attributes:
        input_pdf_path (str): Path to the input PDF file to be read.
    """

    def __init__(self):
        self.defaultAttributes()

    def defaultAttributes(self):
        """Resets the attributes to their default values.

        Sets the initial values for the input PDF path and the content.
        """
        self.input_pdf_path = ""
        self.content = ""

    def check_pdf(self, pdf):
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

    def read_pdf(self, pdf):
        """Reads a PDF file and returns a PdfReader object.

        Args:
            pdf (str): Path to the PDF file to be read.

        Returns:
            PdfReader: A PdfReader object representing the PDF file.
        """

        if not self.check_pdf(pdf):
            raise ValueError(f"The file {pdf} is not a valid PDF.")

        self.input_pdf_path = pdf
        reader = PyPDF2.PdfReader(pdf)

        self.content = "\n".join([page.extract_text() or "" for page in reader.pages])

        return self.content


reader = PDFReader()
