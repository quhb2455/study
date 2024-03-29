import numpy as np

class Variable :
    def __init__(self, data) :
        self.data = data
        self.grad = None

class Function :
    def __call__(self, input) :
        x = input.data
        y = self.forward(x)
        output = Variable(y)
        self.input = input # 입력 값 보존
        return output
    
    def forward(self, x):
        raise NotImplementedError
    
    def backward(self, gy):
        raise NotImplementedError

class Square(Function):
    def forward(self, x):
        return x ** 2
    
    def backward(self, gy):
        x = self.input.data
        gx = 2 * x * gy
        return gx
    
class Exp(Function) :
    def forward(self, x):
        return np.exp(x)

    def backward(self, gy):
        x = self.input.data
        gx = np.exp(x) *gy
        return gx
    
if __name__ == "__main__" :
    
    A = Square()
    B = Exp()
    C = Square()
    
    # 순전파
    x = Variable(np.array(0.5))
    a = A(x)
    b = B(a)
    y = C(b)
    
    # 역전파
    # 진행 한 연산을 찾아서 한번씩 backward를 호출해야하는 단점이 있음.
    y.grad = np.array(1.0)
    b.grad = C.backward(y.grad)
    a.grad = B.backward(b.grad)
    x.grad = A.backward(a.grad)
    print(x.grad)