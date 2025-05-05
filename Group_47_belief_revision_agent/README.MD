# Belief Revision Assignment - 02180 Intro to AI, SP25

A Python implementation of a belief revision agent based on the AGM postulates for contraction and revision.

## Features
- Add beliefs with priorities (low, mid, high)  
- Check logical entailment using resolution theorem proving  
- Perform the belief revision operations (revision, contraction, expansion)  
- Test with AGM postulates to test the algorithm: Success, Inclusion, Vacuity, Consistency and Extensionality

## Requirements
Install dependecies:
```bash
pip install sympy
```


## Usage 
Run the belief revision agent:
```bash
python engine.py
```
### **Available Commands**  
| Option | Action | Input examples |
|--------|--------|---------|
| **1**  | Add a belief (with optional priority) | `p >> q high` <br>`(p \| q) >> r`|
| **2**  | Check if a formula is entailed | `p & q` |
| **3**  | Show current belief base | - |
| **4**  | Clear belief base | - |
| **5**  | Run AGM postulate tests | - |
| **6**  | Quit | - |

### **Supported Operators**
| Symbol | Meaning |
|--------|--------|
| **~** | Negation(¬) |
| **&** | Logical AND (∧) |
| **\|** | Logical OR (∨) |
| **>>** | Implication (→) |
| **<<** | 	Reverse implication (←) |
| **( )** | Parantheses to define precedence |
