#!/usr/bin/env python
"""Homograph disambiguation training and evaluation."""

import csv
import glob

from typing import Dict, List, Tuple

import nltk  # type: ignore
import sklearn.feature_extraction  # type: ignore
import sklearn.linear_model  # type: ignore

import statistics

FeatureVector = Dict[str, str]
FeatureVectors = List[FeatureVector]


TRAIN_TSV = "data/train/*.tsv"


def tokens_checkpoint(x: int, tokens):
    if x < 0 or x >= len(tokens):
        return "(Index out of range)"
    else:
        if tokens[x].isnumeric():
            return "[NUMERIC]"
        else:
            return tokens[x].casefold()


def extract_features(
    sentence: str, homograph: str, start: int, end: int
) -> FeatureVector:
    """Extracts feature vector for a single sentence."""
    # There is some tricky stuff to find the target homograph word here.
    sentence_b = sentence.encode("utf8")
    left = sentence_b[:start]
    target = b"^" + sentence_b[start:end] + b"^"
    right = sentence_b[end:]
    sentence = (left + target + right).decode("utf8")
    tokens = nltk.word_tokenize(sentence)
    t = -1
    for (i, token) in enumerate(tokens):
        if token.count("^") == 2:
            t = i
            break
    assert t != -1, f"target homograph {homograph!r} not found"
    target = tokens[t].replace("_", "")
    # Now onto feature extraction.
    features: Dict[str, str] = {}

    prev_token = t - 1
    prev2_token = t - 2
    next_token = t + 1
    next2_token = t + 2

    features["t-1"] = tokens_checkpoint(prev_token, tokens)
    features["t-2"] = tokens_checkpoint(prev2_token, tokens)
    features["t+1"] = tokens_checkpoint(next_token, tokens)
    features["t+2"] = tokens_checkpoint(next2_token, tokens)
    features["t-2^t-1"] = features.get("t-2") + "^" + features.get("t-1")
    features["t+1^t+2"] = features.get("t+1") + "^" + features.get("t+2")
    features["t-1^t+1"] = features.get("t-1") + "^" + features.get("t+1")
    if target.isupper():
        features["cap(t)"] = "upper"
    elif target.islower():
        features["cap(t)"] = "lower"
    elif target.istitle():
        features["cap(t)"] = "title"
    else:
        features["cap(t)"] = "neither upper, lower, or title"

    return features
# returns dictionary of features called FeatureVector


def extract_features_file(path: str) -> Tuple[FeatureVectors, List[str]]:
    """Extracts feature vectors for an entire TSV file."""
    features: FeatureVectors = []       # List[Dict[str, str]] = []
    labels: List[str] = []
    with open(path, "r") as source:
        for row in csv.DictReader(source, delimiter="\t"):
            labels.append(row["wordid"])
            features.append(
                extract_features(
                    row["sentence"],
                    row["homograph"],
                    int(row["start"]),
                    int(row["end"]),
                )
            )
    return features, labels


def main() -> None:
    correct: List[int] = []
    size: List[int] = []
    for train_path in glob.iglob(TRAIN_TSV):
        features, labels = extract_features_file(train_path)
        vectorizer = sklearn.feature_extraction.DictVectorizer()
        train_feature_vect = vectorizer.fit_transform(features)
        model = sklearn.linear_model.LogisticRegression(
            penalty="l1",
            C=10,
            solver="liblinear",
        )
        model.fit(train_feature_vect, labels)
        test_path = train_path.replace("train", "test")
        test_feat, test_labels = extract_features_file(test_path)
        test_feature_vect = vectorizer.transform(test_feat)
        predicted = model.predict(test_feature_vect)
        assert len(predicted) == len(test_labels)
        right = 0
        total = len(predicted)
        for i in range(total):
            if predicted[i] == test_labels[i]:
                right += 1
        correct.append(right)
        size.append(len(test_labels))
    total_c = 0
    total_s = 0
    list_accuracies = []
    for (c, s) in zip(correct, size):
        total_c += c
        total_s += s
        list_accuracies.append(c / s)
    print(f"Micro-averaged accuracy: {total_c / total_s}")
    print(f"Macro-averaged accuracy: {statistics.mean(list_accuracies)}")


if __name__ == "__main__":
    main()
