import numpy as np

class Matrix(np.ndarray):
    def __new__(cls, input_array):
        obj = np.asarray(input_array).view(cls)
        return obj

    def __init__(self, input_array):
        super(Matrix, self).__init__()
        try:
            x,y = self.shape
        except ValueError:
            error = "This is not a valid matrix : %s" % self
            raise ValueError(error)

    def __array_finalize__(self, obj): pass

    def mulbyscalar(self, x):
        #for a in np.nditer(self,  op_flags=['readwrite']):
            #a[...] = a * x
        x,y = self.shape
        for i in range(x):
            for j in range (y):
                self[i][j] =self[i][j] * x
        return self

    def trace(self):
        self.__checksquarematrix()
        it = np.nditer(self, flags=['multi_index'])
        sum = 0
        while not it.finished:
            if it.multi_index[0] == it.multi_index[1]:
               sum += it[0]
            it.iternext()
        return sum

    def transpose(self):
        y, x = self.shape
        newArray = [[0 for i in range(y)] for i in range(x)]
        it = np.nditer(self, flags=['multi_index'])
        while not it.finished:
            i = it.multi_index[0]
            j = it.multi_index[1]
            newArray[j][i] = it[0]
            it.iternext()
        return Matrix(newArray)

    def mulbymatrix(self, matrix):
        y, x = self.shape
        t, z = matrix.shape
        if not x == t:
            error = "This matrices are not suitable for multiplication: first=%dx%d second=%dx%d" % (x,y,t,z)
            raise ValueError(error)
        C = [[0 for i in range(z)] for i in range(y)]

        for i in range(len(C)):
            for j in range(len(C[0])):
                for k in range(len(C[0])):
                    C[i][j] += self[i][k] * matrix[k][j]
        return Matrix(C)

    def determinant(self):
        self.__checksquarematrix()
        det = 0
        y, x = self.shape
        if x == 2:
            return self[0][0] * self[1][1] - self[0][1] * self[1][0]
        else:
            for i in range(len(self[0])):
                sign = (-1)**i
                arr = self.__decrease_dimension(0, i)
                det += sign * self[0][i] * arr.determinant()
        return det

    def __decrease_dimension(self, row, col):
        y, x = self.shape
        if col >= y:
            error ="there is no %d. column in this matrix :\n%s" % (col, self)
            raise ValueError(error)

        C = [[0 for i in range(y-1)] for i in range(x-1)]
        it = np.nditer(self, flags=['multi_index'])
        i = 0
        j = 0
        while not it.finished:
            k = it.multi_index[0]
            l = it.multi_index[1]
            if k != row and l != col:
                C[i][j] = int(it[0])
                j += 1
                if j == y - 1:
                    j = 0
                    i += 1
            it.iternext()
        return Matrix(C)

    def __matrixofminors(self):
        y, x = self.shape
        M = [[0 for i in range(x)]for i in range(y)]
        for i in range(x):
            for j in range(y):
                minor = self.__decrease_dimension(i, j)
                det = minor.determinant()
                M[i][j] = det
        return Matrix(M)

    def __matrixofcofactors(self):
        y, x = self.shape
        C = [[0 for i in range(x)]for i in range(y)]
        for i in range(x):
            for j in range(y):

                if (i+j) % 2 == 0:
                    sign = 1
                else:
                    sign = -1
                C[i][j] = sign * self[i][j]
        return Matrix(C)

    def inverse(self):
        return self.__checksquarematrix().__matrixofminors().__matrixofcofactors().transpose().astype(np.float64).mulbyscalar(1/B.determinant())

    def __checksquarematrix(self):
        y, x = self.shape
        if not x == y:
            error ="this is not a square matrix:\n%s" % self
            raise ValueError(error)
        return self

list1 = [[1, 2, 3],[4, 5, 6]]
list2 = [[1, 2, 3],[4, 5, 6], [7,8,9]]
list3 = [[1, 5, 2],[8, 6, 4], [3,2,1]]
list4 = [[2, 3, 8, 7],[1, 2, 6, 9], [0,3,5,2],[7, 4,6 ,5]]
list5 = [[3, 0, 2],[2, 0, -2], [0, 1, 1]]
_list = [[1, 2],[3, 4]]
A = Matrix(list2)
B = Matrix(list5)
C = Matrix(list1)
#print(A)
print(B.mulbyscalar(2))
print(B.trace())
print(A.transpose())
print(A.determinant())
#print(B.decrease_dimension(4))
#print( B.matrixofminors())
print(C.inverse())


