from math import e, pi, sqrt
from numpy import cos, sin
from numpy import arcsin as asin
from numpy import arccos as acos
from numpy import log as ln
import tensorflow as tf
import random
from .OperatorChecker import *
# this is an example of how quantum operator rotations can be mapped to rotations on the bloch sphere
# this code is not fully optimized, but its intended purpose is to demonstrate how one would go about doing these calculations by hand


class RotationMatrixModel(tf.Module): # this class extends the tf module class, and it is used by operator_to_rotation to define a tf model to solve for the 3d rotation matrix corresponding to an operator
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # initialize the x, y, and z angles to random values
        self.x = tf.Variable(random.random(), dtype='float32')
        self.y = tf.Variable(random.random(), dtype='float32')
        self.z = tf.Variable(random.random(), dtype='float32')

    def __call__(self, initial_vector): # function that returns the initial state rotated by the matrix
        matrix = [[tf.math.cos(self.x)*tf.math.cos(self.y),   tf.math.cos(self.x)*tf.math.sin(self.y)*tf.math.sin(self.z) - tf.math.sin(self.x)*tf.math.cos(self.z),   tf.math.cos(self.x)*tf.math.sin(self.y)*tf.math.cos(self.z) + tf.math.sin(self.x)*tf.math.sin(self.z)  ], 
                  [tf.math.sin(self.x)*tf.math.cos(self.y),   tf.math.sin(self.x)*tf.math.sin(self.y)*tf.math.sin(self.z) + tf.math.cos(self.x)*tf.math.cos(self.z),   tf.math.sin(self.x)*tf.math.sin(self.y)*tf.math.cos(self.z) - tf.math.cos(self.x)*tf.math.sin(self.z)  ],
                  [-tf.math.sin(self.y),                      tf.math.cos(self.y)*tf.math.sin(self.z),                                                                 tf.math.cos(self.y)*tf.math.cos(self.z)                                                                ]] # rotation matrix stored as a tf tensor
        return tf.reshape((matrix @ initial_vector), [3, 1]) # return the matrix product of the rotation matrix and the initial state


class RotationConversions():
    def operator_to_updated_state(self, operator, theta_init, phi_init):
        '''
        operator_to_updated_state(operator, theta_init, phi_init)

        Description:
            - this function takes a quantum operator (corresponding to a qbit gate), and the initial qbit state defined by the angles theta and phi
            - theta and phi define the state based on some point on the bloch sphere in spherical coordinates
            - the statevector of the qbit is defined as [cos(theta/2), sin(theta/2) * e^(i*phi)]
            - the function returns the state after being acted on by the gate (in terms of the new theta and phi values)

        Parameters:
            - operator <type 'list'>: linear, hermitian matrix representing the quantum operator
            - theta_init <type 'float'>: initial value for the theta component of the quantum state (must be between 0.0 and pi/2)
            - phi_init <type 'float'>: initial value for the phi component of the quantum state (must be between 0.0 and pi/2)

        Returns:
            - [theta_updated, phi_updated] <type 'list'>: list storing the updated values for theta and phi after being operated on by 'operator'

        Example:
            >>> rc = RotationConversions()
            >>> pauli_z = [[1, 0], [0, -1]] # pauli z gate
            >>> print(rc.operator_to_updated_state(pauli_z, 1, 1)) # operate on the initial state of ['theta': 1, 'phi': 1]
            [-1.0, 1.0]

        '''
        
        # make sure that the operator is unitary, and throw an ArithmeticError if it is not
            
        if (not OperatorChecker.check_unitary(operator)):
            raise ArithmeticError("Passed operator is not unitary")

        i = 1.0j # define the imaginary unit

        a0 = cos(theta_init/2) # generate the initial complex statevector using the initial theta and phi angles
        b0 = e**(i*phi_init) * sin(theta_init/2)

        operator_a = operator[0][0] * a0 + operator[0][1] * b0 # calculate the result of operating on the statevector
        operator_b = operator[1][0] * a0 + operator[1][1] * b0 

        phase = asin((operator_a/abs(operator_a)).imag) # calculate the relative phases of the resulting statevector

        a1 = (operator_a / e**(i*phase)) # adjust by the relative phases
        b1 = (operator_b / e**(i*phase))

        theta1 = (-2 * (acos(a1)).real) # calculate the new theta and phi values
        if (sin(theta1 / 2) == 0): # avoid divide by 0
            phi1 = (-i * ln(b1 / 1E-15))
        else:
            phi1 = (-i * ln(b1 / sin(theta1 / 2)))

        return [theta1.real.round(10), phi1.real.round(10)] # return the updated theta and phi values, rounded to 10 decimal places for readability


    def operator_to_rotation(self, operator, print_optimization_loss=False, epochs=300, num_of_vectors=3):
        '''
        operator_to_rotation(operator, print_optimization_loss=False, epochs=300, num_of_vectors=3)

        Description:
            - this function takes a quantum operator (corresponding to a qbit gate)
            - the function uses tensorflow to find the spacial rotations along the x, y, and z axes of the bloch sphere that corresponds to the operator acting on a qbit state state

        Parameters:
            - operator <type 'list'>: linear, hermitian matrix representing the quantum operator
            - print_optimization_loss=False <type 'bool'>: boolean value that determines if the function will print out the loss of the tf model as it optimizes to find the spacial rotations
            - epochs=300 <type: 'int'>: number of epochs that the tf model will optimize for
            - num_of_vectors=3 <type 'int'>: number of quantum statevectors that the tf model will optimize for (higher means more accurate but slower, lower means less accurate but faster)

        Returns:
            - [RotX, RotY, RotZ] <type 'list'>: list storing the spacial rotations along each axis corresponding to the passed operator

        Example:
            >>> rc = RotationConversions()
            >>> pauli_z = [[1, 0], [0, -1]] # pauli z gate
            >>> print(rc.operator_to_rotation(pauli_z)) # solve for the spacial rotation of the pauli z gate
            [0.0, 0.0, 3.14159]

        '''
        
        # make sure that the operator is unitary, and throw an ArithmeticError if it is not
        
        if (not OperatorChecker.check_unitary(operator)):
            raise ArithmeticError("Passed operator is not unitary")

        def generate_vector_rotations(quantity): # this function is used to generate a given number of random pair of vectors such that one is the result of operating on the other with the operator
            vector_pairs = []
            for i in range(quantity):
                # define an arbitrary initial state for the statevector to be in, defined by the two angles on the bloch sphere (just not along any of the axes on the bloch sphere to avoid division by 0)
                theta0 = random.random() * pi / 2
                phi0 = random.random() * pi / 2
                
                # calculate the new statevector in terms of the angles after applying the operator
                theta1, phi1 = self.operator_to_updated_state(operator, theta0, phi0)

                # get the x, y, and z coords of the original state
                x0 = sin(theta0) * cos(phi0)
                y0 = sin(theta0) * sin(phi0)
                z0 = cos(theta0)

                # get the x, y, and z coords of the updated state
                x1 = sin(theta1) * cos(phi1)
                y1 = sin(theta1) * sin(phi1)
                z1 = cos(theta1)

                vector_pairs.append([[x0, y0, z0], [x1, y1, z1]])
            return vector_pairs # return the list of vector pairs

        # generate the list of vector pairs that will be used to find the 3d spacial rotation that corresponds to this operator
        vector_pairs = generate_vector_rotations(num_of_vectors)
        initials = []
        targets = []
        for i in range(num_of_vectors):
            initials.append(vector_pairs[i][0])
            targets.append(vector_pairs[i][1])

        # use the gradient decent tools in tensorflow to solve for the rotation matrix to map between the two states in 3d space
        model = RotationMatrixModel() # instantiate the model that will be optimized to find the spacial rotations

        def loss(target, predicted): # loss function that finds the square of the difference between the predicted and target vectors (the initial vector)
            return tf.square(target[0, 0] - predicted[0, 0]) + tf.square(target[1, 0] - predicted[1, 0]) + tf.square(target[2, 0] - predicted[2, 0]) # calculate the loss by adding the errors in each dimension

        def train(initials, targets, print_loss, learning_rate): # function to optimize the model using gradient descent, thus solving for the angles that produce the rotated state
            with tf.GradientTape() as t:
                # trainable variables are automatically tracked by GradientTape
                current_loss = tf.reduce_sum([loss(tf.reshape(target, [3, 1]), model(tf.reshape(initial, [3, 1]))) for target, initial in zip(initials, targets)])
            
            if (print_optimization_loss):
                print("Loss: "  + str(current_loss.numpy()))

            # use GradientTape to calculate the gradients with respect to x, y, and z
            dx, dy, dz = t.gradient(current_loss, [model.x, model.y, model.z])

            # subtract the gradient scaled by the learning rate
            model.x.assign_sub(learning_rate * dx)
            model.y.assign_sub(learning_rate * dy)
            model.z.assign_sub(learning_rate * dz)

        # train the model to solve for the angles
        if (print_optimization_loss):
            print("Solving for the rotation matrix...")

        for i in range(epochs): # training loop that iterates epochs times
            train(initials, targets, print_optimization_loss, learning_rate=0.08) # optimise using gradient descent

        # return the solution state stored in the model (Rot_x, Rot_y, Rot_z)
        return [model.z.numpy(), model.y.numpy(), model.x.numpy()]

'''
 # example usage
i = 1.0j
h = 1/sqrt(2)

operator0 = [  [0,   -i],
            [i,    0]  ] # y
operator1 = [  [1,    0],
            [0,   -1]  ] # z
operator2 = [  [0,    1],
            [1,    0]  ] # x
operator3 = [  [h,    h],
            [h,   -h]  ] # hadamard gate
operator = [operator0, operator1, operator2, operator3][1]
rc = RotationConversions()
rotation = [i.round(5) for i in rc.operator_to_rotation(operator, epochs=300, num_of_vectors=6, print_optimization_loss=False)]
print("\nRotation Vector [RotX, RotY, RotZ]:")
print("\t\t" + str(rotation))

print(rc.operator_to_updated_state(operator, 1, 1))

'''
