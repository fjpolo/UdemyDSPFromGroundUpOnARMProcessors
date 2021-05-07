#
# Imports
#
import numpy as np
import signals as sigs

#
# Global variables
#

#
# Private functions
#

#
# main
#
if __name__ == "__main__":
    signal_mean = np.mean(sigs.InputSignal_1kHz_15kHz)
    print("The signal's mean is: ", signal_mean)
    # [Done] exited with code=0 in 3.962 seconds