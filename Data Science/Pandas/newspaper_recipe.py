import nltk
from nltk.corpus import stopwords
import numpy as np
import pandas as pd
from urllib.parse import urlparse
import argparse
import logging
import hashlib
logging.basicConfig(level=logging.INFO)

stop_words = set(stopwords.words('spanish'))
logger = logging.getLogger(__name__)


def main(filename):
    logger.info('Starting cleaning process')

    df = _read_data(filename)
    print('print csv ***')
    print(df.loc[9]['title'])
    df.loc[9]['title'] = np.NaN
    print(df.loc[9]['title'])

    newspaper_uid = _extract_newspaper_uid(filename)
    df = _add_newspaper_uid_column(df, newspaper_uid)
    df = _extrac_host(df)
    print(df['title'])
    df = _fill_missing_titles(df)
    df = _generate_uids_for_rows(df)
    df = _remove_new_lines_from_body(df, '\n', '')
    df['n_tokens_title'] = _tokenize_column(df, 'title')
    df['n_tokens_body'] = _tokenize_column(df, 'body')
    df = _remove_duplicate_entries(df,'title')
    print(df)

    df = _drop_rows_with_missing_data(df)
    _save_data(df, filename)
    return df


def _read_data(filename):
    logger.info('Reading file {}'.format(filename))

    return pd.read_csv(filename)


def _extract_newspaper_uid(filename):
    logger.info('Extracting newspaper uid {}'.format(filename))
    newspaper_uid = filename.split('_')[0]
    logger.info('Newspaper uid detected {}'.format(newspaper_uid))

    return newspaper_uid


def _add_newspaper_uid_column(df, newspaper_uid):
    logger.info('Filling newspaper_uid column with {}'.format(newspaper_uid))
    df['newspaper_uid'] = newspaper_uid
    return df


def _extrac_host(df):
    logger.info('Extracting host from urls')
    df['host'] = df['url'].apply(lambda url: urlparse(url).netloc)

    return df


def _fill_missing_titles(df):
    logger.info('Filling missing titles')
    missing_titles_mask = df['title'].isnull()

    missing_titles = (df[missing_titles_mask]['url']
                      .str.extract(r'(?P<missing_titles>[^/]+)$')
                      .map(lambda title: title.split('-'))
                      .map(lambda title_word_list: ' '.join(title_word_list))
                      )

    df.loc[missing_titles_mask, 'title'] = missing_titles
    return df


def _generate_uids_for_rows(df):
    logger.info('Generating uids for each url')
    uids = ((df
             .apply(lambda row: hashlib.md5(bytes(row['url'].encode())), axis=1)
             .apply(lambda hash_object: hash_object.hexdigest())
             ))
    df['uid'] = uids

    return df.set_index('uid')


def _remove_new_lines_from_body(df, text, replace):
    logger.info('Remove new lines from body')

    stripped_body = (df
                     .apply(lambda row: row['body'], axis=1)
                     .apply(lambda body: list(body))
                     .apply(lambda letters: list(map(lambda letter: letter.replace(text, replace), letters)))
                     .apply(lambda letters: ''.join(letters))
                     )

    df['body'] = stripped_body

    return df


def _tokenize_column(df, column_name):

    logger.info('Tokenizing the column {}'.format(column_name))

    return(df
           .dropna()
           .apply(lambda row: nltk.word_tokenize(row[column_name]), axis=1)
           .apply(lambda tokens: list(filter(lambda token: token.isalpha(), tokens)))
           .apply(lambda tokens: list(map(lambda token: token.lower(), tokens)))
           .apply(lambda word_list: list(filter(lambda word: word not in stop_words, word_list)))
           .apply(lambda valid_word_list: len(valid_word_list))
           )

def _remove_duplicate_entries(df,column):
    logger.info('Remove duplicates in {} column'.format(column))
    df.drop_duplicates(subset=[column], keep= 'first', inplace= True)
    return df


def _drop_rows_with_missing_data(df):
    logger.info('Remove nonvalues rows')
    return df.dropna()

def _save_data(df, filename):
    filename = 'clean_{}'.format(filename)
    logger.info('Save file in {}'.format(filename))
    df.to_csv(filename)

    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',
                        help='The path to the dirty data',
                        type=str)

    arg = parser.parse_args()
    df = main(arg.filename)

    # print(df)
