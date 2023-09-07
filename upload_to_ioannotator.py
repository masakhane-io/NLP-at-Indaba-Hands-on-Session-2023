import os

import requests
import csv
import xmltodict
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize

# get your API key https://app.ioannotator.com/api
params = {'apikey': 'add api key'}
api = 'https://api.ioannotator.com/import/texts'


def read_text(filenam):
    with open(filenam) as f:
        text_lines = f.read().splitlines()

    return text_lines


def tokenize_articles(lang, dir_name):
    input_path = dir_name
    df = pd.read_csv(input_path)

    df['no_words'] = df['Scrapped_text'].str.split().str.len()
    #sorted_df = df.sort_values(by=['no_words'], ascending=False)

    #print(sorted_df.iloc[1])

    articles = list(df['Scrapped_text'].values)
    sentences = []
    for art in articles:
        try:
            if lang=='am':
                sent = art.split('።')
                sent = [s+' ።' for s in sent]
            else:
                sent = nltk.tokenize.sent_tokenize(art)
            if len(sent) > 10:
                sentences.append(sent)
            #elif lang=='din' and len(sent) >=10:
            #    sentences.append(sent)
        except:
            pass


    print(len(sentences))
    sel_sentences = []


    no_cnt = 0
    with open('top_1000_sents/'+lang+'.txt', 'w') as f:
        for art in sentences:
            for sent in art:
                if '[' in sent or ']' in sent or '|' in sent: continue

                if lang in ['am']:
                    list_words = sent.split()
                else:
                    list_words = word_tokenize(sent)
                sent_str = ' '.join(list_words)
                f.write(sent_str+'\n')
                no_cnt+=1
            f.write('\n')

            #if no_cnt > 1000: break
            if no_cnt > 5000: break




def upload_language_document(lang, dataset_id):

    if lang in ['kab', 'kcg', 'pcm', 'rn', 'st', 'sw', 'tw', 'wo', 'xh', 'yo', 'zu']:
        lang = lang+'_edited'

    sentences = read_text('top_1000_sents/'+lang+'.txt')
    sel_sentences = []
    for sent in sentences[:1000]:
        if len(sent.strip()) < 2: continue
        sel_sentences.append(sent)


    for s, row in enumerate(sel_sentences[:100]):
        data = {
            'dataset': dataset_id,
            'text': row,
            'reference': s+1,
        }

        x = requests.post(api, json=data, params=params)
        print(s, x)
    print("\n")


def get_label_dict():
    label_dict = {'PER':'P', 'ORG':'O', 'LOC':'L', }
    print(len(label_dict), label_dict)

    return label_dict


def add_labels(labels_dict, dataset_id):

    for category, shortcut in labels_dict.items():
        payload = {
            "name": category,
            "dataset": dataset_id,
            "key": shortcut
        }

        r = requests.post("https://api.ioannotator.com/label?apikey=8C540MR-DQ4MXEK-GR4ZSCV-X51QYMZ", json=payload)
        print(dataset_id, r)

if __name__ == '__main__':

    '''
    dir_name = 'scrapped_articles/'
    languages = list(os.listdir(dir_name))
    languages = [l[:-4] for l in languages]
    for lang in languages:
        print(lang)
        dir_name = 'scrapped_articles/'+lang+'.csv'
        label_dict = get_label_dict()

        # 1. PCM
        tokenize_articles(lang, dir_name)
    '''


    lang_datasetname = {
        'af': '5684147406241792', 'am': '5677095229325312', 'ary': '5681867072208896', 'arz': '5767682464940032',
        'ee': '5766515576012800', 'ff': '5649803438456832', 'fr': '5747494172491776', 'ha': '5725974373072896',
        'ig': '5659503982804992', 'lg': '5722749163012096', 'ln': '5704323979804672', 'mg': '5634436741726208',
        'nqo': '5121197452820480', 'om': '5759567031959552', 'ny': '5700708087103488', 'pcm': '5700134104989696',
        'rw': '5160364626935808', 'rn': '5635397472223232', 'sn': '5086853485035520', 'so': '5118917118787584',
        'tn': '5665428755972096', 'tw': '5641506970927104', 'wo': '5184544219070464', 'xh': '5656598949134336',
        'zu': '5711682307358720', 'yo': '5727531164499968', 'nso': '5682410830168064', 'ss': '5701862695108608',
        'st': '5672397206192128', 'tum': '5204732511518720', 'ts': '5732758945005568', 'kab': '5740021197832192',
        'guw': '5096554029383680', 'en': '5693052207235072', 'ki': '5685855083560960', 'sw': '5725521388240896',
        'din': '5671432247836672', 'bm': '5686626164408320', 'shi': '5737883981840384', 'pt': '5642147659251712',
        'practice': '5738484446789632', 'yo_practice':'5650928946380800'

    }

    label_dict = get_label_dict()
    #upload_language_document('practice', lang_datasetname['practice'])
    #add_labels(label_dict, lang_datasetname['practice'])

    #upload_language_document('yo_practice', lang_datasetname['yo_practice'])
    #add_labels(label_dict, lang_datasetname['yo_practice'])


    for lang in lang_datasetname:
        print(lang)
        upload_language_document(lang, lang_datasetname[lang])
        add_labels(label_dict, lang_datasetname[lang])