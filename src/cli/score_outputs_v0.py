import argparse, json
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('-i','--in_csv',default='outputs/manual_scores/dialect_word_pilot_v0.csv')
parser.add_argument('-o','--out',default='outputs/score_summary_dialect_word_pilot_v0.json')
parser.add_argument('-p','--pair',default='outputs/pairing_dialect_word_pilot_v0.json')

def main():
    args = parser.parse_args()
    input_path = args.in_csv
    output_path = args.out
    pair_path = args.pair
    print('Input path:', input_path)
    print('Output path:', output_path)

    ds = pd.read_csv(input_path)
    ds = ds[
        ds['register'].isin(['formal','informal']) &
        ds['rubric_number'].between(1, 10) &
        ((ds['rubric_number'].between(1, 7) & ds['score'].isin([0, 2]))|
        (ds['rubric_number'].between(8, 10) & ds['score'].isin([0, 1])))
        ]
    print(ds.groupby(['intent_id', 'register']).size())
    max_total_score = 17
    rubric_item_num = 10
    scoring_style = 'binary'

    total_score_ds = ds.groupby(['intent_id','register'],as_index=False)['score'].sum().rename(
        columns = {'score':'total_score'}
    )

    responses = {}
    for _, row in total_score_ds.iterrows():
        suffix = 'f' if row['register'] == 'formal' else 'i'
        response_id = f'{row["intent_id"]}_{suffix}'
        responses[response_id] = {
            'intent_id': int(row['intent_id']),
            'register': row['register'],
            'total_score': row['total_score'],
            'max_score': max_total_score
        }

    intent_ids = total_score_ds['intent_id'].drop_duplicates().sort_values(ascending = False).tolist()
    intent_ids = [int(x) for x in intent_ids]
    meta = {
        'source_csv': input_path,
        'max_total_score': max_total_score,
        'rubric_item_num': rubric_item_num,
        'scoring_style': scoring_style,
        'intent_id_num': len(intent_ids),
        # 'intend_ids': intent_ids
    }

    summary = {
        'meta': meta,
        'responses': responses
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

    # Pairing results
    pairs = {}
    for intent_id, group in total_score_ds.groupby('intent_id'):
        formal_total = int(group.loc[group['register'] == 'formal', 'total_score'].iloc[0])
        informal_total = int(group.loc[group['register'] == 'informal', 'total_score'].iloc[0])

        pairs[intent_id] = {
            'formal_total': formal_total,
            'informal_total': informal_total,
            'delta_informal_to_formal': informal_total - formal_total
        }

    pairs_summary = {
        'total_pair_num': len(pairs),
        'pairs': pairs
    }

    with open(pair_path, 'w', encoding='utf-8') as f:
        json.dump(pairs_summary, f, indent = 2)

if __name__ == '__main__':
    main()
