def arithmetic_arranger(problems, include_result=False):
    #  If there are too many problems supplied (>5) to the function we have an error
    if len(problems) > 5:
        return print("Error: Too many problems")

    # Admissible perators
    operators = ["+", "-"]
    # List for each line to print
    line1 = []
    line2 = []
    line3 = []
    line4 = []

    for value in problems:
        operation = value.split(" ")

        # Error for non admissible operators
        if operation[1] not in operators:
            return(print("Error: Operator must be '+' or '-'."))

        # Assign operand values
        operand_1 = operation[0]
        operand_2 = operation[2]

        # Operands must only contains digits. Otherwise operation non admited
        if operand_1.isdigit() == False or operand_2.isdigit() == False:
            return (print("Error: Numbers must only contain digits"))

        # Max of four digits for each operand
        if len(operand_1) > 4 or len(operand_2) > 4:
            return print("Error: Numbers cannot be more than four digits.")

        # Max spaces to fill in the final print. We will find the longest operand and we add
        # the operator's space and the space btw the operator and the second element
        max_spaces_to_fill = max(len(x) for x in operation)
        dash = "-"
        space = " "

        # Append each first operand and we add 4 spaces btw each operation
        line1.append(operand_1.rjust(max_spaces_to_fill + 2) + space * 4)
        # Append the operator, space and second operand
        line2.append(operation[1] + space + operand_2.rjust(max_spaces_to_fill) + space * 4)
        # Append dash line
        line3.append(dash * (max_spaces_to_fill + 2) + space * 4)
        # Append the result line in case argument include_result = True
        result = (str(eval(value)))
        line4.append(result.rjust(max_spaces_to_fill + 2) + space * 4)

    # Transform each list in string
    line1 = ''.join(map(str, line1))
    line2 = ''.join(map(str, line2))
    line3 = ''.join(map(str, line3))
    line4 = ''.join(map(str, line4))
    # If second argument true, include results
    if include_result == True:
        arranged_problems = line1 + "\n" + line2 + "\n" + line3 + "\n" + line4
    # If second argument false, only print operation
    if include_result == False:
        arranged_problems = line1 + "\n" + line2 + "\n" + line3
    return arranged_problems


print(arithmetic_arranger(["32 + 8", "1 - 3801", "9999 + 9999", "523 - 49"], True))
