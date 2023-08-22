# scrape-save

This is a Python Selenium Web scraping code to get extract article text from urls provided in Input.xslx
It then scans each article and performs the following:
- Scans for words in StopWords dictionary and removes them from each article
- Create a positive and negative words dislctionary
- Return the data format below stored in an excel(.xslx) format.
  {"POSITIVE SCORE": positive_score,
                      "NEGATIVE SCORE": negative_score,
                      "POLARITY SCORE": polarity_score,
                      "SUBJECTIVITY SCORE": subjectivity_score,
                      "AVG SENTENCE LENGTH": average_sentence_length,
                      "PERCENTAGE OF COMPLEX WORDS": percentage_complex_words,
                      "FOG INDEX": fog_index,
                      "AVG NUMBER OF WORDS PER SENTENCE": average_words_per_sentence,
                      "COMPLEX WORD COUNT": complex_word_count,
                      "WORD COUNT": word_count,
                      "SYLLABLE PER WORD": syllable_count_per_word,
                      "PERSONAL PRONOUNS": personal_pronoun_count,
                      "AVG WORD LENGTH": average_word_length}

## To run the script
On the terminal execute the below command to create the projects' working directory and move into that directory.

 
```python
$ mkdir app
cd app
```

In the projects' working directory execute the below command to create a virtual environment for our project. Virtual environments make it easier to manage packages for various projects separately.

 
```python
$ py -m venv venv
```

To activate the virtual environment, execute the below command.

```python
$ source venv/Script/activate
```
Clone this repository in the projects' working directory by executing the command below.

```python
$ git clone https://github.com/ajaoooluseyi/scrape-save.git
$ cd scrape-save
```

To install all the required dependencies execute the below command.

```python
$ pip install -r requirements.txt
```

To run the app, navigate to the app folder in your virtual environment and execute the below command
```python
$ py analyze.py
```
