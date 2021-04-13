[![Build](https://api.travis-ci.com/Qonic-Team/qonic-misc.svg?branch=main)](https://travis-ci.com/github/Qonic-Team/qonic-misc)
[![Known Vulnerabilities](https://snyk.io/test/github/Qonic-Team/qonic-misc/badge.svg?targetFile=source_dir/requirements.txt)](https://snyk.io/test/github/Qonic-Team/qonic-misc?targetFile=source_dir/requirements.txt)

## qonic-misc Python Library:
Python library with miscellaneous tools to be used in conjunction with the qonic framework

**To install:** `pip3 install qonic_misc`

**Includes:**  
  * `qonic_misc.RotationConversions`: 
    * `operator_to_updated_state(operator, theta_init, phi_init)`
    
        **Description:**
        * this function takes a quantum operator (corresponding to a qbit gate), and the initial qbit state defined by the angles theta and phi
        * theta and phi define the state based on some point on the bloch sphere in spherical coordinates
        * the statevector of the qbit is defined as [*cos(theta/2)*, *sin(theta/2) e^(i phi)*]
        * the function returns the state after being acted on by the gate (in terms of the new theta and phi values)

        **Parameters:**
        * `operator <type 'list'>`: linear, hermitian matrix representing the quantum operator
        * `theta_init <type 'float'>`: initial value for the theta component of the quantum state (must be between 0.0 and pi/2)
        * `phi_init <type 'float'>`: initial value for the phi component of the quantum state (must be between 0.0 and pi/2)

        **Returns:**
        * `[theta_updated, phi_updated] <type 'list'>`: list storing the updated values for theta and phi after being operated on by 'operator'

        **Example:**
        
            
            >>> rc = qonic_misc.RotationConversions()
            >>> pauli_z = [[1, 0], [0, -1]] # pauli z gate
            >>> print(rc.operator_to_updated_state(pauli_z, 1, 1)) # operate on the initial state of ['theta': 1, 'phi': 1]
            [-1.0, 1.0]
            
            
            
    * `operator_to_rotation(operator, print_optimization_loss=False, epochs=300, num_of_vectors=3)`
        **Description:**
        * this function takes a quantum operator (corresponding to a qbit gate)
        * the function uses tensorflow to find the spacial rotations along the x, y, and z axes of the bloch sphere that corresponds to the operator acting on a qbit state state

        **Parameters:**
        * `operator <type 'list'>`: linear, hermitian matrix representing the quantum operator
        * `print_optimization_loss=False <type 'bool'>`: boolean value that determines if the function will print out the loss of the tf model as it optimizes to find the spacial rotations
        * `epochs=300 <type: 'int'>`: number of epochs that the tf model will optimize for
        * `num_of_vectors=3 <type 'int'>`: number of quantum statevectors that the tf model will optimize for (higher means more accurate but slower, lower means less accurate but faster)

        **Returns:**
        * `[RotX, RotY, RotZ] <type 'list'>`: list storing the spacial rotations along each axis corresponding to the passed operator

        **Example:**
        
            
            >>> rc = qonic_misc.RotationConversions()
            >>> pauli_z = [[1, 0], [0, -1]] # pauli z gate
            >>> print(rc.operator_to_rotation(pauli_z)) # solve for the spacial rotation of the pauli z gate
            [0.0, 0.0, 3.14159]
            
            
            
  * `qonic_misc.OperatorChecker`: tool for evaluating operators
    * `check_hermitian(operator)`

        **Description:**
        * this function takes a 2 by 2 operator matrix and checks to see if it is hermitian (equal to its transposed conjugate)
        * this is useful because all qbit operators corresponding to quantum logic gates must be hermitian
    
        **Parameters:**
        * `operator <type 'list'>`: matrix representing the quantum operator
            
        **Returns:**
        * `hermitian <type 'bool'>`: boolean value storing if the passed matrix is hermitian
     
        **Example:**
        
            >>> oc = qonic_misc.OperatorChecker
            >>> pauli_z = [[1, 0], [0, -1]] # pauli z gate
            >>> print(oc.check_hermitian(pauli_z)) # check to see if the pauli z gate is hermitian
            True



    * `check_unitary(operator)`
        
        **Description:**
        * this function takes a 2 by 2 operator matrix and checks to see if it is unitary (produces the identity matrix when multiplied by its transposed conjugate)
        * this is useful because all qbit operators corresponding to quantum logic gates must be unitary
        
        **Parameters:**
        * `operator <type 'list'>`: matrix representing the quantum operator
            
        **Returns:**
        * `unitary <type 'bool'>`: boolean value storing if the passed matrix is unitary
        
        **Example:**
        
            >>> oc = qonic_misc.OperatorChecker
            >>> pauli_z = [[1, 0], [0, -1]] # pauli z gate
            >>> print(oc.check_unitary(pauli_z) # check to see if the pauli z gate is unitary
            True
