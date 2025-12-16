class FibonacchiLst:
    def __init__(self, lst):
        self.lst = lst
        self.fib_numbers = self._get_fib_numbers()
    
    def _get_fib_numbers(self):
        """Возвращает список чисел Фибоначчи из исходного списка"""
        if not self.lst:
            return []
        
        max_val = max(self.lst)
        fib_set = {0, 1}
        a, b = 0, 1
        
        # Генерируем числа Фибоначчи до максимального значения
        while True:
            next_fib = a + b
            if next_fib > max_val:
                break
            fib_set.add(next_fib)
            a, b = b, next_fib
        
        # Фильтруем исходный список
        result = []
        for item in self.lst:
            if item in fib_set:
                result.append(item)
        
        return result
    
    def __iter__(self):
        self.current_index = 0
        return self
    
    def __next__(self):
        if self.current_index < len(self.fib_numbers):
            result = self.fib_numbers[self.current_index]
            self.current_index += 1
            return result
        raise StopIteration
    
    def __getitem__(self, index):
        return self.fib_numbers[index]
