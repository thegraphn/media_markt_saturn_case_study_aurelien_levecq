from random import shuffle
from utils import create_text_labels
from utils import write_data_set_to_file

labels, texts = create_text_labels("../../data/TV & Audio products Data Set - labeled data.csv", False)

labels_texts = list(zip(labels, texts))
shuffle(labels_texts)
labels, texts = zip(*labels_texts)

begin_train = 0
end_train = round(len(texts) * 0.9)
begin_test = end_train + 1
end_test = len(texts)

training_data_texts = texts[begin_train:end_train]
training_data_labels = labels[begin_train:end_train]
test_data_texts = texts[begin_test:end_test]
test_data_labels = labels[begin_test:end_test]

write_data_set_to_file("../../data/training_data/train_multi_class_multi_label.csv", training_data_texts,
                       training_data_labels,False)
write_data_set_to_file("../../data/training_data/test_multi_class_multi_label.csv", test_data_texts,
                       test_data_labels,False)
