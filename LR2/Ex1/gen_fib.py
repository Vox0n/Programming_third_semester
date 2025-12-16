import functools
import itertools

def fib_elem_gen():
    """Генератор, возвращающий элементы рядов Фибоначчи"""
    a = 0
    b = 1
    
    yield a
    yield b
    
    while True:
        res = a + b
        yield res
        a = b
        b = res

def my_genn():
    """Корутина для генерации списка чисел Фибоначчи"""
    fib_gen = fib_elem_gen()
    
    while True:
        number_of_fib_elem = yield
        result = []
        
        for i in range(number_of_fib_elem):
            result.append(next(fib_gen))
        
        # Возвращаем результат через yield
        # (корутины в Python могут возвращать значение через yield)
        # В данном случае мы используем yield как выражение
        # Чтобы продолжить работу после yield, нам нужно отправить None
        _ = yield result
        
        # Сбрасываем генератор для следующего запроса
        if i == number_of_fib_elem - 1:
            fib_gen = fib_elem_gen()

def fib_coroutine(g):
    @functools.wraps(g)
    def inner(*args, **kwargs):
        gen = g(*args, **kwargs)
        next(gen)  # или gen.send(None) - инициализация корутины
        return gen
    return inner

# Декорируем функцию
my_genn = fib_coroutine(my_genn)
