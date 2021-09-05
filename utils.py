import os
import json
import pandas as pd


def load_dataset(response_path="data/anonymized_project.json", reference_path="data/references.json"):
    """Just a little helper function to load the dataset into a pandas dataframe.
    """

    if os.path.exists("data/responses.pkl") and os.path.exists("data/references.pkl"):
        df_responses = pd.read_pickle("data/responses.pkl")
        df_references = pd.read_pickle("data/references.pkl")
        return df_responses, df_references

    with open(response_path, "r") as f1, open(reference_path, "r") as f2:
        d_responses = json.load(f1)
        d_references = json.load(f2)

    res_results = d_responses['results']['root_node']['results']
    df_responses = []
    for _, record in res_results.items():
        repeats = pd.json_normalize(record, record_path='results')
        df_responses.append(repeats)
    df_responses = pd.concat(df_responses, ignore_index=True)

    print("loaded responses")
    df_references = pd.DataFrame.from_dict(d_references, orient='index')
    print("loaded references")
    # store parsed dataframes to disk, since we don't want to redo the parsing everytime.
    # Note: In the context of a larger project one would likely want to use a database for this, but for a explorative
    # task this should be good enough.

    df_responses.to_pickle("data/responses.pkl")
    df_references.to_pickle("data/references.pkl")

    return df_responses, df_references


def prepare_dataframe(res):
    # rename columns for quality of life
    res = res.rename(columns={'task_output.answer': "str_answer",
                              "task_input.image_url": "img_url",
                              "task_output.cant_solve": "cant_solve",
                              "task_output.corrupt_data": "corrupt_data",
                              "task_output.duration_ms": "duration_ms",
                              "user.vendor_id": "vendor_id",
                              "user.id": "user_id",
                              "user.vendor_user_id": "vendor_user_id"
                              })

    # add columns with boolean answer tags and image ids
    res['answer'] = res['str_answer'].replace({'yes': True, 'no': False, '': 'invalid'})
    res['img_id'] = res['img_url'].apply(lambda x: x.split("/")[-1].split(".")[0])

    # drop obsolete columns
    res = res.drop(columns=["project_root_node_input_id", "loss", 'root_input.image_url'])

    return res