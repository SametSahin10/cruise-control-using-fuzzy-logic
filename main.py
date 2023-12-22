# Set the initial speed
    x = True
    G = 9.8
    initial_slope = 7
    initial_speed = 108.34301340128121
    target_speed = 90;
    while x:
    initial_speed -= math.sin(initial_slope)*G
    #print("eğimdeki hızz:", initial_speed)
    speed_stabilization.input['speed'] = initial_speed-target_speed

    speed_stabilization.compute()
    print("control signal:",speed_stabilization.output['control_signal'])
    initial_speed += speed_stabilization.output['control_signal']
    print("Input Speed:", initial_speed)
    time.sleep(1)

    # Compute the control signal

    speed.view()
    control_signal.view()

    # Print the results
    print("Input Speed:", initial_speed)
    print("Control Signal:", speed_stabilization.output['control_signal'])
    control_signal.view(sim=speed_stabilization)