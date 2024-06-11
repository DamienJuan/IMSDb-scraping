import numpy as np

# for word love in western category
queries = ["love"]
expected_relevant_results = {
    "love": {"American Outlaws",
"Bad Day at Black Rock",
"Book of Eli, The",
"Dances with Wolves",
"Django Unchained",
"First Cow",
"Mariachi, El",
"Roughshod",
"Searchers, The",
"Station West",
"Tall in the Saddle",
"Tombstone",
"True Grit",
"Wild Bunch, The",
"Wild Wild West"}
}
search_results = {
    "love": ["American Outlaws",
"Bad Day at Black Rock",
"Book of Eli, The",
"Dances with Wolves",
"Django Unchained",
"First Cow",
"Mariachi, El",
"Roughshod",
"Searchers, The",
"Station West",
"Tall in the Saddle",
"Tombstone",
"True Grit",
"Wild Bunch, The",
"Wild Wild West"],
}

def calculate_precision_recall_f1(expected, retrieved):
    retrieved_set = set(retrieved)
    true_positives = len(expected & retrieved_set)
    precision = true_positives / len(retrieved_set) if retrieved_set else 0
    recall = true_positives / len(expected) if expected else 0
    f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) else 0
    return precision, recall, f1_score

precision_list = []
recall_list = []
f1_list = []

for query in queries:
    expected = expected_relevant_results[query]
    retrieved = search_results[query]
    precision, recall, f1_score = calculate_precision_recall_f1(expected, retrieved)
    precision_list.append(precision)
    recall_list.append(recall)
    f1_list.append(f1_score)

average_precision = np.mean(precision_list)
average_recall = np.mean(recall_list)
average_f1 = np.mean(f1_list)

print(f"Precision: {average_precision:.2f}")
print(f"Recall: {average_recall:.2f}")
print(f"F1 Score: {average_f1:.2f}")
