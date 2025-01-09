"""Original case templates with independently supplied expected results."""
import copy
import re

TEMPLATES = [('calculate recall and reciprocal rank at the supplied cutoff', {'k': 2, 'queries': [{'id': 'q{n}', 'relevant': ['a', 'b'], 'ranked': ['x', 'a']}]}, {'queries': [{'id': 'q{n}', 'recall_at_k': 0.5, 'reciprocal_rank_at_k': 0.5}], 'mean_recall_at_k': 0.5, 'mean_reciprocal_rank_at_k': 0.5}), ('include empty relevance sets as zero in the documented macro average', {'k': 1, 'queries': [{'id': 'a{n}', 'relevant': ['d'], 'ranked': ['d']}, {'id': 'b{n}', 'relevant': [], 'ranked': []}]}, {'queries': [{'id': 'a{n}', 'recall_at_k': 1.0, 'reciprocal_rank_at_k': 1.0}, {'id': 'b{n}', 'recall_at_k': 0.0, 'reciprocal_rank_at_k': 0.0}], 'mean_recall_at_k': 0.5, 'mean_reciprocal_rank_at_k': 0.5}), ('return zero aggregate metrics for an empty evaluation set', {'k': 5, 'queries': []}, {'queries': [], 'mean_recall_at_k': 0.0, 'mean_reciprocal_rank_at_k': 0.0}), ('reject duplicate document IDs in a ranked result', {'k': 2, 'queries': [{'id': 'q{n}', 'relevant': ['a'], 'ranked': ['a', 'a']}]}, None), ('reject a zero retrieval evaluation cutoff', {'k': 0, 'queries': []}, None)]


def make_case(index):
    description, source, expected = copy.deepcopy(TEMPLATES[index % len(TEMPLATES)])
    def fill(value):
        if isinstance(value, str):
            if re.fullmatch(r"@i[+]\d+", value):
                return index + int(value[3:])
            return value.replace("{n}", str(index))
        if isinstance(value, list):
            return [fill(item) for item in value]
        if isinstance(value, dict):
            return {fill(key): fill(item) for key, item in value.items()}
        return value
    case = {"id": "evaluation-{:04d}".format(index), "description": description, "input": fill(source)}
    case.update({"expected_error": True} if expected is None else {"expected": fill(expected)})
    return case
