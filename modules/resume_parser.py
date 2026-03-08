"""
Resume Parser Module
Extracts text from PDF and DOCX files
"""

import PyPDF2
import docx
import re
from typing import Optional


class ResumeParser:
    """Parses resume files and extracts text"""
    
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """
        Extract text from PDF file
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text from PDF
        """
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            return text
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    @staticmethod
    def extract_text_from_docx(file_path: str) -> str:
        """
        Extract text from DOCX file
        
        Args:
            file_path: Path to DOCX file
            
        Returns:
            Extracted text from DOCX
        """
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")
    
    @staticmethod
    def extract_text_from_file(file_path: str) -> str:
        """
        Extract text from file (PDF or DOCX)
        
        Args:
            file_path: Path to resume file
            
        Returns:
            Extracted resume text
        """
        if file_path.lower().endswith('.pdf'):
            return ResumeParser.extract_text_from_pdf(file_path)
        elif file_path.lower().endswith('.docx'):
            return ResumeParser.extract_text_from_docx(file_path)
        else:
            raise ValueError("File format not supported. Please use PDF or DOCX.")
    
    @staticmethod
    def extract_email(text: str) -> Optional[str]:
        """Extract email from resume text"""
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        match = re.search(pattern, text)
        return match.group(0) if match else "Not found"
    
    @staticmethod
    def extract_phone(text: str) -> Optional[str]:
        """Extract phone number from resume text"""
        pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        match = re.search(pattern, text)
        return match.group(0) if match else "Not found"
    
    @staticmethod
    def extract_urls(text: str) -> list:
        """Extract URLs (LinkedIn, GitHub, etc.) from resume text"""
        pattern = r'https?://[^\s]+'
        urls = re.findall(pattern, text)
        return urls if urls else []
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean resume text
        
        Args:
            text: Raw resume text
            
        Returns:
            Cleaned text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespaces
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
