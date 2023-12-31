import json
from collections import defaultdict
import json
import os
import pandas as pd
import csv


def create_dir(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def find_tag(specific_token, dict_tags):
    for str_of_chars in dict_tags:
        token_set = set(specific_token.split('_'))
        chars_set = set(str_of_chars.split('_'))
        common_ele = token_set.intersection(chars_set)
        if len(common_ele)>0:
            #print(specific_token, str_of_chars)
            return dict_tags[str_of_chars]
    return 'O'

def export_all_annotators(output_path, all_annotators, lang, reference_range=(1,101)):

    annotator_names = all_annotators.keys()

    output_file = output_path +lang+ '.tsv'
    with open(output_file, 'w') as f:
        for i in range(reference_range[0], reference_range[1]):
            words_ann_tags = defaultdict(lambda: defaultdict(str))
            for ann_idx, ann_name in enumerate(annotator_names):
                if i in all_annotators[ann_name]:
                    for w, word_tag in enumerate(all_annotators[ann_name][i]):
                        word, tag = word_tag
                        words_ann_tags[(w, word)][ann_idx] = tag


            for word in words_ann_tags:
                ne1 = words_ann_tags[word][0]
                ne2 = words_ann_tags[word][1]
                ne3 = words_ann_tags[word][2]
                if len(ne1.strip()) < 1: ne1 = 'O'
                if len(ne2.strip()) < 1: ne2 = 'O'
                if len(ne3.strip()) < 1: ne3 = 'O'
                f.write(word[1] + '\t' +  ne1 + '\n')

                print(word[1] + '\t' +  ne1)
            f.write('\n')

            '''
            for word in words_ann_tags:
                ne1 = words_ann_tags[word][0]
                ne2 = words_ann_tags[word][1]
                ne3 = words_ann_tags[word][2]
                if len(ne1.strip()) < 1: ne1 = 'O'
                if len(ne2.strip()) < 1: ne2 = 'O'
                if len(ne3.strip()) < 1: ne3 = 'O'
                if "," in word or '.' in word:
                    word = word.replace('.', ' . ')
                    word = word.replace(',', ' , ')
                    print(word)
                    for w in word.strip().split():
                        #f.write(w + '\t' + ne1 + '\t' + ne2 + '\t' + ne3 + '\n')
                        f.write(w + '\t' + ne1 + '\n')
                else:
                    #f.write(word + ' ' +  ne1+ ' ' + ne2 + ' ' + ne3 + '\n')
                    f.write(word + '\t' + ne1 + '\n')
            f.write('\n')
            '''



def extract_from_json_(dict_lang, data_path, lang, no_examp=510):

    list_data_ids = os.listdir(data_path)
    all_annotators = {}
    #print(dict_lang)
    for d_id in dict_lang[lang]:
        input_path = data_path+d_id+'/export.json'

        #if d_id not in list_data_ids: continue
        with open(input_path) as f:
            dict_ann = json.loads(f.read())

        #print(len(dict_ann['annotations']))
        #print(dict_ann)

        per_ann_sentences = {}
        for s, dict_sent in enumerate(dict_ann['annotations']):
            #print(s, dict_sent)
            content = dict_sent['text_snippet']['content']
            reference = int(dict_sent['reference'])

            tokens_annot = dict_sent['annotations']
            start_end_offset = {}
            for dict_token in tokens_annot:
                start_idx = dict_token['text_extraction']['text_segment']['start_offset']
                end_idx = dict_token['text_extraction']['text_segment']['end_offset']
                start_end_str = '_'.join([str(i) for i in range(start_idx, end_idx)])
                start_end_offset[start_end_str] = dict_token['display_name']
                #print(content[start_idx:end_idx])

            start_offsets = sorted(start_end_offset.keys())
            print(content)
            #print(tokens_annot)


            tokens = content.split()
            token_index = '_'.join([str(c) for c in list(range(len(content)))])
            print(token_index)

            beg_idx = 0
            annotated_words = []
            for tok in tokens:
                tok_start_end_str = '_'.join([str(i) for i in range(beg_idx, beg_idx + len(tok))])
                tag = find_tag(tok_start_end_str, start_end_offset)
                print(tok, tag)
                annotated_words.append((tok, tag))

                beg_idx += len(tok)+1

            #print(content)
            per_ann_sentences[reference] = annotated_words
            '''
            beg_content_indexes = sorted(dict_token_len.keys())
            annotated_words = []
            for beg_idx in beg_content_indexes:
                if beg_idx in start_offsets:
                    annotated_words.append((dict_token_len[beg_idx][0], start_end_offset[beg_idx][1]))
                else:
                    annotated_words.append((dict_token_len[beg_idx][0], 'O'))

            per_ann_sentences[reference] = annotated_words
            '''

        all_annotators[dict_lang[lang][d_id]] = per_ann_sentences
        output_path = 'data/ioAnnotator_tsv/' + lang + '/'
        create_dir(output_path)
        #print(all_annotators)
        export_all_annotators(output_path, all_annotators, lang, reference_range=(1,no_examp+1))
    #print(all_annotators)

    return all_annotators


def extract_sentences(dict_lang, lang='ne'):
    all_annotators = extract_from_json_(dict_lang, 'data/annotation_export/'+lang+'/', lang)




if __name__ == "__main__":
    '''
    dataset_id = '5703869787013120'

    dict_lang = defaultdict(lambda: defaultdict(str))
    #for sent in pos_lines[1:]:
        #d_id, lang, ann_name = sent.split('\t')
    dict_lang['en'][dataset_id]='David'
    dict_lang['en']['5703869787013121'] = 'Emma'
    dict_lang['en']['5703869787013122'] = 'Noah'
    '''
    dict_lang = defaultdict(lambda: defaultdict(str))
    # for sent in pos_lines[1:]:
    # d_id, lang, ann_name = sent.split('\t')
    #dict_lang['pcm']['5727602702548992'] = 'Group1'
    #extract_sentences(dict_lang, lang='pcm')

    dict_lang['yor']['5727531164499968'] = 'Group1'
    extract_sentences(dict_lang, lang='yor')

    dict_lang['eng']['5738484446789632'] = 'Group1'
    extract_sentences(dict_lang, lang='eng')