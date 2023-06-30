"""
COMP.CS.100 Ohjelmointi 1 / Programming 1
Student Id: 151057054
Name:       Dong Le
Email:      dong.le@tuni.fi

Project Warehouse Inventory: implement a program which can be used to manage
product in warehouse 
The program reads data from a file and imports those data to a dictionary.
There are few actions that user can interact with product in the program:
display all product's info, display specific product, 
change the stock of product, delete a product, inform user about low stock,
combine two product together, and set sale price for categories.
"""

# +--------------------------------------------------------------+
# | This template file requires at minimum Python version 3.8 to |
# | work correctly. If your Python version is older, you really  |
# | should get yourself a newer version.                         |
# +--------------------------------------------------------------+


LOW_STOCK_LIMIT = 30


class Product:
    """
    This class represent a product i.e. an item available for sale.
    """

    def __init__(self, code, name, category, price, stock):
        self.__code = code
        self.__name = name
        self.__category = category
        self.__price = price
        self.__stock = stock
        # is_sale is true if the product is on sale off
        # is_sale is false means the product is on original price
        self.__is_sale = False
        # original price store the data of price
        self.__original_price = 0.0


    def __str__(self):
        """
        YOU SHOULD NOT MODIFY THIS METHOD or it will mess up
        the automated tests.
        """

        lines = [
            f"Code:     {self.__code}",
            f"Name:     {self.__name}",
            f"Category: {self.__category}",
            f"Price:    {self.__price:.2f}€",
            f"Stock:    {self.__stock} units",
        ]

        longest_line = len(max(lines, key=len))

        for i in range(len(lines)):
            lines[i] = f"| {lines[i]:{longest_line}} |"

        solid_line = "+" + "-" * (longest_line + 2) + "+"
        lines.insert(0, solid_line)
        lines.append(solid_line)

        return "\n".join(lines)

    def __eq__(self, other):
        """
        YOU SHOULD NOT MODIFY THIS METHOD or it will mess up
        the automated tests since the read_database function will
        stop working correctly.
        """

        return self.__code == other.__code and \
               self.__name == other.__name and \
               self.__category == other.__category and \
               self.__price == other.__price

    def modify_stock_size(self, amount):
        """
        YOU SHOULD NOT MODIFY THIS METHOD since read_database
        relies on its behavior and might stop working as a result.

        Allows the <amount> of items in stock to be modified.
        This is a very simple method: it does not check the
        value of <amount> which could possibly lead to
        a negative amount of items in stock. Caveat emptor.

        :param amount: int, how much to change the amount in stock.
                       Both positive and negative values are accepted:
                       positive value increases the stock and vice versa.
        """

        self.__stock += amount

    def get_category(self):
        """
        Return category of the product
        """
        return self.__category
    
    def get_price(self):
        """
        Return price of the product
        """
        return self.__price

    def get_stock(self):
        """
        Return how many the product left in inventory
        """
        return self.__stock
    
    def set_new_price(self, percentage):
        """
        set a new price for the product
        :param percentage: float, how many percentage the product sale off
        """

        # if the product is not sale off, then save
        # the price to the original price
        if self.__is_sale == False:
            self.__original_price = self.__price

        # calculate the new price
        new_price = self.__original_price*(100-percentage)/100
        if percentage != 0.0:
            # the percentage > 0.0, the product is on sale off
            # new price is update and is_sale tag is on
            self.__is_sale = True
            self.__price = new_price
        else:
            # the percentage is 0.0, the product is set back to 
            # original price, and the _is_sale tag is off
            self.__is_sale = False
            self.__price = self.__original_price



def _read_lines_until(fd, last_line):
    """
    YOU SHOULD NOT MODIFY THIS FUNCTION since read_database
    relies on its behavior and might stop working as a result.

    Reads lines from <fd> until the <last_line> is found.
    Returns a list of all the lines before the <last_line>
    which is not included in the list. Return None if
    file ends bofore <last_line> is found.
    Skips empty lines and comments (i.e. characeter '#'
    and everything after it on a line).

    You don't need to understand this function works as it is
    only used as a helper function for the read_database function.

    :param fd: file, file descriptor the input is read from.
    :param last_line: str, reads lines until <last_line> is found.
    :return: list[str] | None
    """

    lines = []

    while True:
        line = fd.readline()

        if line == "":
            return None

        hashtag_position = line.find("#")
        if hashtag_position != -1:
            line = line[:hashtag_position]

        line = line.strip()

        if line == "":
            continue

        elif line == last_line:
            return lines

        else:
            lines.append(line)


def read_database(filename):
    """
    YOU SHOULD NOT MODIFY THIS FUNCTION as it is ready.

    This function reads an input file which must be in the format
    explained in the assignment. Returns a dict containing
    the product code as the key and the corresponding Product
    object as the payload. If an error happens, the return value will be None.

    You don't necessarily need to understand how this function
    works as long as you understand what the return value is.
    You can probably learn something new though, if you examine the
    implementation.

    :param filename: str, name of the file to be read.
    :return: dict[int, Product] | None
    """

    data = {}

    try:
        with open(filename, mode="r", encoding="utf-8") as fd:

            while True:
                lines = _read_lines_until(fd, "BEGIN PRODUCT")
                if lines is None:
                    return data

                lines = _read_lines_until(fd, "END PRODUCT")
                if lines is None:
                    print(f"Error: premature end of file while reading '{filename}'.")
                    return None

                # print(f"TEST: {lines=}")

                collected_product_info = {}

                for line in lines:
                    keyword, value = line.split(maxsplit=1)  # ValueError possible

                    # print(f"TEST: {keyword=} {value=}")

                    if keyword in ("CODE", "STOCK"):
                        value = int(value)  # ValueError possible

                    elif keyword in ("NAME", "CATEGORY"):
                        pass  # No conversion is required for string values.

                    elif keyword == "PRICE":
                        value = float(value)  # ValueError possible

                    else:
                        print(f"Error: an unknown data identifier '{keyword}'.")
                        return None

                    collected_product_info[keyword] = value

                if len(collected_product_info) < 5:
                    print(f"Error: a product block is missing one or more data lines.")
                    return None

                product_code = collected_product_info["CODE"]
                product_name = collected_product_info["NAME"]
                product_category = collected_product_info["CATEGORY"]
                product_price = collected_product_info["PRICE"]
                product_stock = collected_product_info["STOCK"]

                product = Product(code=product_code,
                                  name=product_name,
                                  category=product_category,
                                  price=product_price,
                                  stock=product_stock)

                # print(product)

                if product_code in data:
                    if product == data[product_code]:
                        data[product_code].modify_stock_size(product_stock)

                    else:
                        print(f"Error: product code '{product_code}' conflicting data.")
                        return None

                else:
                    data[product_code] = product

    except OSError:
        print(f"Error: opening the file '{filename}' failed.")
        return None

    except ValueError:
        print(f"Error: something wrong on line '{line}'.")
        return None


def example_function_for_example_purposes(warehouse, parameters):
    """
    This function is an example of how to deal with the extra
    text user entered on the command line after the actual
    command word.

    :param warehouse: dict[int, Product], dict of all known products.
    :param parameters: str, all the text that the user entered after the command word.
    """

    try:
        # Let's try splitting the <parameters> string into two parts.
        # Raises ValueError if there are more or less than exactly two
        # values (in this case there should be one int and one float) in
        # the <parameters> string.
        code, number = parameters.split()

        # First parameter was supposed to be a products code i.e. an integer
        # and the second should be a float. If either of these assumptions fail
        # ValueError will be raised.
        code = int(code)
        number = float(number)

    except ValueError:
        print(f"Error: bad parameters '{parameters}' for example command.")
        return

    # <code> should be an existing product code in the <warehouse>.
    if code not in warehouse:
        print(f"Error: unknown product code '{code}'.")
        return

    # All the errors were checked above, so everything should be
    # smooth sailing from this point onward. Of course, the other
    # commands might require more or less error/sanity checks, this
    # is just a simple example.

    print("Seems like everything is good.")
    print(f"Parameters are: {code=} and {number=}.")

def print_command(data):
    """
    This function is to print out all products in the inventory

    :param data: dict[int, Product], dictionary of all known products.
    """
    for product_code in sorted(data):
        print(data[product_code])

def print_code_command(data, code):
    """
    This function is to print a specific product in the inventory

    :param data: dict[int, Product], dictionary of all known products.
    :param code: int, product's code.
    """
    try:
        # parameter was supposed to be a products code i.e. an integer
        # If either of these assumptions fail
        # ValueError will be raised.
        code = int(code)

    except ValueError:
        print(f"Error: product '{code}' can not be printed as it does not exist.")
        return

    # <code> should be an existing product code in the <warehouse>.
    if code not in data:
        print(f"Error: product '{code}' can not be printed as it does not exist.")
        return
    print(data[int(code)])

def change_amount_command(data, parameters):
    """
    This function is to change amount of stock of the product in the inventory

    :param data: dict[int, Product], dict of all known products.
    :param parameters: str, all the text that the user entered after the command word.
    """

    try:
        # Let's try splitting the <parameters> string into two parts.
        # Raises ValueError if there are more or less than exactly two
        # values (in this case there should be two int) in
        # the <parameters> string.
        code, number = parameters.split()

        # First parameter was supposed to be a products code i.e. an integer
        # and the second should be a float. If either of these assumptions fail
        # ValueError will be raised.
        code = int(code)
        number = int(number)

    except ValueError:
        print(f"Error: bad parameters '{parameters}' for change command.")
        return

    # <code> should be an existing product code in the <warehouse>.
    if code not in data:
        print(f"Error: stock for '{code}' can not be changed as it does not exist.")
        return
    data[code].modify_stock_size(number)

def delete_command(data, code):
    """
    This function is to delete the product from the inventory

    :param data: dict[int, Product], dict of all known products.
    :param parameters: str, product's code
    """
    try:
        # First parameter was supposed to be a products code i.e. an integer
        # If either of these assumptions fail
        # ValueError will be raised.
        code = int(code)

    except ValueError:
        print(f"Error: product '{code}' can not be deleted as it does not exist.")
        return

    # <code> should be an existing product code in the <warehouse>.
    if code not in data:
        print(f"Error: product '{code}' can not be deleted as it does not exist.")
        return
    if data[code].get_stock() > 0:
        print(f"Error: product '{code}' can not be deleted as stock remains.")
        return
    del data[code]

def low_command(data):
    """
    This function is to alert the user when the amount of items
    drop below <LOW_STOCK_LIMIT>.

    :param data: dict[int, Product], dict of all known products.
    """
    for code in sorted(data):
        if data[code].get_stock() <= LOW_STOCK_LIMIT:
            print_code_command(data, code)

def combine_command(data, parameters):
    """
    This function is to allows the combining of two products into one.

    :param data: dict[int, Product], dict of all known products.
    :param parameters: str, included code1 and code2
    """

    try:
        # Let's try splitting the <parameters> string into two parts.
        # Raises ValueError if there are more or less than exactly two
        # values (in this case there should be two int) in
        # the <parameters> string.
        code1, code2 = parameters.split()

        # First parameter was supposed to be a products code i.e. an integer
        # and the second should be a float. If either of these assumptions fail
        # ValueError will be raised.
        code1 = int(code1)
        code2 = int(code2)

    except ValueError:
        print(f"Error: bad parameters '{parameters}' for combine command.")
        return

    # <code> should be an existing product code in the <warehouse>.
    if code1 not in data or code2 not in data or code1 == code2:
        print(f"Error: bad parameters '{parameters}' for combine command.")
        return
    price1 = data[code1].get_price()
    price2 = data[code2].get_price()
    cate1 = data[code1].get_category()
    cate2 = data[code2].get_category()
    stock2 = data[code2].get_stock()
    if cate1 != cate2:
        print(f"Error: combining items of different categories '{cate1}' and '{cate2}'.")
    elif price1 != price2:
        print(f"Error: combining items with different prices {price1}€ and {price2}€.")
    else:
        # add stock2 into stock1
        change_amount_command(data, str(code1) + " " + str(stock2))
        # empty stock2 to delete product2
        change_amount_command(data, str(code2) + " " + str(-stock2))
        delete_command(data, str(code2))

def sale_command(data, parameters):
    """
    This function is to sets all the products in the category on sale for sale_percentage% (float).

    :param data: dict[int, Product], dict of all known products.
    :param parameters: str, included category and sale percentage
    """

    try:
        # Let's try splitting the <parameters> string into two parts.
        # Raises ValueError if there are more or less than exactly two
        # values (in this case there should be one string and one float) in
        # the <parameters> string.
        category, percentage = parameters.split()

        # First parameter was supposed to be a products code i.e. an integer
        # and the second should be a float. If either of these assumptions fail
        # ValueError will be raised.
        percentage = float(percentage)

    except ValueError:
        print(f"Error: bad parameters '{parameters}' for sale command.")
        return

    # <category> should be an existing category in the <warehouse>.
    counter = 0
    for code in sorted(data):
        if data[code].get_category() == category:
            counter += 1
           
            data[code].set_new_price(percentage)

    print(f"Sale price set for {counter} items.")

def main():
    filename = input("Enter database name: ")
    # filename = "products.txt"

    warehouse = read_database(filename)
    if warehouse is None:
        return

    while True:
        command_line = input("Enter command: ").strip()

        if command_line == "":
            return

        command, *parameters = command_line.split(maxsplit=1)

        command = command.lower()

        if len(parameters) == 0:
            parameters = ""
        else:
            parameters = parameters[0]

        # If you have trouble undestanding what the values
        # in the variables <command> and <parameters> are,
        # remove the '#' comment character from the next line.
        # print(f"TEST: {command=} {parameters=}")

        if "example".startswith(command) and parameters != "":
            """
            'Example' is not an actual command in the program. It is
            implemented only to allow you to get ideas how to handle
            the contents of the variable <parameters>.

            Example command expects user to enter two values after the
            command name: an integer and a float:

                Enter command: example 123456 1.23

            In this case the variable <parameters> would refer to
            the value "123456 1.23". In other words, everything that
            was entered after the actual command name as a single string.
            """

            example_function_for_example_purposes(warehouse, parameters)

        elif "print".startswith(command) and parameters == "":
            print_command(warehouse)

        elif "print".startswith(command) and parameters != "":
            print_code_command(warehouse, parameters)

        elif "delete".startswith(command) and parameters != "":
            delete_command(warehouse, parameters)

        elif "change".startswith(command) and parameters != "":
            change_amount_command(warehouse, parameters)

        elif "low".startswith(command) and parameters == "":
            low_command(warehouse)

        elif "combine".startswith(command) and parameters != "":
            combine_command(warehouse, parameters)

        elif "sale".startswith(command) and parameters != "":
            sale_command(warehouse, parameters)

        else:
            print(f"Error: bad command line '{command_line}'.")


if __name__ == "__main__":
    main()
