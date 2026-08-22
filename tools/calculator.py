def calculate(expression):
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return result
    except Exception:
        return "Invalid calculation"


if __name__ == "__main__":
    print(calculate("125 * 48"))