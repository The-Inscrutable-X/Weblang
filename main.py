from webscraping import *
from simple_translator import *
from sentence_segmentation import display_separated
from understandability_algorithm import Understandability
#import PySimpleGUI as pg

#"""setup gui"""

#window = sg.Window(title="Hello World", layout=[[]], margins=(100, 50)).read()

"""setup selenium"""
print('setting up selenium')
os.environ['PATH'] += r';D:/Selenium_webautomation_drivers'
options = Options()
options.headless = False
driver = webdriver.Chrome(options=options)
print('finished setting up selenium')
"""
googlesearch query
breakfast, the first response brings us to a good connection with japan '朝ご飯', https://www.kurashiru.com/lists/d5d8b53c-5cf2-4c4b-b623-9f95ca0666ab
the problem is that curated information souces, like geeksforgeeks often lack detailed or up to date information.
english query = lightning,
Alt: 朝ごはん,
Result: query: 朝ご飯, sentence: 1000人が絶賛の朝ご飯レシピ, trans: Breakfast recipe acclaimed by 1000 people
"""
language = 'ja'
query_origin = '化石'
query = '"'+query_origin+'"'
target_sentences = 50
#query = query_origin

print('ai training start')
response = search(query, tld='co.in', num = 10, stop = 10, pause = 2)
understandability_algorithm = Understandability('data_to_train.csv', debug = False)
understandability_algorithm.train()
print('ai training_done')
#print('Class testing:', understandability_algorithm.predict("vocabs are ontime and dazzling and fantastic."))
#quit()

response = search(query, tld='co.in', pause = 2, lang = language)
with open('storage.csv', 'w', encoding='utf8') as f:
    good_sentences = 0
    output_sentences = []
    for x in range(3):
        if good_sentences >= target_sentences:
            break
        print(x)
        sentences, url = parse_another_site(response, driver, f, query_origin)
        for x, sentence in enumerate(sentences):
            output_sentences.append((sentence, url))
            good_sentences += 1

            api_broken = True
            if api_broken == False:
                converted_sentence, converted_sentence_pronounciation = translateEnglish(sentence)
                """with open('storage.txt', 'a', encoding='utf8') as g:
                    g.writelines('|original', sentence, '\n|translated', converted_sentence, '\n|pronounciation', converted_sentence_pronounciation, '\n')
                    pass"""
                if converted_sentence_pronounciation == None:
                    score = understandability_algorithm.predict(converted_sentence)
                elif converted_sentence_pronounciation != None:
                    score = understandability_algorithm.predict(converted_sentence_pronounciation)

                if score == 1:
                   output_sentences.append([sentence, converted_sentence, converted_sentence_pronounciation, url, score])
                   good_sentences += 1




    print('finished')
    #converted_sentence, converted_sentence_pronounciation = translate_text('en', sentence)
    try:
        with open('output.txt', 'a+', encoding='utf8') as f:
            f.write('\n\n')
            f.write('\n'.join([str(i) for i in output_sentences]))
        checkout = output_sentences[0][1]
        checkout_sentence = output_sentences[0][0]
        driver.get(checkout)
        import pyperclip
        pyperclip.copy(checkout_sentence)
        spam = pyperclip.paste()
        #print(spam)
        if api_broken == False:
            converted_sentence, converted_sentence_pronounciation = translateEnglish(sentence)
            print('\n|original', sentence, '\n|translated', converted_sentence, '\n|pronounciation', converted_sentence_pronounciation, '\n|url', url, '\n|comprehension level', score)
            display_separated(converted_sentence_pronounciation, 'en')
    except IndexError:
        print('query busted, do not include underlines, query must exist in website text exactly')
    input('quit? ')
    driver.quit()
