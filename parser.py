class ASTNode:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

    def __repr__(self):
        visited = set()  # Track visited nodes to avoid infinite recursion
        return self._repr_helper(visited)

    def _repr_helper(self, visited):
        if id(self) in visited:
            return f"{self.type}({self.value})"  # Avoid infinite recursion by skipping
        visited.add(id(self))  # Mark this node as visited

        # If children exist, recursively print them with indentation based on depth
        children_repr = ', '.join([child._repr_helper(visited) for child in self.children]) if self.children else ''
        return f"{self.type}({self.value}): [{children_repr}]"


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current_token(self):
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def eat(self, token_type):
        """Consumes the current token if it matches the expected type."""
        if self.current_token() and self.current_token()[0] == token_type:
            self.position += 1
        else:
            raise SyntaxError(f"Expected {token_type}, found {self.current_token()}")

    def parse_program(self):
        root = ASTNode("Program")
        while self.position < len(self.tokens):
            statement = self.parse_statement()
            if statement:
                root.add_child(statement)  # Ensure statement is added to root
        return root

    def parse_statement(self):
        current = self.current_token()
        if current and current[0] == 'Keyword':
            keyword = current[1]
            if keyword == 'draw':
                print("Parsing draw statement...")  # Debugging print statement
                return self.parse_draw_statement()
            elif keyword == 'grid':
                print("Parsing grid statement...")  # Debugging print statement
                return self.parse_grid_statement()
            elif keyword == 'write':  # Handle 'write' keyword as a separate statement
                print("Parsing write statement...")  # Debugging print statement
                return self.parse_write_statement()  # Parse the write statement
            else:
                raise SyntaxError(f"Unknown statement {keyword}")
        
        # Handle expressions that start with '(' 
        elif current[0] == 'SpecialSymbol' and current[1] == '(':
            print("Parsing expression inside parentheses...")  # Debugging print statement
            return self.parse_expression()  # Parse the expression inside the parentheses
        
        elif current[0] == 'SpecialSymbol' and current[1] == ';':
            # Skip over semicolons as statement terminators
            self.eat('SpecialSymbol')  # eat ';'
            return None  # No statement to parse
        else:
            raise SyntaxError(f"Unexpected token {current}")


    def parse_draw_statement(self):
        print("Inside parse_draw_statement()")  # Debugging print statement
        self.eat('Keyword')  # consume 'draw'
        self.eat('SpecialSymbol')  # consume '('
        expression = self.parse_expression()  # Parse the expression inside 'draw'
        self.eat('SpecialSymbol')  # consume ')'

        # Create the AST node for the DrawStatement and add the expression as its child
        node = ASTNode('DrawStatement')
        node.add_child(expression)

        # Check for a * operator followed by a number
        if self.current_token() and self.current_token()[0] == 'Operator' and self.current_token()[1] == '*':
            self.eat('Operator')  # consume '*'
            if self.current_token() and self.current_token()[0] == 'Number':
                number_node = ASTNode('Number', self.current_token()[1])
                self.eat('Number')  # consume the number

                # Create an Expression node for the '*' operation
                multiply_node = ASTNode('Expression', value='*')
                multiply_node.add_child(node)  # Add draw statement as left operand
                multiply_node.add_child(number_node)  # Add number as right operand
                node = multiply_node  # Update node to be the * expression

        # Check for a + operator following the draw statement or * expression
        if self.current_token() and self.current_token()[0] == 'Operator' and self.current_token()[1] == '+':
            self.eat('Operator')  # consume '+'
            right_expression = self.parse_expression()  # Parse the expression on the right side of '+'

            # Create an Expression node for the '+' operation
            plus_node = ASTNode('Expression', value='+')
            plus_node.add_child(node)  # Left side (draw * number, if present)
            plus_node.add_child(right_expression)  # Right side of '+'
            node = plus_node  # Update node to be the + expression

        return node  # Return the final expression node


    def parse_write_statement(self):
        print("Inside parse_write_statement()")  # Debugging print statement
        self.eat('Keyword')  # consume 'write'
        self.eat('SpecialSymbol')  # consume '('
        expression = self.parse_expression()  # Parse the expression inside 'write'
        self.eat('SpecialSymbol')  # consume ')'

        # Create the AST node for the WriteStatement and add the expression as its child
        node = ASTNode('WriteStatement')
        node.add_child(expression)

        # Check for a * operator followed by a number
        if self.current_token() and self.current_token()[0] == 'Operator' and self.current_token()[1] == '*':
            self.eat('Operator')  # consume '*'
            if self.current_token() and self.current_token()[0] == 'Number':
                number_node = ASTNode('Number', self.current_token()[1])
                self.eat('Number')  # consume the number

                # Create an Expression node for the '*' operation
                multiply_node = ASTNode('Expression', value='*')
                multiply_node.add_child(node)  # Add write statement as left operand
                multiply_node.add_child(number_node)  # Add number as right operand
                node = multiply_node  # Update node to be the * expression

        # Check for a + operator following the write statement or * expression
        if self.current_token() and self.current_token()[0] == 'Operator' and self.current_token()[1] == '+':
            self.eat('Operator')  # consume '+'
            right_expression = self.parse_expression()  # Parse the expression on the right side of '+'

            # Create an Expression node for the '+' operation
            plus_node = ASTNode('Expression', value='+')
            plus_node.add_child(node)  # Left side (write * number, if present)
            plus_node.add_child(right_expression)  # Right side of '+'
            node = plus_node  # Update node to be the + expression

        return node  # Return the final expression node


    def parse_expression(self):
        print("Inside parse_expression()")  # Debugging print statement

        # Parse the left-hand side, which could be a write statement, draw statement, identifier, or number
        current = self.current_token()
        if current[0] == 'Keyword':
            if current[1] == 'write':
                left = self.parse_write_statement()
            elif current[1] == 'draw':
                left = self.parse_draw_statement()
            else:
                raise SyntaxError(f"Unexpected keyword {current[1]}")
        elif current[0] == 'Identifier':
            left = self.parse_image()  # Parse identifier
        elif current[0] == 'Number':
            left = ASTNode('Number', current[1])  # Parse number
            self.eat('Number')
        else:
            raise SyntaxError(f"Unexpected token {current}")

        # Handle operators and right-hand expressions
        while self.current_token() and self.current_token()[0] == 'Operator':
            operator = self.current_token()[1]  # Get the operator (e.g., '+', '*')
            self.eat('Operator')  # Consume the operator token

            # Parse the right-hand side as another primary expression
            current = self.current_token()
            if current[0] == 'Keyword':
                if current[1] == 'write':
                    right = self.parse_write_statement()
                elif current[1] == 'draw':
                    right = self.parse_draw_statement()
                else:
                    raise SyntaxError(f"Unexpected keyword {current[1]}")
            elif current[0] == 'Identifier':
                right = self.parse_image()  # Parse identifier
            elif current[0] == 'Number':
                right = ASTNode('Number', current[1])  # Parse number
                self.eat('Number')
            else:
                raise SyntaxError(f"Unexpected token {current}")

            # Create an expression node for the operator, with left and right as children
            operator_node = ASTNode('Expression', value=operator)
            operator_node.add_child(left)
            operator_node.add_child(right)
        
            # Update `left` to be the operator node for chained operations
            left = operator_node

        print(f"Expression parsed as: {left}")  # Debugging print statement
        return left


    def parse_image(self):
        current = self.current_token()
        if current[0] == 'Identifier':
            identifier = self.current_token()[1]
            self.eat('Identifier')  # Eat the identifier (sun, dog)
            return ASTNode('Identifier', value=identifier)
        else:
            raise SyntaxError(f"Unexpected token in image: {current}")

    def parse_number(self):
        number = self.current_token()[1]
        self.eat('Number')
        return number

    def parse_grid_content(self):
        """Parse grid content which can be a combination of expressions."""
        content_node = ASTNode('GridContent')
        while self.position < len(self.tokens):
            current = self.current_token()
            
            if current and current[0] == 'Keyword':  # Handle 'draw' or 'write' separately
                if current[1] == 'draw':
                    content_node.add_child(self.parse_draw_statement())
                elif current[1] == 'write':
                    content_node.add_child(self.parse_write_statement())
                else:
                    raise SyntaxError(f"Unexpected keyword {current[1]}")
                
                # Check for comma separation and eat if found
                if self.current_token() and self.current_token()[0] == 'SpecialSymbol' and self.current_token()[1] == ',':
                    self.eat('SpecialSymbol')  # Eat ','
                else:
                    break  # Stop if no more commas or invalid tokens
            elif current and current[0] == 'SpecialSymbol' and current[1] == ')':
                break  # Stop if we've encountered the closing parenthesis for the grid
            else:
                break  # Break if any unexpected token is found
    
        return content_node
    
    
    def parse_grid_statement(self):
        print("Inside parse_grid_statement()")  # Debugging print statement
        self.eat('Keyword')  # consume 'grid'
        self.eat('SpecialSymbol')  # consume '('
    
        # Parse x-axis size
        if self.current_token()[0] == 'Number':
            row_size = ASTNode('Number', self.current_token()[1])
            self.eat('Number')
        else:
            raise SyntaxError("Expected a number of rows in grid")

        self.eat('SpecialSymbol')  # consume ','

        # Parse y-axis size
        if self.current_token()[0] == 'Number':
            coloumn_size = ASTNode('Number', self.current_token()[1])
            self.eat('Number')
        else:
            raise SyntaxError("Expected a number of coloumns in grid")

        self.eat('SpecialSymbol')  # consume ','

        # Create the GridStatement node and add x and y size as its first children
        grid_node = ASTNode('GridStatement')
        grid_node.add_child(row_size)
        grid_node.add_child(coloumn_size)

        # Parse grid content (content for each cell of the grid)
        content_node = self.parse_grid_content()  # Reuse parse_grid_content method
        grid_node.add_child(content_node)  # Add content node to grid node

        self.eat('SpecialSymbol')  # consume ')'
        self.eat('SpecialSymbol')  # consume ';'

        print(f"Grid statement AST node: {grid_node}")  # Debugging print statement
        return grid_node
        node = ASTNode('GridStatement', value=(rows, cols))
        node.add_child(grid_content)  # Add the parsed grid content as a child node
        return node
