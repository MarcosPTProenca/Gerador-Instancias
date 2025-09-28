def calculate_metrics(n_caminhoes, n_machines, alpha, p, t, d):
    """
    Calculate the makespan, number of delays, maximum delay, and sum of delays.

    Parameters:
    n_caminhoes (int): number of trucks
    n_machines (int): number of forklifts
    alpha (dict): assignment of operations to forklifts and trucks
    p (list): list of tuples (operation, machine, processing_time)
    t (dict): start times of operations
    A (dict): maximum delay for each truck
    d (dict): scheduled departure date for each truck

    Returns:
    dict: containing makespan, num_delays, max_delay, sum_delays
    """
    # Create a mapping from (operation, machine) to processing time
    processing_time = {(op, machine): pt for op, machine, pt in p}

    # List to store operation details
    operations_info = []

    if n_machines <= n_caminhoes:
        # Keys of alpha are forklifts
        for forklift, matrix in alpha.items():
            num_operations, num_trucks = matrix.shape
            for row in range(num_operations):
                operation = row + 1  # Operations start from 1
                for col in range(num_trucks):
                    truck = col + 1  # Trucks start from 1
                    if matrix[row][col] == 1:
                        start_time = t.get(operation)
                        proc_time = processing_time.get((operation, forklift))
                        if start_time is None or proc_time is None:
                            continue  # Skip if data is missing
                        completion_time = start_time + proc_time
                        operations_info.append({
                            'operation': operation,
                            'forklift': forklift,
                            'truck': truck,
                            'start_time': start_time,
                            'processing_time': proc_time,
                            'completion_time': completion_time
                        })
    else:
        # Keys of alpha are trucks
        for truck, matrix in alpha.items():
            num_operations, num_forklifts = matrix.shape
            for row in range(num_operations):
                operation = row + 1
                for col in range(num_forklifts):
                    forklift = col + 1
                    if matrix[row][col] == 1:
                        start_time = t.get(operation)
                        proc_time = processing_time.get((operation, forklift))
                        if start_time is None or proc_time is None:
                            continue  # Skip if data is missing
                        completion_time = start_time + proc_time
                        operations_info.append({
                            'operation': operation,
                            'forklift': forklift,
                            'truck': truck,
                            'start_time': start_time,
                            'processing_time': proc_time,
                            'completion_time': completion_time
                        })

    # Calculate makespan
    makespan = max(op['completion_time'] for op in operations_info)

    # Calculate delays for each truck
    truck_completion_times = {}
    for op in operations_info:
        truck = op['truck']
        completion_time = op['completion_time']
        truck_completion_times.setdefault(truck, []).append(completion_time)

    delays = {}
    for truck, times in truck_completion_times.items():
        actual_departure_time = max(times)
        scheduled_departure_time = d.get(truck, 0)
        delay = max(0, actual_departure_time - scheduled_departure_time)
        delays[truck] = delay

    # Number of trucks with delay
    num_delays = sum(1 for delay in delays.values() if delay > 0)

    # Maximum delay
    max_delay = max(delays.values()) if delays else 0

    # Sum of delays
    sum_delays = sum(delays.values())

    return {
        'makespan': makespan,
        'num_delays': num_delays,
        'max_delay': max_delay,
        'sum_delays': sum_delays
    }

