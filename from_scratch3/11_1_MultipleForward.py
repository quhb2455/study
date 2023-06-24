import numpy as np

# python 내장 함수로 단위 테스트를 할 때 사용함
import unittest

class Variable:
    def __init__(self, data) -> None:
        if data is not None:
            if not isinstance(data, np.ndarray) :
                raise TypeError(f'{type(data)}는 취급하지 않음ㅋ')
            
        self.data = data
        self.grad = None
        self.creator = None
        
    def set_creator(self, func) :
        self.creator = func

    def backward(self):
        if self.grad is None : 
            self.grad = np.ones_like(self.data)
            
        funcs = [self.creator]
        while funcs :
            f = funcs.pop() 
            x, y = f.input, f.output 
            x.grad = f.backward(y.grad)
            
            if x.creator is not None :
                funcs.append(x.creator)
                
        
class Function:
    # input을 1개 값이 아니라 리스트 값으로 받기
    def __call__(self, inputs):
        # Varialbe list로 들어온 inputs을 분리해서 x.data로 만드는거
        xs = [x.data for x in inputs]
        ys = self.forward(xs)
        
        # 결과값을 다시 Variable list 로 바꿔줌
        outputs = [Variable(as_array(y)) for y in ys]
        for output in outputs:
            output.set_creator(self) 
        
        self.input = input
        self.output = outputs
        return outputs
    
    def forward(self, x):
        raise NotImplementedError
    
    def backward(self, gy):
        raise NotImplementedError
    
class Square(Function):
    def forward(self, x):
        return x ** 2
    
    def backward(self, gy) :
        x = self.input.data
        gx = 2 * x * gy
        return gx
    
class Exp(Function) :
    def forward(self, x) :
        return np.exp(x)   
    
    def backward(self, gy) :
        x = self.input.data
        gx = np.exp(x) * gy
        return gx

class Add(Function) :
    def forward(self, xs):
        x0, x1 = xs
        y = x0 + x1
        return (y,)
    

    
def as_array(x):
    if np.isscalar(x) :
        return np.array(x)
    return x

def square(x) :
    f = Square()
    return f(x)

def numerical_diff(f, x, eps=1e-4):
    x0 = Variable(x.data - eps)
    x1 = Variable(x.data + eps)
    y0 = f(x0)
    y1 = f(x1)
    return (y1.data - y0.data) / (2 * eps)
    

# 단위 테스트 용 클래스
class SquareTest(unittest.TestCase) :
    def test_forward(self) :
        x = Variable(np.array(2.0))
        y = square(x)
        # 예상값을 하드코딩하여 넣어주고 연산과 같은지 확인함
        excepted = np.array(4.0)
        self.assertEqual(y.data, excepted)
    
    def test_backward(self) :
        x = Variable(np.array(3.0))
        y = square(x)
        y.backward()
        # 예상값 하드코딩
        expected = np.array(6.0)
        self.assertEqual(x.grad, expected)
    
    def test_gradient_check(self) :
        x = Variable(np.random.rand(1))
        y = square(x)
        y.backward()
        num_grad = numerical_diff(square, x)
        flg = np.allclose(x.grad, num_grad)
        self.assertTrue(flg)
        
if __name__ == "__main__" :
    inputs = [Variable(np.array(2)), Variable(np.array(3))]
    f = Add()
    ys = f(inputs)
    y = ys[0]
    print(y.data)
    
    