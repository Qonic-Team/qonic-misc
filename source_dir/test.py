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
rotation = [i.round(5) for i in rc.operator_to_rotation(operator, epochs=300, num_of_vectors=6, print_optimization_loss=False)]
print("\nRotation Vector [RotX, RotY, RotZ]:")
print("\t\t" + str(rotation))

print(rc.operator_to_updated_state(operator, 1, 1))
