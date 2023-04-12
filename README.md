# Text to Speech (TTS) script

## Overview
This Python script utilizes several libraries to enable reading and conversion of various file formats into either MP3 or WAV speech format. Supported file formats include PDF, DOCX, TXT, and HTML, with the added capability to process multiple pages for PDF and DOCX files.

## Requirements
To run the script, the following libraries need to be installed on your machine:

- `pdfplumber`
- `gtts`
- `pygame`
- `docx2txt`
- `BeautifulSoup`
## Usage
To use this script, follow these steps:

- Create an instance of the TextToSpeech class.
- Set the language (if required) by calling the set_language() method.
- Call the transform() method with the file path and desired output format as parameters.
Here's an example of how to use the script to transform a PDF file into speech in MP3 format:
```python
tts = TextToSpeech()
tts.set_language('en')
tts.transform('path/to/file.pdf', output_format='mp3')
```
## Output file
The output file will be saved in the same directory as the input file with the same filename and the appropriate extension.

## Limitations
This script was developed and tested on the Windows operating system. The playback function in the TextToSpeech class relies on the operating system's default media player. Some modifications may be necessary to run this script on other operating systems.

## Code structure
The script has two classes:

- `FileReader`: This class is responsible for reading the input file and returning its content in a usable format. It supports different file formats and can read pages of PDF and DOCX files. If the file format is not supported, an error message is displayed.

- `TextToSpeech`: This class is responsible for transforming the text to speech. The speed of speech can be adjusted and the language of speech can also be set by calling the set_language() method. The transform() method will process the input file, convert it to speech, and save it in the specified output format (MP3 or WAV). It also starts playing the speech automatically and provides a pause/resume functionality while playing. An error message will be displayed if any issues arise during this process.
