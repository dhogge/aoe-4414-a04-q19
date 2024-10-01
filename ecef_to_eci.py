# ecef_to_eci.py
#
# Usage: python3 script_name.py arg1 arg2 ...
#  Text explaining script usage
# Parameters:
#  arg1: description of argument 1
#  arg2: description of argument 2
#  ...
# Output:
#  A description of the script output
#
# Written by Brad Denby
# Other contributors: Dylan Hogge
#
# Optional license statement, e.g., See the LICENSE file for the license.

# import Python modules
import sys  # argv
import math  # mathematical functions

# "constants"
w = 7.2921150e-5  # Earth's rotation rate in rad/s

# helper functions (if needed)

# initialize script arguments
year = float('nan')
month = float('nan')
day = float('nan')
hour = float('nan')
minute = float('nan')
second = float('nan')
ecef_x_km = float('nan')
ecef_y_km = float('nan')
ecef_z_km = float('nan')

# parse script arguments
if len(sys.argv) == 10:
    year = int(sys.argv[1])
    month = int(sys.argv[2])
    day = int(sys.argv[3])
    hour = int(sys.argv[4])
    minute = int(sys.argv[5])
    second = float(sys.argv[6])
    ecef_x_km = float(sys.argv[7])
    ecef_y_km = float(sys.argv[8])
    ecef_z_km = float(sys.argv[9])
else:
    print(
        'Usage: python3 ecef_to_eci.py year month day hour minute second ecef_x_km ecef_y_km ecef_z_km'
    )
    exit()

# write script below this line
# Compute Julian Date
JD = day - 32075 \
     + 1461 * (year + 4800 - (14 - month) // 12) // 4 \
     + 367 * (month - 2 + (14 - month) // 12 * 12) // 12 \
     - 3 * ((year + 4900 - (14 - month) // 12) // 100) // 4

JD_MN = JD - 0.5

D_fract = (second + 60 * (minute + 60 * hour)) / 86400
JD_fract = JD_MN + D_fract

T_UT1 = (JD_fract - 2451545.0) / 36525

# Calculate Greenwich Mean Sidereal Time (GMST) in seconds
theta_gmst_sec = 67310.54841 \
                 + (876600 * 3600 + 8640184.812866) * T_UT1 \
                 + 0.093104 * (T_UT1 ** 2) \
                 - 6.2e-6 * (T_UT1 ** 3)

# Reduce theta_gmst_sec to range [0,86400) seconds
theta_gmst_sec = theta_gmst_sec % 86400

# Convert GMST to radians
GMST = w * theta_gmst_sec

# Rotate ECEF coordinates to ECI
eci_x_km = ecef_x_km * math.cos(GMST) - ecef_y_km * math.sin(GMST)
eci_y_km = ecef_x_km * math.sin(GMST) + ecef_y_km * math.cos(GMST)
eci_z_km = ecef_z_km

# Print the ECI coordinates
print(round(eci_x_km, 3))
print(round(eci_y_km, 5))
print(round(eci_z_km, 3))

