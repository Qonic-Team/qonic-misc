from numpy import conj, dot
# tool for evaluating operators

class OperatorChecker():
    def check_hermitian(operator):
        '''
        check_hermitian(operator)

        Description:
            - this function takes a 2 by 2 operator matrix and checks to see if it is hermitian (equal to its transposed conjugate)
            - this is useful because all qbit operators corresponding to quantum logic gates must be hermitian

        Parameters:
            - operator <type 'list'>: matrix representing the quantum operator
            
        Returns:
            - hermitian <type 'bool'>: boolean value storing if the passed matrix is hermitian

        Example:
            >>> oc = qonic_misc.OperatorChecker
            >>> pauli_z = [[1, 0], [0, -1]] # pauli z gate
            >>> print(oc.check_hermitian(pauli_z)) # check to see if the pauli z gate is hermitian
            True

        '''
    
        # check all 4 of the elements of the matrix to test for hermitianarity (hermitiary, hermitianary, i dont know...)
        element00 = (operator[0][0]) == conj(operator[0][0])
        element01 = (operator[0][1]) == conj(operator[1][0])
        element10 = (operator[1][0]) == conj(operator[0][1])
        element11 = (operator[1][1]) == conj(operator[1][1])

        # if all 4 of the above conditions are true, then the operator matrix is hermitian
        return (element00 and element01 and element10 and element11)


    def check_unitary(operator):
        '''
        check_unitary(operator)

        Description:
            - this function takes a 2 by 2 operator matrix and checks to see if it is unitary (produces the identity matrix when multiplied by its transposed conjugate)
            - this is useful because all qbit operators corresponding to quantum logic gates must be unitary

        Parameters:
            - operator <type 'list'>: matrix representing the quantum operator
            
        Returns:
            - unitary <type 'bool'>: boolean value storing if the passed matrix is unitary

        Example:
            >>> oc = qonic_misc.OperatorChecker
            >>> pauli_z = [[1, 0], [0, -1]] # pauli z gate
            >>> print(oc.check_unitary(pauli_z) # check to see if the pauli z gate is unitary
            True

        '''

        # define the transposed conjugate of the passed operator
        trans_conj = [[conj(operator[0][0]), conj(operator[1][0])], [conj(operator[0][1]), conj(operator[1][1])]] 

        # get the product of the two matricies
        product = dot(operator, trans_conj)

        # round to 10 decimal points to avoid small errors causing the function to return false
        for i in range(2):
            for j in range(2):
                product[i][j] = round(product[i][j], 10)

        # check to see if the product is equal to the identity matrix, and return the result
        return product.tolist() == [[1, 0], [0, 1]]
