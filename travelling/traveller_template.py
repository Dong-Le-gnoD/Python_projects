"""
COMP.CS.100 Ohjelmointi 1 / Programming 1
Student Id: 151057054
Name:       Dong Le
Email:      dong.le@tuni.fi

Project 3: implement a program which can be used to examine distances and routes between cities. 
The program reads data from a file and imports those data to a dictionary.
There are four actions in the program: display all info, adding new route, 
remove routes, and display a route base on departure and destination.
"""


def find_route(data, departure, destination):
    """
    This function tries to find a route between <departure>
    and <destination> cities. It assumes the existence of
    the two functions fetch_neighbours and distance_to_neighbour
    (see the assignment and the function templates below).
    They are used to get the relevant information from the data
    structure <data> for find_route to be able to do the search.

    The return value is a list of cities one must travel through
    to get from <departure> to <destination>. If for any
    reason the route does not exist, the return value is
    an empty list [].

    :param data: ?????, A data structure of an unspecified type (you decide)
           which contains the distance information between the cities.
    :param departure: str, the name of the departure city.
    :param destination: str, the name of the destination city.
    :return: list[str], a list of cities the route travels through, or
           an empty list if the route can not be found. If the departure
           and the destination cities are the same, the function returns
           a two element list where the departure city is stored twice.
    """

    # +--------------------------------------+
    # |                                      |
    # |     DO NOT MODIFY THIS FUNCTION!     |
    # |                                      |
    # +--------------------------------------+

    if departure not in data:
        return []

    elif departure == destination:
        return [departure, destination]

    greens = {departure}
    deltas = {departure: 0}
    came_from = {departure: None}

    while True:
        if destination in greens:
            break

        red_neighbours = []
        for city in greens:
            for neighbour in fetch_neighbours(data, city):
                if neighbour not in greens:
                    delta = deltas[city] + distance_to_neighbour(data, city, neighbour)
                    red_neighbours.append((city, neighbour, delta))

        if not red_neighbours:
            return []

        current_city, next_city, delta = min(red_neighbours, key=lambda x: x[2])

        greens.add(next_city)
        deltas[next_city] = delta
        came_from[next_city] = current_city

    route = []
    while True:
        route.append(destination)
        if destination == departure:
            break
        destination = came_from.get(destination)

    return list(reversed(route))


def read_distance_file(file_name):
    """
    Reads the distance information from <file_name> and stores it
    in a suitable data structure (you decide what kind of data
    structure to use). This data structure is also the return value,
    unless an error happens during the file reading operation.

    :param file_name: str, The name of the file to be read.
    :return: ????? | None: A data structure containing the information
             read from the <file_name> or None if any kind of error happens.
             The data structure to be chosen is completely up to you as long
             as all the required operations can be implemented using it.
    """
    # Initialize the a dictionary for the data.
    dict = {}
    try:
        # Try to open the file for the reading of the data.
        data_file = open(file_name, mode = "r")

        # Populate the dictionary, until the file has been processed.
        # A nested loop is needed, because the data structure is nested.

        for row in data_file:
            str_data = row.rstrip().split(";")
            city = str_data[0]
            des = str_data[1]
            distance = int(str_data[2])
            if city not in dict:
                dict[city] = {}

            dict[city][des] = distance

        # Close the file.
        data_file.close()
    except OSError:

        dict = None
    # Return the data or the error code.
    return dict


def fetch_neighbours(data, city):
    """
    Returns a list of all the cities that are directly
    connected to parameter <city>. In other words, a list
    of cities where there exist an arrow from <city> to
    each element of the returned list. Return value is
    an empty list [], if <city> is unknown or if there are no
    arrows leaving from <city>.

    :param data: ?????, A data structure containing the distance
           information between the known cities.
    :param city: str, the name of the city whose neighbours we
           are interested in.
    :return: list[str], the neighbouring city names in a list.
             Returns [], if <city> is unknown (i.e. not stored as
             a departure city in <data>) or if there are no
             arrows leaving from the <city>.
    """
    neighbours = []
    if city in data:
        for fact_key in sorted(data[city]):
            neighbours.append(fact_key)
    return neighbours   


def distance_to_neighbour(data, departure, destination):
    """
    Returns the distance between two neighbouring cities.
    Returns None if there is no direct connection from
    <departure> city to <destination> city. In other words
    if there is no arrow leading from <departure> city to
    <destination> city.

    :param data: ?????, A data structure containing the distance
           information between the known cities.
    :param departure: str, the name of the departure city.
    :param destination: str, the name of the destination city.
    :return: int | None, The distance between <departure> and
           <destination>. None if there is no direct connection
           between the two cities.
    """
    if departure not in data:
        return None
    if destination not in sorted(data[departure]):
        return None
    else:
        return data[departure][destination]


def display_data(data):
    """
    sorting the data and print dictionary based on city name alphabet
    and also print the destination based on alphabet order.
    :param data: A data structure containing the distance
           information between the known cities.
    :return: print out all info
    """
    for name in sorted(data):
        # Print the facts.
        for fact_key in sorted(data[name]):
            fact_value = data[name][fact_key]
            print(f"{name:<14}{fact_key:<14}{fact_value:>5}")

def add_data(data):
    """
    user enters departure, destination, and distance of 2 cities.
    The process continues if the distance is integer.
    if the departure is not available in the data, add it on.
    then add destination and distance to the data
    :param data: A data structure containing the distance
           information between the known cities.
    :return: the distance_data dictionary
    """
    # Read the inputs from the user.
    name = input("Enter departure city: ")
    fact_key = input("Enter destination city: ")
    fact_value = input("Distance: ")
    if fact_value.isdigit():
        # Add info to the data
        if name not in data:
            data[name] = {}

        # Add the new fact to the data.
        data[name][fact_key] = int(fact_value)
    else:
        print(f"Error: '{fact_value}' is not an integer.")
    return data

def remove_data(distance_data):
    """
    user enters departure, destination.
    if the departure is not in data, the process shut down, also the same as destination
    The process continues if both cities are valid.
    then remove departure and destination from the data
    :param distance_data: A data structure containing the distance
           information between the known cities.
    :return: the distance_data dictionary
    """
    # Read the inputs from the user.
    name = input("Enter departure city: ")
    if check_city_valid(distance_data, name):
        fact_key = input("Enter destination city: ")

        if fact_key not in distance_data[name]:
            print(f"Error: missing road segment between '{name}' and '{fact_key}'.")
        else:
            # remove the fact from the data.
            del distance_data[name][fact_key]
    else:
        print(f"Error: '{name}' is unknown.")
    return distance_data

def print_neighbours(distance_data):
    """
    user enters departure.
    if the departure is not in data, the process shut down
    The process continues if the city is valid.
    :param distance_data: A data structure containing the distance
           information between the known cities.
    :return: print out the neighbours of the city in alphabet order
    """
    name = input("Enter departure city: ")
    if check_city_valid(distance_data, name):
        if name in distance_data:
            for fact_key in sorted(distance_data[name]):
                fact_value = distance_data[name][fact_key]
                print(f"{name:<14}{fact_key:<14}{fact_value:>5}")
    else:
        print(f"Error: '{name}' is unknown.")

def check_city_valid(data, city):
    """
    check if the city is in the departure data, then check if it is in destination
    :param distance_data: A data structure containing the distance
           information between the known cities.
    :param city: the name of city which need to check whether in the data
    :return: True if the city either departure or destination
    """
    for cities in data:
        if city == cities:
            return True
        elif city in data[cities]:
            return True
    return False

def print_route(distance_data):
    """
    user enters departure and destination
    if the departure is not in data, the process shut down
    The process continues if the city is valid.
    :param distance_data: A data structure containing the distance
           information between the known cities.
    :return: print out the route from the departure and destination
    """
    name = input("Enter departure city: ")
    if check_city_valid(distance_data, name):
        fact_key = input("Enter destination city: ")

        route = find_route(distance_data, name, fact_key)
        if route == []:
            print(f"No route found between '{name}' and '{fact_key}'.")
        elif route[0] == route[-1]:
            print(f"{name}-{name} (0 km)")
        else:
            sum_dis = 0
            for i in range(len(route)-1):
                sum_dis += distance_data[route[i]][route[i+1]]
            for city in route:
                if city == fact_key:
                    print(f"{city} ({sum_dis} km)")
                else:
                    print(city, end="-")
    else:
        print(f"Error: '{name}' is unknown.")

def main():
    input_file = input("Enter input file name: ")

    distance_data = read_distance_file(input_file)

    if distance_data is None:
        print(f"Error: '{input_file}' can not be read.")
        return

    while True:
        action = input("Enter action> ")

        if action == "":
            print("Done and done!")
            return

        elif "display".startswith(action):
            display_data(distance_data)

        elif "add".startswith(action):
            distance_data = add_data(distance_data)

        elif "remove".startswith(action):
            distance_data = remove_data(distance_data)

        elif "neighbours".startswith(action):
            print_neighbours(distance_data)

        elif "route".startswith(action):
            print_route(distance_data)

        else:
            print(f"Error: unknown action '{action}'.")


if __name__ == "__main__":
    main()
