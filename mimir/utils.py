# coding=utf-8
import os
import json
import datasets
import requests

def save_dict_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

def process_double_agent(temp):
    data = []
    for topic in temp:
        x = temp[topic]
        x = x.split("[Human]")[1:]
        if len(x) != 0:
            s = ""
            for y in x:
                if "[AI]" in y:
                    y = y.split("[AI]")
                    if len(y) == 2:
                        s += (
                                "[|Human|] "
                                + y[0].strip()
                                + "\n"
                                + "[|AI|] "
                                + y[1].strip()
                                + "\n"
                        )
                    else:
                        break
                else:
                    break
            if s != "":
                prompt = "The conversation between human and AI assistant.\n"
                s = prompt + s + "[|Human|] "
                data.append({"instruction": topic, "input":'', "output": s})
    return data

def process_mutil_agent(temp, role_list):
    data = []
    person = ','.join(role_list)
    for key in temp:
        list_talk = a[key]
        talk_content = ''
        for str_person in list_talk:
            talk_content += str_person
        if talk_content != "":
            prompt = "The {} had a conversation.\n".format(person)
            talk_content = prompt + talk_content
            data.append({"instruction": key, "input":'', "output": talk_content})
    return data


def removeHyphen(example):
    example_clean = {}
    for key in example.keys():
        if "-" in key:
            new_key = key.replace("-", "_")
            example_clean[new_key] = example[key]
        else:
            example_clean[key] = example[key]
    example = example_clean
    return example


def renameDatasetColumn(dataset):
    col_names = dataset.column_names
    for cols in col_names:
        if "-" in cols:
            dataset = dataset.rename_column(cols, cols.replace("-", "_"))
    return dataset


#
# Helper functions for datasets library
#


def get_dataset_builder(path, conf=None):
    "Get a dataset builder from name and conf."
    module_path = datasets.load.dataset_module_factory(path)
    builder_cls = datasets.load.import_main_class(module_path.module_path, dataset=True)
    if conf:
        builder_instance = builder_cls(name=conf, cache_dir=None, hash=module_path.hash)
    else:
        builder_instance = builder_cls(cache_dir=None, hash=module_path.hash)
    return builder_instance


def get_dataset(path, conf=None):
    "Get a dataset from name and conf."
    builder_instance = get_dataset_builder(path, conf)
    if builder_instance.manual_download_instructions is None and builder_instance.info.size_in_bytes is not None:
        builder_instance.download_and_prepare()
        return builder_instance.as_dataset()
    else:
        return load_dataset(path, conf)


def load_dataset(dataset_name, subset_name):
    try:
        return datasets.load_dataset(dataset_name, subset_name)
    except datasets.builder.ManualDownloadError:
        cache_root_dir = (
            os.environ["PROMPTSOURCE_MANUAL_DATASET_DIR"]
            if "PROMPTSOURCE_MANUAL_DATASET_DIR" in os.environ
            else DEFAULT_PROMPTSOURCE_CACHE_HOME
        )
        data_dir = (
            f"{cache_root_dir}/{dataset_name}"
            if subset_name is None
            else f"{cache_root_dir}/{dataset_name}/{subset_name}"
        )
        return datasets.load_dataset(
            dataset_name,
            subset_name,
            data_dir=data_dir,
        )


def get_dataset_confs(path):
    "Get the list of confs for a dataset."
    module_path = datasets.load.dataset_module_factory(path).module_path
    # Get dataset builder class from the processing script
    builder_cls = datasets.load.import_main_class(module_path, dataset=True)
    # Instantiate the dataset builder
    confs = builder_cls.BUILDER_CONFIGS
    if confs and len(confs) > 1:
        return confs
    return []


def render_features(features):
    """Recursively render the dataset schema (i.e. the fields)."""
    if isinstance(features, dict):
        return {k: render_features(v) for k, v in features.items()}
    if isinstance(features, datasets.features.ClassLabel):
        return features.names

    if isinstance(features, datasets.features.Value):
        return features.dtype

    if isinstance(features, datasets.features.Sequence):
        return {"[]": render_features(features.feature)}
    return features


#
# Loads dataset information
#


def filter_english_datasets():
    """
    Filter English datasets based on language tags in metadata.

    Also includes the datasets of any users listed in INCLUDED_USERS
    """
    english_datasets = []

    response = requests.get("https://huggingface.co/api/datasets?full=true")
    tags = response.json()

    for dataset in tags:
        dataset_name = dataset["id"]

        is_community_dataset = "/" in dataset_name
        if is_community_dataset:
            user = dataset_name.split("/")[0]
            if user in INCLUDED_USERS:
                english_datasets.append(dataset_name)
            continue

        if "cardData" not in dataset:
            continue
        metadata = dataset["cardData"]

        if "language" not in metadata:
            continue
        languages = metadata["language"]

        if "en" in languages or "en-US" in languages:
            english_datasets.append(dataset_name)

    return sorted(english_datasets)


def list_datasets():
    """Get all the datasets to work with."""
    dataset_list = filter_english_datasets()
    dataset_list.sort(key=lambda x: x.lower())
    return dataset_list
