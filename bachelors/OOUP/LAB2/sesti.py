import ast
import re

class Sheet:
   def __init__(self, rows, cols):
      self.cells = [[Cell(self) for _ in range(cols)] for _ in range(rows)]
      
   def set(self, ref, content):
      cell = self.cell(ref)
      cell.expression = content
      for ref in self.get_refs(cell):
         ref.add_listener(cell)
      cell.update_value()

   def cell(self, ref):
      row, col = self._parse_ref(ref)
      return self.cells[row][col]

   def get_refs(self, cell):
      refs = re.findall(r'[A-Z]+\d+', cell.expression)
      return [self.cell(ref) for ref in refs]

   def _parse_ref(self, ref):
      col = ord(ref[0]) - ord('A')
      row = int(ref[1:]) - 1
      return row, col

   def print(self):
      for row in self.cells:
         for cell in row:
            print(cell.expression if cell.expression else '-', end='\t')
         print()

class Cell:
   def __init__(self, sheet):
      self.expression = None
      self.value = None
      self.sheet = sheet
      self.listeners = []

   def add_listener(self, listener):
      self.listeners.append(listener)

   def _eval(self, node, variables):
      if isinstance(node, ast.Constant):
         return node.value
      elif isinstance(node, ast.Name):
         return variables[node.id]
      elif isinstance(node, ast.BinOp):
         return self._eval(node.left, variables) + self._eval(node.right, variables)
      else:
         raise Exception('Unsupported type {}'.format(node))

   def eval_expression(self, exp, variables={}):
      node = ast.parse(exp, mode='eval')
      return self._eval(node.body, variables)

   def evaluate(self):
      refs = re.findall(r'[A-Z]+\d+', self.expression)
      variables = {ref: self.sheet.cell(ref).value for ref in refs}
      return self.eval_expression(self.expression, variables)

   def update_value(self, updating=None):
      if updating is None:
         updating = set()
      elif self in updating:
         raise RuntimeError("Circular dependency detected")
   
      updating.add(self)
      try:
         self.value = self.evaluate()
         for listener in self.listeners:
               listener.update_value(updating)
      except Exception as e:
         self.value = None
         raise RuntimeError("Error evaluating expression:", e)
      finally:
         updating.remove(self)
         
def main():
   s = Sheet(5, 5)
   print()
   s.set('A1', '2')
   s.set('A2', '5')
   s.set('A3', 'A1+A2')
   s.print()
   print()

   s.set('A1', '4')
   s.set('A4', 'A1+A3')
   s.print()
   print()

   try:
      s.set('A1', 'A3')
   except RuntimeError as e:
      print("Caught exception:", e)
   s.print()
   print()

if __name__ == "__main__":
   main()