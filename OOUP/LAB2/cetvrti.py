import numpy as np
import math
   
class SequentialStrategy:
   def generate_numbers(self, start, end, step):
      return list(range(start, end, step))

class RandomStrategy:
   def generate_numbers(self, mean, std_dev, size):
      return np.random.normal(mean, std_dev, size).astype(int).tolist()

class FibonacciStrategy:
   def generate_numbers(self, size):
      fib_sequence = [1, 1]
      while len(fib_sequence) < size:
         fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
      return fib_sequence[:size]

class DistributionTester:
   def __init__(self, generator_strategy):
      self.generator_strategy = generator_strategy

   def generate_numbers(self, *args, **kwargs):
      return self.generator_strategy.generate_numbers(*args, **kwargs)

   def percentile_by_rank(self, numbers, p):
      sorted_numbers = sorted(numbers)
      N = len(sorted_numbers)
      position = round(p * N / 100 + 0.5)
      if position < 1:
         return sorted_numbers[0]
      elif position > N:
         return sorted_numbers[-1]
      else:
         return sorted_numbers[int(position) - 1]

   def percentile_by_interpolation(self, numbers, p):
      sorted_numbers = sorted(numbers)
      N = len(sorted_numbers)
      position = (p * N / 100) - 0.5
      if position <= 1:
         return sorted_numbers[0]
      elif position >= N:
         return sorted_numbers[-1]
      else:
         lower_index = max(0, math.floor(position))
         upper_index = min(N-1, math.ceil(position))
         lower_value = sorted_numbers[lower_index]
         upper_value = sorted_numbers[upper_index]
         return lower_value + (position - lower_index) * (upper_value - lower_value)

def main():
   sequential_tester = DistributionTester(SequentialStrategy())
   random_tester = DistributionTester(RandomStrategy())
   fibonacci_tester = DistributionTester(FibonacciStrategy())

   print("Test case:")
   numbers = [1, 10, 50]
   print("Generated numbers:", numbers)
   for percentile in range(10, 100, 10):
      print(f"{percentile}th percentile rank:", sequential_tester.percentile_by_rank(numbers, percentile))
      print(f"{percentile}th percentile interpolation:", sequential_tester.percentile_by_interpolation(numbers, percentile)) 

   numbers = sequential_tester.generate_numbers(10, 50, 10)
   print("\nSequential Strategy:", numbers)
   for percentile in range(10, 100, 10):
      print(f"{percentile}th percentile rank:", sequential_tester.percentile_by_rank(numbers, percentile))
      print(f"{percentile}th percentile interpolation:", sequential_tester.percentile_by_interpolation(numbers, percentile)) 

   print("\nRandom Strategy:")
   numbers = random_tester.generate_numbers(50, 10, 100)
   print("Generated numbers:", numbers)
   for percentile in range(10, 100, 10):
      print(f"{percentile}th percentile rank:", random_tester.percentile_by_rank(numbers, percentile))
      print(f"{percentile}th percentile interpolation:", random_tester.percentile_by_interpolation(numbers, percentile))
      
   print("\nFibonacci Strategy:")
   numbers = fibonacci_tester.generate_numbers(10)
   print("Generated numbers:", numbers)
   for percentile in range(10, 100, 10):
      print(f"{percentile}th percentile rank:", fibonacci_tester.percentile_by_rank(numbers, percentile))
      print(f"{percentile}th percentile interpolation:", fibonacci_tester.percentile_by_interpolation(numbers, percentile))

if __name__ == "__main__":
   main()