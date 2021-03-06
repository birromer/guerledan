# Guerledan experimental class at ENSTA Bretagne - 2020

The activities followed were:

1. Create a [driver](drivers/compass_drivers.py) for the LIS3MDL sensor in order to access the compass information.

2. Calibrate the compass so to convert the ellipsoid to the best possible shpere using two different methods. The implementation was done in [calibration.py](calibration.py), the captured data used can be found in the [data](data/) folder and the results can be found in the [images](images/) folder. 

3. Get the ddboat robot to orientate itself by following a given direction. That task was part of the goal of reaching a stable cycle inside a pool and it was partially achieved in [time_orientation.py](time_orientation.py), where the goal direction changed after a predetermined number of seconds, calibrated for the working environment.

4. Detect whenever the robot bumped into a limit of the pool, also being part of the end goal of reaching a stable cycle where the bumps would indicate the turning points. That task was implemented in [another driver](drivers/acc_gyro_driver.py), this one accessing the gyroscope and accelerometer information. The accuracy of the bump detection was analyzed in [acc_analysis.py](acc_analysis.py) and an example of the outputs can be seen [here](images/bumps.png)

5. Get the robot to perform a stable cycle in the pool by turning a certain angle every time a bump is detected in some edge. That task was implemented in [bump_orientation.py](bump_orientation.py) and managed to work in a inner pool without wind, but more calibration was required for a precise working in a noisy outer pool. The recordings can be found in the [videos](videos/) folder and in [this recording](https://www.youtube.com/watch?v=EiN3b3HCuXk).

6. Analyze the interference in the magnetic field caused by the actioning of the mototrs, adding noise to the compass readings. That task was implemented in [tst_interference.py], generating measurements for different speeds. 
