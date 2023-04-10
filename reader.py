import pdfplumber
import os
import threading
import time
from gtts import gTTS
import pygame
import docx2txt
from bs4 import BeautifulSoup

class FileReader:
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
        if self.file_type == ".pdf":
            self.file.close()

class TextToSpeech:
    def __init__(self, speed=1.0):
        self.speed = speed
        self.language = None
        self.paused = False

    def set_language(self, language):
        self.language = language

    def _play_audio(self, filename, output_format):
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
        self.paused = True

    def resume(self):
        self.paused = False


if __name__ == '__main__':
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





