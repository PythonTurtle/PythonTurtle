class VectorError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.value)
    

class vector(list):
        def __add__(self, other):
            if not(isinstance(other,vector)):
                raise VectorError("right hand side is not a vector")
            return vector(map(lambda x,y: x+y, self, other))

        def __neg__(self):
                return vector(map(lambda x: -x, self))

        def __pos__(self):
                return self

        def __sub__(self, other):
                return vector(map(lambda x,y: x-y, self, other))

        def __mul__(self, other):
            if not(isinstance(other,int) or isinstance(other,float)):
                raise VectorError("right hand side is illegal")
            return vector(map(lambda x: x*other, self))


        def __rmul__(self, other):
                return (self*other)

        def __div__(self, other):
                if not(isinstance(other,int) or isinstance(other,float)):
                    raise VectorError("right hand side is illegal")
                return vector(map(lambda x: x/other, self))

        def __rdiv__(self, other):
                raise VectorError("you sick pervert! you tried to divide something by a vector!")

        def __and__(self,other):
                """
                this is a dot product, done like this: a&b
                must use () around it because of fucked up operator precedence.
                """
                if not(isinstance(other,vector)):
                        raise VectorError("trying to do dot product of vector with non-vector")
                """
                if self.dim()!=other.dim():
                        raise("trying to do dot product of vectors of unequal dimension!")
                """
                d=self.dim()
                s=0.
                for i in range(d):
                        s+=self[i]*other[i]
                return s
                        
        def __rand__(self,other):
                return self&other

        def __or__(self,other):
                """
                cross product, defined only for 3D vectors. goes like this: a|b
                don't try this on non-3d vectors. must use () around it because of fucked up operator precedence.
                """
                a=self
                b=other
                return vector([a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]])
                
        def __ror__(self,other):
                return -(self|other)

        def __abs__(self):
                s=0.
                for x in self:
                        s+=x**2
                return s**(1.0/2)

        def __iadd__(self,other):
                self=self+other
                return self
        
        def __isub__(self,other):
                self=self-other
                return self
        
        def __imul__(self,other):
                self=self*other
                return self

        def __idiv__(self,other):
                self=self/other
                return self

        def __iand__(self,other):
                raise VectorError("please don't do &= with my vectors, it confuses me")

        def __ior__(self,other):
                self=self|other
                return self

        def norm(self):
                """
                gives the vector, normalized
                """
                return self/abs(self)
        def dim(self):
                return len(self)
        
        def copy(self):
                return vector(self)

        def wolfize(self):
                return list(self)
        

        """
        def __deepcopy__(self):
                s=[thing.__deepcopy__() for thing in self]
                return vector[s]
        """                
        
################################################################################################

def zeros(n):
        """
        Returns a zero vector of length n.
        """
        return vector(map(lambda x: 0., range(n)))

def ones(n):
        """
        Returns a vector of length n with all ones.
        """
        return vector(map(lambda x: 1., range(n)))
