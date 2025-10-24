from datetime import datetime


def export_to_txt(variable, filename=f"results_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt"):
    """
    Exports any Python variable to a plain text file.

    Args:
        variable: The Python object to save (e.g. dict, list, str, etc.)
        filename: The name of the output text file (default: 'output_<current time>.txt')
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(str(variable))
        print(f"Variable successfully written to '{filename}'")
    except Exception as e:
        print(f"Error writing to file: {e}")



data = 'kjfhgkhskhdhkgskhsgd'
export_to_txt(data)