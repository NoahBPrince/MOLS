import galois

class Square:

    TEN_ONE = [
        [ 1, 8, 9, 0, 2, 4, 6, 3, 5, 7 ] ,
        [ 7, 2, 8, 9, 0, 3, 5, 4, 6, 1 ] ,
        [ 6, 1, 3, 8, 9, 0, 4, 5, 7, 2 ] ,
        [ 5, 7, 2, 4, 8, 9, 0, 6, 1, 3 ] ,
        [ 0, 6, 1, 3, 5, 8, 9, 7, 2, 4 ] ,
        [ 9, 0, 7, 2, 4, 6, 8, 1, 3, 5 ] ,
        [ 8, 9, 0, 1, 3, 5, 7, 2, 4, 6 ] ,
        [ 2, 3, 4, 5, 6, 7, 1, 8, 9, 0 ] ,
        [ 3, 4, 5, 6, 7, 1, 2, 0, 8, 9 ] ,
        [ 4, 5, 6, 7, 1, 2, 3, 9, 0, 8 ] ]

    TEN_TWO = [
        [ 1, 7, 6, 5, 0, 9, 8, 2, 3, 4 ] ,
        [ 8, 2, 1, 7, 6, 0, 9, 3, 4, 5 ] ,
        [ 9, 8, 3, 2, 1, 7, 0, 4, 5, 6 ] ,
        [ 0, 9, 8, 4, 3, 2, 1, 5, 6, 7 ] ,
        [ 2, 0, 9, 8, 5, 4, 3, 6, 7, 1 ] ,
        [ 4, 3, 0, 9, 8, 6, 5, 7, 1, 2 ] ,
        [ 6, 5, 4, 0, 9, 8, 7, 1, 2, 3 ] ,
        [ 3, 4, 5, 6, 7, 1, 2, 8, 0, 9 ] ,
        [ 5, 6, 7, 1, 2, 3, 4, 0, 9, 8 ] ,
        [ 7, 1, 2, 3, 4, 5, 6, 9, 8, 0 ] ]

    def __init__( self , box ):
        if not Square.is_square( box ):
            raise Exception( "The Square class is meant for squares" )
        self.mat = box
        self.w = len( box )

    def __repr__( self ):
        rep = ""
        fill = len( str( self.w ) )
        format_string = "{:" + str( fill ) + "d}"
        for row in self.mat:
            rep += "| "
            for entry in row:
                rep += format_string.format( entry ) + " "
            rep += "|\n"
        return rep

    def __mul__( self , other ):
        # returns the product of self and other as a Square
        if not isinstance( other , Square ):
            raise Exception( "Only Squares can be multiplied with Squares" )
        if self.w != other.w:
            raise Exception( "Only boxes with the same dimensions can be multiplied" )
        to_return = [ [ None for i in range( self.w ) ] for j in range( self.w ) ]
        for row_no in range( self.w ):
            for pre, post in enumerate( self.mat[ row_no ] ):
                to_return[ row_no ][ pre ] = other.mat[ row_no ][ post ]
        return Square( to_return )

    def __eq__( self , sq ):
        # returns a boolean indicating whether self and sq are equal squares
        if not isinstance( sq , Square ):
            raise Exception( "Squares can only be compared to other Squares." )
        if self.w != sq.w :
            return False
        for row in range( w ):
            for col in range( w ):
                if self[ row ][ col ] == sq[ row ][ col ]:
                    return False
        return True

    def size( self ):
        # returns the length/width of self
        return self.w

    def inverse( self ):
        # returns the inverse of a square box as a Square
        if not Square.is_square( self.mat ) or not Square.has_latin_rows( self.mat ) :
            return None
        to_return = [ [ None for i in range( self.w ) ] for j in range( self.w ) ]
        for row_no in range( self.w ):
            for idx, val in enumerate( self.mat[ row_no ] ):
                to_return[ row_no ][ val ] = idx
        return Square( to_return )

    def is_orthogonal( self , box ):
        # returns a boolean indicating whether the Squares self and box are orthogonal
        if self.w != box.w:
            return False
        pairs = []
        for row_no in range( self.w ):
            for col_no in range( self.w ):
                this_pair = ( self.mat[ row_no ][ col_no ] , box.mat[ row_no ][ col_no ] )
                if this_pair in pairs:
                    return False
                pairs.append( this_pair )
        return True

    def is_square( box ):
        # returns a boolean indicating whether box has a square shape
        if not isinstance( box , list ):
            return False
        for row in box:
            if len( row ) != len( box ):
                return False
        return True

    def transpose( box ):
        # returns the transpose of a square box
        to_return = [ [] for row in box.mat ]
        for row in box.mat:
            for i in range( len( box.mat ) ):
                to_return[i].append( row[i] )
        return to_return 

    def has_latin_rows( box ):
        # returns a boolean indicating whether all rows have the same set of symbols, 0 to width-1
        symbols = list( range( len( box ) ) )
        for i in range( len( box ) ):
            if sorted( box[i] ) != symbols:
                return False
        return True 

    def is_latin( box ):
        # returns a boolean indicating whether box is a latin square
        return has_latin_rows( box ) and has_latin_rows( transpose( box ) )

class Family:
    def __init__( self , squares ):
        # squares is a list each entry of which is a Square
        for square in squares:
            if not isinstance( square , Square ):
                raise Exception( "The Family class is meant for squares" )
        self.stack = squares
        self.c = len( squares )

    def __repr__( self ):
        ct = 0 
        rep = "" 
        for square in self.stack:
            ct += 1
            rep += "Square #{}:\n".format( ct )
            rep += str( square ) + "\n"
        return rep

    def __eq__( self , fam ):
        # returns a boolean indicating whether the Families self and fam are equal (up to reordering)
        if not isinstance( fam , Family ):
            raise Exception( "Families can only be compared to other Families." )
        if self.size() != fam.size() :
            return False
        self_in = [ False for _ in range( self.size() ) ]
        fam_in = [ False for _ in range( fam.size() ) ]
        for self_idx in range( self.size() ):
            for fam_idx in range( fam.size() ):
                if self.stack[ self_idx ] == fam.stack[ fam_idx ] :
                    self_in[ self_idx ] = True
                    fam_in[ fam_idx ] = True
        return all( self_in ) and all( fam_in )

    def size( self ):
       # returns the number of Squares in self
        return self.c

    def rprod( self , square ):
        # returns a Family consisting of A*square for each A in self
        return Family( [ sqr * square for sqr in self.stack ] )

    def lprod( self , square ):
        # returns a Family consisting of square*A for each A in self
        return Family( [ square * sqr for sqr in self.stack ] )

    def is_orthogonal( self ):
        # returns a boolean indicating whether self is a mutually orthogonal family
        from_here = []
        for idx in range( self.c - 1 ):
            list_comp = [ self.stack[idx].is_orthogonal( self.stack[ridx] ) for ridx in range( idx + 1 , self.c ) ]
            from_here.append( all( list_comp ) )
        return all( from_here )

    def MOLS( dim ):
        # returns a MOLS family with width dim if dim is a prime power, or None otherwise
        dim = int( dim )
        if dim < 1:
            raise Exception( "The dimension of a MOLS must be a positive integer." )
        primes = Math.prime_factorization( dim )
        if len( set( primes ) ) != 1:
            raise( Exception( "We cannot build a MOLS if dimension is not a prime power." ) )

        p = primes[0]
        gf = galois.GF( dim )
        elts = gf.elements
        stack = [ [ [ 0 for i in range(dim) ] for j in range(dim) ] for k in range(dim) ]
        fam = []
        for slc in range(dim):
            for row in range(dim):
                for col in range(dim):
                    stack[ slc ][ row ][ col ] = elts[ slc ] * elts[ row ] + elts[ col ]
            fam.append( Square( stack[ slc ] ) )

        return Family( fam )

class Permutation:
    def __init__( self , list_form ):
        for entry in range( len( list_form ) ):
            if entry not in list_form:
                raise Exception( "Permutations must be bijections of the integers starting from 0." )
        self.lf = list_form
        self.len = len( list_form )

    def __mul__( self , perm ):
        # returns the product of permuations self and perm
        if not isinstance( perm , Permutation ):
            raise Exception( "Permutations can only be multiplied by other permutations." )
        if not self.len == perm.len :
            raise Exception( "Permutations can only be multiplied when their lengths are equal." )
        prod = []
        for inpt in range( self.len ) :
            prod.append( self.lf[ perm.lf[ inpt ] ] )
        return Permutation( prod )        

    def to_list( self ):
        # returns list form of permutation
        return self.lf
    
    def from_cycles( cycle_list ):
        # returns a list in standard form representing the permutation whose cycle form is cycle_list
        n = sum( [ len(c) for c in cycle_list ] )
        to_return = [ None ] * n
        for c in cycle_list:
            for idx in range( len(c) ):
                if c[idx] in range( n ):
                    to_return[ c[idx] ] = c[ (idx+1) % len(c) ]
        return to_return

class Math:
    def prime_factors( n , lower ):
        # returns a list of all prime factors of n that are at least n, with multiplicity
        lower = max( lower , 2 )
        while lower <= n :
            if ( n % lower ) == 0 :
                factors = Math.prime_factors( n // lower , lower ) 
                factors.append( lower )
                return factors
            lower += 1
        return []

    def prime_factorization( n ):
        if n == 1:
            return []
        if n < 1:
            raise Exception( "Prime factorizations only exist for integers at least 2." )
        return Math.prime_factors( n , 2 )
