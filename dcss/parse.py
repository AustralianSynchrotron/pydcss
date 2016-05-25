import re


def parse_start_operation(message):

    """
    Parses "..._start_operation" type messages.
    Returns a dictionary with:
      * direction: message direction (stog, stoh, gtos, htos, stoc)
      * name: operation name (str)
      * handle: operation handle (str)
      * arguments: operation arguments (str or None)
    """

    regex = r'^(?P<direction>.*)_start_operation (?P<name>\S+) +'\
            r'(?P<handle>\S+)( +(?P<arguments>.*))? *$'
    return re.search(regex, message).groupdict()


def parse_operation_update(message):

    """
    Parses "..._operation_update" type messages.
    Returns a dictionary with:
      * direction: message direction (stog, stoh, gtos, htos, stoc)
      * name: operation name (str)
      * handle: operation handle (str)
      * arguments: operation update arguments (str or None)
    """

    regex = r'^(?P<direction>.*)_operation_update (?P<name>\S+) +'\
            r'(?P<handle>\S+)( +(?P<arguments>.*))? *$'
    return re.search(regex, message).groupdict()


def parse_operation_completed(message):

    """
    Parses "..._operation_completed" type messages.
    Returns a dictionary with:
      * direction: message direction (stog, stoh, gtos, htos, stoc)
      * name: operation name (str)
      * handle: operation handle (str)
      * arguments: operation update arguments (str or None)
    """

    regex = r'^(?P<direction>.*)_operation_completed (?P<name>\S+) +'\
            r'(?P<handle>\S+) +(?P<status>\S+)( +(?P<arguments>.*))? *$'
    return re.search(regex, message).groupdict()


def parse_holder_found_message(message):

    """
    Parses "stog_operation_update robot_config ... found ..." messages.
    Returns a dictionary with:
      * handle: operation handle (str)
      * position: holder position ('left', 'middle', 'right', 'unknown')
      * type: holder type ('calibration', 'cassette', 'puck adaptor', 'unknown')
      * dz: height difference (float)
    """

    regex = r'robot_config +(?P<handle>\S+) +'\
            r'found +(?P<type>.+) +(?P<position>.) +'\
            r'dz: +(?P<dz>\S+) *$'
    data = re.search(regex, message).groupdict()
    # TODO: Handle regex fail - log message and raise exception
    # TODO: Add warning if position or type unknown
    position_lookup = {'l': 'left', 'm': 'middle', 'r': 'right'}
    holder_lookup = {
        'calibration cassette': 'calibration cassette',
        'normal cassette': 'cassette',
        'super puck adaptor': 'puck adaptor',
    }
    parsed = {
        'handle': data['handle'],
        'position': position_lookup.get(data['position'], 'unknown'),
        'type': holder_lookup.get(data['type'], 'unknown'),
        'dz': float(data['dz']),
    }
    return parsed


def parse_robot_force_message(message):

    """
    Parses "stog_set_string_completed robot_force_..." messages.
    Returns a dictionary with:
      * position: holder position ('left', 'middle', 'right', 'unknown')
      * status: (str)
      * height: cassette height (float)
      * forces: list of dictionaries with keys:
        * force: force measurement (float or None)
        * empty: if port is empty (bool)
    """

    regex = r'robot_force_(?P<position>\S+) +(?P<status>\S+?) +'\
            r'(?P<height>\S+)(?P<forces>( +\S+)+) *$'
    data = re.search(regex, message).groupdict()
    # TODO: Handle regex fail - log message and raise exception
    forces = []
    for force_str in data['forces'].split():
        if force_str == 'EEEE':
            force = 'empty'
        elif force_str == 'uuuu':
            force = 'unknown'
        else:
            try:
                force = float(force_str)
            except ValueError:
                # TODO: Add logging
                raise ValueError
        forces.append(force)

    parsed = {
        'position': data['position'],
        'status': data['status'],
        'height': float(data['height']),
        'forces': forces,
    }

    return parsed


def parse_robot_cassette_message(message):

    """
    Parses "stog_set_string_completed robot_cassette ..." messages.
    Returns a dictionary with:
      * status: (str)
      * holders: list of dictionaries containing:
        * type: 'calibration cassette', 'cassette', 'puck adaptor', 'bad', 'unknown'
        * ports: 96 element list of '0', '1', 'j', 'u', '-', 'b'
    """

    regex = r'robot_cassette +(?P<status>.+?)(?P<holder_data>( +\S){291})'
    data = re.search(regex, message).groupdict()
    holder_data = data['holder_data'].split()
    holders = []

    type_lookup = {
        '1': 'cassette',
        '2': 'calibration cassette',
        '3': 'puck adaptor',
        'X': 'bad',
        'u': 'unknown',
    }

    elems_per_holder = 97  # 96 ports plus 1 for holder type
    for i in range(0, len(holder_data), elems_per_holder):
        # TODO: Add warning of no match
        holder_type = type_lookup.get(holder_data[i])
        holders.append({
            'type': holder_type,
            'ports': holder_data[i+1:i+elems_per_holder],
        })

    parsed = {
        'status': data['status'],
        'holders': holders,
    }

    return parsed


def parse_start_robot_probe_message(message):

    """
    Parses "_start_operation robot_config probe" type messages.
    Returns a dictionary with:
      * direction: message direction (stog, stoh, gtos, htos, stoc)
      * name: operation name (str)
      * handle: operation handle (str)
      * arguments: operation update arguments (str or None)
      * holders: list of dictionaries containing
        * probe_holder_type: 0 or 1
        * ports: 96 element list of 0 or 1
    """

    parsed = parse_start_operation(message)
    parsed['holders'] = []
    values = list(map(int, parsed['arguments'].replace('probe ', '').split()))
    for holder_idx in range(3):
        offset = holder_idx * 97
        parsed['holders'].append({
            'probe_holder_type': values[offset],
            'ports': values[offset+1:offset+97],
        })
    return parsed
