# IPA Transcription Training Software
----------------------------


### Description


The IPA Transcription Training Software is a tool that facilitates learning IPA symbols and training the transcription of English texts. It should be of great help to all students of English who want to learn the International Phonetic Alphabet or practice transcribing English texts.

The software allows its users to practice the IPA transcription at their own pace and in a personalized way (a range of training options available). Because of that, it is both, a useful supplement for students of English Philology/Linguistics and a stand-alone course for individuals who plan to learn the IPA transcription from scratch. 

In the future, the software might be extended to account for other languages and, possibly, other forms of practice (e.g. it could accept and analyze audio input, and thus enable the user to practice sound production).


### Functions

#### **Upload a text**
Allows for selecting a .txt file of the user's liking
#### **Choose training settings**
Allows for suiting training options to the user's needs. Current options include:
- selecting written or spoken mode
- selecting parts of speech
- selecting the number of words to practice
#### **Practice transcribing words**
Allows for practicing the transcription of English words


### External Modules

#### Word tokenization and POS tagging:
- **nltk** – a suite of libraries and programs for symbolic and statistical natural language processing (NLP) for English written in the Python programming language [(learn more)](https://www.nltk.org/)
#### Providing transcription:
- **eng_to_ipa** – a Python module which utilizes the Carnegie-Mellon University Pronouncing Dictionary to convert English text into the International Phonetic Alphabet [(learn more)](https://pypi.org/project/eng-to-ipa/)
#### Audio output:
- **gTTs** – a Python library and CLI tool to interface with Google Translate's text-to-speech API [(learn more)](https://pypi.org/project/gTTS/)
- **playsound** – a Python cross platform, single-function module with no dependencies for playing sounds. [(learn more)](https://pypi.org/project/playsound/)


### Requirements

For the program to run properly, you must install the abovementioned external modules. In case you do not do it, the program will redirect you to the corresponding websites when you run it. 

### Acknowledgement

Special thanks to Miroslav Bićanić from the University of Zagreb for helping me create the ipakb module.

### Contributing

If you want to introduce any changes to the program, please contact me first to discuss what you would like to modify. 

