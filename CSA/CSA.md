  

```ASSEMBLY

-- P-6

DATA SEGMENT

X DB 5

Y DB 6

DATA ENDS

  

CODE SEGMENT

ASSUME CS:CODE, DS:DATA

START:  MOV AX, DATA

        MOV DS, AX

  

        MOV AL, X

        MOV BL, Y

        ADD AL, BL

  

        INT 3H

  

CODE ENDS

END START

```

  

```ASSEMBLY

-- P-7

DATA SEGMENT

X DB 08H

Y DB 08H

DATA ENDS

  

CODE SEGMENT

ASSUME CS:CODE, DS:DATA

  

START:

    MOV AX, DATA

    MOV DS, AX

    MOV AL, X

    MOV BL, Y

    MUL BL

    INT 3H

  

CODE ENDS

END START

```

  

```ASSEMBLY

P-8

  

DATA SEGMENT

HELLO DB "HELLO WORLD", "$"

DATA ENDS

  

CODE SEGMENT

    ASSUME CS:CODE, DS:DATA

START:

    MOV AX, DATA

    MOV DS, AX

    LEA DX, HELLO

    MOV AH, 09H

    INT 21H

  

STOP:

    MOV AX, 4C00H

    INT 21H

  

CODE ENDS

END START

  

```

  

```ASSEMBLY

P-9

  

DATA SEGMENT

    X DB 5H

    Y DB 6H

DATA ENDS

  

CODE SEGMENT

ASSUME CS:CODE, DS:DATA

  

START:

    MOV AX, DATA

    MOV DS, AX

    MOV AL, X

    MOV BL, Y

    ADD AL, BL

    NOT AX

  

    INT 3H

  

CODE ENDS

END START

  

```

```ASSEMBLY
DATA SEGMENT

DATA ENDS

CODE SEGMENT
ASSUME CS:CODE, DS:DATA
START:
        MOV AX, DATA
        MOV DS, AX
        MOV AX, 4F3DH
        MOV BX, 6A0FH
        ADD AX, BX

        INT 3H

CODE ENDS
END START
```

```ASM
DATA SEGMENT
X DW 4F30H
Y DW 6A0FH
DATA ENDS

CODE SEGMENT
ASSUME CS: CODE,DS:DATA
START: MOV AX, DATA
        MOV DS, AX
        MOV AX, X
        MOV BX, Y
        ADD BX, AX

        INT 3H
CODE ENDS
END START

```


```ASM
DATA SEGMENT
MESSAGE DB "XXXXXX", "$"
DATA ENDS

CODE SEGMENT
ASSUME CS:CODE, DS:DATA
START :
        MOV AX, DATA
        MOV DS, AX
        LEA DX, MESSAGE
        MOV AH, 09H
        INT 21H

STOP:
        MOV AX, 4C00H
        INT 21H
CODE ENDS
END START

```

```ASM
DATA SEGMENT

DATA ENDS

CODE SEGMENT
ASSUME CS:CODE, DS:DATA
START :
        MOV AX, DATA
        MOV AH, 30H
        MOV BH, 6AH
        ADD AH, BH
        MOV CH, AH

        INT 3H
CODE ENDS
END START
```


### 1. **Half Adder Truth Table**

A half adder is a combinational circuit that adds two binary digits and produces a sum and carry output.

|A|B|Sum|Carry|
|---|---|---|---|
|0|0|0|0|
|0|1|1|0|
|1|0|1|0|
|1|1|0|1|

- **Sum** = A XOR B
    
- **Carry** = A AND B
    

---

### 2. **Full Adder Truth Table**

A full adder is a combinational circuit that adds three binary digits, including a carry input, and produces a sum and carry output.

|A|B|Cin|Sum|Cout|
|---|---|---|---|---|
|0|0|0|0|0|
|0|0|1|1|0|
|0|1|0|1|0|
|0|1|1|0|1|
|1|0|0|1|0|
|1|0|1|0|1|
|1|1|0|0|1|
|1|1|1|1|1|

- **Sum** = A XOR B XOR Cin
    
- **Cout** = (A AND B) OR (B AND Cin) OR (A AND Cin)
    

---

### 3. **2-Bit Asynchronous (Ripple) Counter Truth Table**

An asynchronous counter is a counter where the flip-flops are not clocked simultaneously. The state transitions occur based on the flip-flop outputs, starting with the least significant bit.

|Clock|Q1|Q0|
|---|---|---|
|0|0|0|
|1|0|1|
|2|1|0|
|3|1|1|

Here, **Q1** and **Q0** represent the outputs of two flip-flops.

---

### 4. **3-Bit Asynchronous (Ripple) Counter Truth Table**

For a 3-bit asynchronous counter:

|Clock|Q2|Q1|Q0|
|---|---|---|---|
|0|0|0|0|
|1|0|0|1|
|2|0|1|0|
|3|0|1|1|
|4|1|0|0|
|5|1|0|1|
|6|1|1|0|
|7|1|1|1|

Again, **Q2**, **Q1**, and **Q0** represent the outputs of three flip-flops.

---

### 5. **2-Bit Synchronous Counter Truth Table**

In a synchronous counter, all flip-flops are triggered simultaneously with the same clock signal.

|Clock|Q1|Q0|
|---|---|---|
|0|0|0|
|1|0|1|
|2|1|0|
|3|1|1|

This is similar to the asynchronous counter but with all flip-flops clocked simultaneously.

---

### 6. **3-Bit Synchronous Counter Truth Table**

For a 3-bit synchronous counter:

|Clock|Q2|Q1|Q0|
|---|---|---|---|
|0|0|0|0|
|1|0|0|1|
|2|0|1|0|
|3|0|1|1|
|4|1|0|0|
|5|1|0|1|
|6|1|1|0|
|7|1|1|1|

Like the 2-bit synchronous counter, all flip-flops transition simultaneously with each clock pulse.

---

### 7. **JK Flip-Flop Truth Table**

The JK flip-flop is a type of flip-flop where both inputs (J and K) can control the output. The state transitions depend on the J and K inputs.

|J|K|Q(t)|Q(t+1)|
|---|---|---|---|
|0|0|0|0|
|0|0|1|1|
|1|0|0|1|
|1|0|1|1|
|0|1|0|0|
|0|1|1|0|
|1|1|0|1|
|1|1|1|0|

- **When J = 1 and K = 0**, the output is set.
    
- **When J = 0 and K = 1**, the output is reset.
    
- **When J = 1 and K = 1**, the output toggles.
    

---

### 8. **JK Master-Slave Flip-Flop Truth Table**

The master-slave JK flip-flop is a combination of two JK flip-flops, where one is used as a master and the other as a slave. It prevents race conditions.

|J|K|Clock|Q (Master)|Q (Slave)|Q(t+1)|
|---|---|---|---|---|---|
|0|0|0|0|0|0|
|0|0|1|0|0|0|
|1|0|0|0|0|0|
|1|0|1|1|1|1|
|0|1|0|0|0|0|
|0|1|1|0|0|0|
|1|1|0|0|0|0|
|1|1|1|1|1|0|

- The flip-flop updates the slave output only on the clock's positive edge, making the JK master-slave flip-flop edge-triggered.
    

---

