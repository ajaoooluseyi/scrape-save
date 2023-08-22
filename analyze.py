import os
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

# Read the input.xlsx file
input_data = pd.read_excel('C:/Users/AJAO SEYI/Desktop/ML/Input.xlsx')

# Configure Selenium webdriver options
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run Chrome in headless mode (without opening the browser window)
chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration
chrome_options.add_argument('--no-sandbox')  # Disable sandbox mode

# Initialize the webdriver
#service = Service('path/to/chromedriver')  # Path to your chromedriver executable
driver = webdriver.Chrome(options=chrome_options)

# Iterate over each URL and extract the article text
for index, row in input_data.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    
    # Load the URL
    driver.get(url)
    
    # Wait for the article text to be loaded
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'article-content')))
    
    # Extract the article title and text
    try:
        # Find the article title element using XPath
        article_title = driver.find_element(By.XPATH, '//h1').text
    except NoSuchElementException:
        try:
            # Find the article title element using CSS selector
            article_title = driver.find_element(By.CSS_SELECTOR, 'h1').text
        except NoSuchElementException:
            try:
                # Find the article title element using class name
                article_title = driver.find_element(By.CLASS_NAME, 'article-title').text
            except NoSuchElementException:
                article_title = 'Article title not found'

    # Find the article text elements using XPath
    article_text_elements = driver.find_elements(By.XPATH, '//div[@class="td-pb-span8.td-main-content"]//p')


    if not article_text_elements:
        try:
            # Find the article text elements using CSS selector
            article_text_elements = driver.find_elements(By.CSS_SELECTOR, '.td-pb-span8.td-main-content')
        except NoSuchElementException:
            pass
    
     # Extract the article text
    article_text = '\n'.join([element.text for element in article_text_elements])       

    # Create a text file with the URL_ID as the filename and save the extracted article
    filename = f'{url_id}.txt'
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f'{article_title}\n\n{article_text}')
        print(f'Article saved: {filename}')

# Quit the webdriver
driver.quit()

# Create a DataFrame to store the combined data
combined_data = pd.DataFrame()

# Append the input data to the combined data
combined_data = pd.concat([combined_data, pd.DataFrame(input_data)], ignore_index=True)

# Path to the Text folder
text_folder = "C:/Users/AJAO SEYI/Desktop/ML/scrape_save/extract/Text"

# Path to the StopWords folder
stopwords_folder = "C:/Users/AJAO SEYI/Desktop/ML/scrape_save/extract/StopWords"

# Path to the MasterDictionary folder
master_dict_folder = "C:/Users/AJAO SEYI/Desktop/ML/scrape_save/extract/MasterDictionary"

# Get the list of stopwords files
stopwords_files = [f for f in os.listdir(stopwords_folder) if f.startswith("StopWords_")]

# Create a set to store the stopwords
stopwords = set()

# Read stopwords from each file and add them to the set
for filename in stopwords_files:
    with open(os.path.join(stopwords_folder, filename), "r") as file:
        stopwords.update(file.read().split())

# Create a dictionary to store positive and negative words
word_dict = {"positive": set(), "negative": set()}

# Process positive and negative word files
for sentiment in ["positive", "negative"]:
    filename = f"{sentiment}-words.txt"
    with open(os.path.join(master_dict_folder, filename), "r") as file:
        words = file.read().split()

        # Add words to the dictionary if they are not stopwords
        word_dict[sentiment].update(word for word in words if word.lower() not in stopwords)

# Regex pattern to find personal pronouns
pronoun_pattern = re.compile(r'\b(I|we|my|ours|us)\b', re.IGNORECASE)

# Process text files
for filename in os.listdir(text_folder):
    if filename.endswith(".txt"):
        # Read the text file
        with open(os.path.join(text_folder, filename), "r", encoding="utf-8") as file:
            text = file.read()

        # Clean the text by excluding stopwords
        cleaned_text = ' '.join(word for word in text.split() if word.lower() not in stopwords)

        # Tokenize the cleaned text
        tokens = word_tokenize(cleaned_text)

        # Calculate positive score
        positive_score = sum(1 for token in tokens if token.lower() in word_dict["positive"])

        # Calculate negative score (multiplied by -1)
        negative_score = sum(1 for token in tokens if token.lower() in word_dict["negative"]) * -1

        # Calculate polarity score
        polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)

        # Calculate word count
        word_count = len(tokens)

        # Calculate subjectivity score
        subjectivity_score = (positive_score + negative_score) / (word_count + 0.000001)

        # Calculate average sentence length
        sentences = sent_tokenize(text)
        sentence_count = len(sentences)
        average_sentence_length = word_count / sentence_count

        # Calculate percentage of complex words
        complex_word_count = sum(1 for token in tokens if len(token) > 2)
        percentage_complex_words = (complex_word_count / word_count) * 100

        # Calculate Fog Index
        fog_index = 0.4 * (average_sentence_length + percentage_complex_words)

        # Calculate average number of words per sentence
        average_words_per_sentence = word_count / sentence_count

        # Calculate complex word count (words with more than two syllables)
        complex_word_count = sum(1 for token in tokens if len(token) > 2)

        # Calculate syllable count per word
        syllable_count_per_word = sum(len(re.findall(r'[aeiouy]+', word.lower())) for word in tokens)

        # Calculate personal pronoun count
        personal_pronoun_count = len(re.findall(pronoun_pattern, cleaned_text))

        # Calculate average word length
        total_character_count = sum(len(word) for word in tokens)
        average_word_length = total_character_count / word_count

        # Create a dictionary of the output data
        output_row = {"POSITIVE SCORE": positive_score,
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

        # Append the output data row to the combined data
        output_df = pd.DataFrame(output_row, index=[0])
        combined_data = pd.concat([combined_data, output_df], ignore_index=True)
        
        
        # Save the DataFrame to an Excel file
        combined_data.to_excel("Output Data Structure.xlsx", index=False)
        print(f"Processed {filename}.")
