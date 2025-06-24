import sys
import math
from collections import Counter

def main():
   if len(sys.argv) > 4:
      print("Usage: python solution.py <training_data> <testing_data> [OPTIONAL : <depth>]")
      sys.exit(1)
   elif len(sys.argv) < 3:
      print("Usage: python solution.py <training_data> <testing_data> [OPTIONAL : <depth>]")
      sys.exit(1)
   else:
      depth = int(sys.argv[3]) if len(sys.argv) == 4 else None

   train_data = sys.argv[1]
   test_data = sys.argv[2]

   header_train, train_data = load_data(train_data)
   _, test_data = load_data(test_data)

   model = ID3()
   model.fit(header_train, train_data, depth)

   print("[BRANCHES]:")
   model.print_tree()

   predictions = model.predict(test_data)
   print("[PREDICTIONS]:", ' '.join(predictions))

   accuracy = calculate_accuracy(test_data, predictions)
   print("[ACCURACY]: {:.5f}".format(accuracy))

   confusion_matrix = calculate_confusion_matrix(test_data, predictions)
   print("[CONFUSION_MATRIX]:")
   for row in confusion_matrix:
      print(' '.join(map(str, row)))

def calculate_accuracy(test_data, predictions):
   correct_predictions = 0
   for true_value, predicted_value in zip(test_data, predictions):
      if true_value[-1] == predicted_value:
         correct_predictions += 1

   total_test_data = len(test_data)
   return correct_predictions / total_test_data

def calculate_confusion_matrix(test_data, predictions):
   unique_labels = sorted(set(true[-1] for true in test_data))
   confusion_matrix = [[0] * len(unique_labels) for _ in range(len(unique_labels))]
   label_to_index = {}
   for i, label in enumerate(unique_labels):
      label_to_index[label] = i

   for true, pred in zip(test_data, predictions):
      true_label_index = label_to_index[true[-1]]
      pred_label_index = label_to_index[pred]
      confusion_matrix[true_label_index][pred_label_index] += 1

   return confusion_matrix

class ID3():
   def __init__(self):
      self.tree = None

   def fit(self, header, data, depth=None):
      self.header = header
      self.tree = self.build_tree(data, data, header[:-1], header[-1], depth, 0)

   def predict(self, data):
      return [self._classify(instance, self.tree) for instance in data]

   def build_tree(self, all_data, current_data, features, target, max_depth, current_depth):
      if not current_data:
         v = self.argmax(all_data, target)
         return Leaf(v)
      if self.same_value(current_data, target):
         return Leaf(current_data[0][self.header.index(target)])
      if not features or (max_depth is not None and current_depth >= max_depth):
         return Leaf(self.argmax(current_data, target))

      information_gain = [self.calc_information_gain(current_data, feature, target) for feature in features]
      best_feature = features[information_gain.index(max(information_gain))]
      subtrees = {}
      best_feature_index = self.header.index(best_feature)

      for value in sorted(set(row[best_feature_index] for row in current_data)):
         subset = [row for row in current_data if row[best_feature_index] == value]
         new_features = [f for f in features if f != best_feature]
         if not subset:
               subtrees[value] = Leaf(self.argmax(current_data, target))
         else:
               subtrees[value] = self.build_tree(all_data, subset, new_features, target, max_depth, current_depth + 1)

      return Node(best_feature, subtrees, self.argmax(current_data, target))

   def argmax(self, data, target):
      target_index = self.header.index(target)
      values = []
      for row in data:
         values.append(row[target_index])
      counts = Counter(values)
      max_count = max(counts.values())
      candidates = []
      for label, count in counts.items():
         if count == max_count:
               candidates.append(label)
      return min(candidates)

   def same_value(self, data, target):
      target_index = self.header.index(target)
      values = []
      for row in data:
         values.append(row[target_index])

      return len(set(values)) == 1
   
   def calc_information_gain(self, data, feature, target):
      total_entropy = self.entropy([row[self.header.index(target)] for row in data])
      feature_index = self.header.index(feature)
      feature_values = set(row[feature_index] for row in data)

      weighted_entropy = 0
      for value in feature_values:
         subset = []
         for row in data:
            if row[feature_index] == value:
                  subset.append(row)
         subset_target_values = []
         for row in subset:
            subset_target_values.append(row[self.header.index(target)])
         weighted_entropy += (len(subset) / len(data)) * self.entropy(subset_target_values)
      return total_entropy - weighted_entropy

   def entropy(self, labels):
      total = len(labels)
      counts = Counter(labels)
      entropy = 0
      for count in counts.values():
         if count:
               proportion = count / total
               entropy_contribution = proportion * math.log2(proportion)
               entropy -= entropy_contribution
      return entropy
   
   def _classify(self, instance, tree):
      if isinstance(tree, Leaf):
         return tree.label

      feature_index = self.header.index(tree.feature)
      feature_value = instance[feature_index]

      if feature_value in tree.subtrees:
         return self._classify(instance, tree.subtrees[feature_value])
      else:
         return tree.label

   def print_tree(self, tree=None, path=[]):
      if tree is None:
         tree = self.tree

      if isinstance(tree, Leaf):
         print(' '.join(path) + ' ' + tree.label)
         return

      for value, subtree in sorted(tree.subtrees.items()):
         self.print_tree(subtree, path + [f"{len(path)+1}:{tree.feature}={value}"])

class Node:
   def __init__(self, feature, subtrees, label):
      self.feature = feature
      self.subtrees = subtrees
      self.label = label

class Leaf:
   def __init__(self, label):
      self.label = label

def load_data(file):
   data = []
   with open(file, "r") as f:
      first = True
      for line in f:
         if first:
               first = False
               header = line.strip().split(",")
               continue
         data.append(line.strip().split(","))
   return header, data

if __name__ == "__main__":
   main()