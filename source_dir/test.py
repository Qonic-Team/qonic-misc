# test file 
from qonic_misc import *

i = 1.0j
h = 1/sqrt(2)

operator0 = [  [0,   -i],
            [i,    0]  ] # y
operator1 = [  [1,    0],
            [0,   -1]  ] # z
operator2 = [  [0,    1],
            [1,    0]  ] # x
operator3 = [  [h,    h],
            [h,   -h]  ] # hadamard
operator = [operator0, operator1, operator2, operator3][1]
rc = RotationConversions()

# make sure that operation_to_rotation runs without error
rotation = [i.round(5) for i in rc.operator_to_rotation(operator, epochs=200, num_of_vectors=4, print_optimization_loss=False)]
print("\nRotation Vector [RotX, RotY, RotZ]:")
print("\t\t" + str(rotation))

# make sure that operator_to_updated_state runs without error
print(rc.operator_to_updated_state(operator, 1, 1))

# make sure that the above functions properly raise ArithmeticError when the operators are not of the correct form
try:
            operator = [[1.23, 4.56], [7.89, 0.12]] # invalid operator
            print(rc.operator_to_updated_state(operator, 1, 1))
except ArithmeticError:
            print("Caught exception - Success!")
