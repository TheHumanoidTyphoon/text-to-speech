import pdfplumber
import os
import threading
import time
from gtts import gTTS
import pygame
import docx2txt
from bs4 import BeautifulSoup

class FileReader:
    """
    This class reads different types of files and extracts their content for further processing.

    Args:
    file_path (str): The path to the file.

    Attributes:
    file_path (str): The path to the file.
    file_type (str): The type of the file, determined by its extension.
    file (object): The file object for the given file path.

    Methods:
    read_page(page_num): Reads the text content of a page from the file.
    read_pages(page_nums): Reads the text content of multiple pages from the file.
    close(): Closes the file object.
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_type = os.path.splitext(file_path)[-1].lower()

        if self.file_type == ".pdf":
            try:
                self.file = pdfplumber.open(self.file_path)
            except Exception as e:
                print(f"Failed to open PDF file: {e}")
        elif self.file_type == ".docx":
            try:
                self.file = docx2txt.process(self.file_path)
            except Exception as e:
                print(f"Failed to open Word file: {e}")
        elif self.file_type == ".txt":
            try:
                with open(self.file_path, 'r') as f:
                    self.file = f.read()
            except Exception as e:
                print(f"Failed to open text file: {e}")
        elif self.file_type == ".html":
            try:
                with open(self.file_path, 'r') as f:
                    soup = BeautifulSoup(f, 'html.parser')
                    self.file = soup.get_text()
            except Exception as e:
                print(f"Failed to open HTML file: {e}")
        else:
            print("Unsupported file type")
            self.file = None

    def read_page(self, page_num):
        """
        Reads the text content of a page from the file.

        Args:
        page_num (int): The page number to read.

        Returns:
        str: The text content of the page.
        """
        if self.file_type == ".pdf":
            page = self.file.pages[page_num]
            text = page.extract_text()
        elif self.file_type == ".docx":
            try:
                text = self.file.split("\n")[page_num]
            except Exception as e:
                print(f"Failed to read page {page_num}: {e}")
                text = ""
        else:
            print("Unsupported file type")
            text = ""

        return text

    def read_pages(self, page_nums):
        """
        Reads the text content of multiple pages from the file.

        Args:
        page_nums (list of int): The list of page numbers to read.

        Returns:
        str: The text content of the selected pages.
        """
        texts = []
        for i, num in enumerate(page_nums):
            try:
                text = self.read_page(num)
                texts.append(text)
            except Exception as e:
                print(f"Failed to read page {num}: {e}")
            progress = (i + 1) / len(page_nums) * 100
            print(f"Processing page {i+1} of {len(page_nums)} ({progress:.2f}%)")
        return "\n\n".join(texts)

    def close(self):
        """
        Closes the file object.
        """
        if self.file_type == ".pdf":
            self.file.close()

class TextToSpeech:
    """
    A class for converting text to speech.

    Args:
        speed (float, optional): The speed at which the text should be spoken, defaults to 1.0.

    Attributes:
        speed (float): The speed at which the text should be spoken.
        language (str): The language in which the text should be spoken.
        paused (bool): Whether the speech playback is currently paused.

    Methods:
        set_language(language): Sets the language for speech synthesis.
        _play_audio(filename, output_format): Plays the audio file.
        transform(file_path, output_format): Converts text to speech and plays it.
        pause(): Pauses the speech playback.
        resume(): Resumes the speech playback.
    """
    def __init__(self, speed=1.0):
        """
        Initializes the TextToSpeech object.

        Args:
            speed (float, optional): The speed at which the text should be spoken, defaults to 1.0.
        """
        self.speed = speed
        self.language = None
        self.paused = False

    def set_language(self, language):
        """
        Sets the language for speech synthesis.

        Args:
            language (str): The language in which the text should be spoken.
        """
        self.language = language

    def _play_audio(self, filename, output_format):
        """
        Plays the audio file.

        Args:
            filename (str): The name of the file to play.
            output_format (str): The format of the output file.
        """

        try:
            if output_format == 'mp3':
                os.startfile(filename) # open the file automatically
            elif output_format == 'wav':
                pygame.mixer.music.load(filename)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
        except Exception as e:
            print(f"Failed to play audio file: {e}")

    def transform(self, file_path, output_format='mp3'):
        """
        Converts text to speech and plays it.

        Args:
            file_path (str): The path to the input file.
            output_format (str, optional): The format of the output file, defaults to 'mp3'.
        """
        try:
            file_reader = FileReader(file_path)
            pages = range(50, 55)
            text = file_reader.read_pages(pages)
            file_reader.close()

            gtts_transformer = gTTS(text=text, lang=self.language, slow=False)
            gtts_transformer.speed = self.speed
            filename = f"{os.path.splitext(file_path)[0]}.{output_format}"
            gtts_transformer.save(filename)

            self.paused = False
            t = threading.Thread(target=self._play_audio, args=(filename, output_format))
            t.start()

            while t.is_alive():
                if self.paused:
                    if output_format == 'mp3':
                        os.system("TASKKILL /F /IM Music.UI.exe") # stop the playback on Windows
                    elif output_format == 'wav':
                        pygame.mixer.music.pause()
                else:
                    time.sleep(0.1)
        except Exception as e:
            print(f"Failed to transform text to speech: {e}")

    def pause(self):
        """
        Set the 'paused' attribute of the object to True.
        """
        self.paused = True

    def resume(self):
        """
        Set the 'paused' attribute of the object to False.
        """
        self.paused = False


if __name__ == '__main__':
    """
    Convert a PDF file to an audio file using text-to-speech.
    """
    pdf_path = "e-books/alices-adventures-in-wonderland.pdf"
    try:
        tts = TextToSpeech(speed=1.5)
        tts.set_language("en")
        tts.transform(pdf_path, output_format='mp3')
        
        # tts.set_language("fr")
        # tts.transform(pdf_path, output_format='wav')
    except Exception as e:
        print(f"Error while processing text to speech: {e}")
    
    print("WORK DONE")





