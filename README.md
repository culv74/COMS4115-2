### **Authors**
- Gabrielle Holley: `gf2501`
- William Culver: `wrc2120`

### **Context-Free Grammar (CFG)**

#### **Non-Terminals:**
- `Program`: The entry point of the program, consisting of multiple statements.
- `Statement`: Represents a single line of code in the program.
- `Expression`: A combination of images, words, and operations.
- `Image`: Represents either a pre-defined image (`draw`) or text written in ASCII (`write`).
- `Grid`: Represents a grid layout for images and words.
- `Identifier`: Represents predefined image names or identifiers.
- `Number`: Represents numbers used in repeat operations.

#### **Terminals:**
- **Keywords**: `draw`, `write`, `grid`
- **Operators**: `+`, `/`, `*`
- **Special Symbols**: `(`, `)`, `,`, `;`
- **Identifiers**: Words like `dog`, `cat`, `tree`, `sun`, etc.
- **Numbers**: Digits like `1`, `2`, `3`, etc.

#### **Production Rules:**

```
Program         -> Statement*
Statement       -> DrawStatement | WriteStatement | GridStatement | AssignmentStatement
DrawStatement   -> 'draw' '(' Expression ')'
WriteStatement  -> 'write' '(' Expression ')'
GridStatement   -> 'grid' '(' Number ',' Number ',' GridContent ')'
GridContent     -> (Expression (',' Expression)*) | (GridStatement (',' GridStatement)*)
Expression      -> Image | Expression '+' Image | Expression '/' Image | Number '*' Image
Image           -> 'draw' '(' Identifier ')'
                | 'write' '(' Identifier ')'
                | Identifier
Identifier      -> 'dog' | 'cat' | 'tree' | 'sun' | 'house' | 'bird'
Number          -> [0-9]+
```

---

### **Explanation of the Grammar**:

- **Program**: A program consists of one or more statements (`Statement*`).
- **Statement**: A statement can be a `DrawStatement`, `WriteStatement`, `GridStatement`, or an `AssignmentStatement`. We can later expand this to include more functionality if needed.
- **DrawStatement**: A `draw` statement takes an expression inside parentheses, which can be an image.
- **WriteStatement**: A `write` statement is similar to `draw`, except it creates text-based ASCII art.
- **GridStatement**: A `grid` statement consists of a grid size (rows, columns) followed by `GridContent`, which can be a combination of images or other grid statements. This allows for nested grid layouts.
- **Expression**: An expression can be a single image, or a combination of images using the operators `+`, `/`, or `*`.
  - `+` combines images linearly (side by side).
  - `/` combines images vertically (stacked).
  - `*` duplicates an image a specified number of times.
- **Image**: An image is either a predefined ASCII image generated by `draw` or `write`, or a reference to an identifier (e.g., `dog`, `cat`).
- **Identifier**: Identifiers are predefined image names such as `dog`, `cat`, `sun`, etc.
- **Number**: Represents numerical values, used for repeat operations (e.g., `*` operator).

---

### **Example Input and Corresponding Derivation**:

#### Example 1: `draw(sun + dog);`
```
Statement -> DrawStatement
DrawStatement -> 'draw' '(' Expression ')'
Expression -> Expression '+' Image
Expression -> 'draw' '(' Identifier ')'
Image -> 'draw' '(' Identifier ')'
Identifier -> 'sun'
+ 
Image -> 'draw' '(' Identifier ')'
Identifier -> 'dog'
```

This would generate an image where the ASCII art of the sun and dog are placed side by side.

#### Example 2: `grid(2,2, draw(sun), draw(cat), write(dog), write(tree));`
```
Statement -> GridStatement
GridStatement -> 'grid' '(' Number ',' Number ',' GridContent ')'
Number -> 2
GridContent -> Expression ',' Expression ',' Expression ',' Expression
Expression -> 'draw' '(' Identifier ')'
Identifier -> 'sun'
,
Expression -> 'draw' '(' Identifier ')'
Identifier -> 'cat'
,
Expression -> 'write' '(' Identifier ')'
Identifier -> 'dog'
,
Expression -> 'write' '(' Identifier ')'
Identifier -> 'tree'
```

This would generate a 2x2 grid with the specified images (`sun`, `cat`, `dog`, and `tree`).

#### Example 3: `(3 * draw(dog)) / write(I like dogs);`
```
Statement -> Expression
Expression -> Expression '/' Image
Expression -> Number '*' Image
Number -> 3
Image -> 'draw' '(' Identifier ')'
Identifier -> 'dog'
/
Image -> 'write' '(' Identifier ')'
Identifier -> 'I like dogs'
```

This would generate three dogs stacked vertically, followed by the text "I like dogs" in ASCII.

