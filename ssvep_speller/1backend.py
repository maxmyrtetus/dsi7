import pylsl
import time
import random
import collections
import os

results_out = None
mrkstream_in = None
eeg_in = None

def lsl_mrk_outlet(name):
    info = pylsl.stream_info(name, 'Markers', 1, 0, pylsl.cf_string, 'ID66666666');
    outlet = pylsl.stream_outlet(info, 1, 1)
    print('backend.py created result outlet.')
    return outlet
    
def lsl_inlet(name):
    # Resolve all marker streams
    inlet = None
    tries = 0
    info = pylsl.resolve_stream('name', name)
    inlet = pylsl.stream_inlet(info[0], recover=False)
    print(f'backend.py has received the {info[0].type()} inlet.')
    return inlet
    
def main():
    terminate_backend = False
    store_data = False
    send_result = False
    
    # Wait for a marker, then start recording EEG data
    data = collections.deque() # fast datastructure for appending/popping in either direction
    
    print('main function started')
    while True and terminate_backend == False:
        # Constantly check for a marker
        mrk, t_mrk = mrkstream_in.pull_sample(timeout=0)
        eeg, t_eeg = eeg_in.pull_sample(timeout=0)
        print(eeg,t_eeg)
                
        if store_data and eeg is not None:
            data.append(eeg)

        elif send_result:
            send_result = False
            # do processing/classification here
            res = ['TL', 'TR', 'BL', 'BR'][random.randint(0, 3)] # inclusive

            # Wait 50ms then send a message (to give the task a chance to listen)
            time.sleep(0.05)
            print('Sent command')
            results_out.push_sample(pylsl.vectorstr([res]))

    
    
if __name__ == "__main__":
    # Initialize our streams
    random.seed()
    results_out = lsl_mrk_outlet('Result_Stream')
    mrkstream_in = lsl_inlet('Task_Markers')
    eeg_in = lsl_inlet('dsi-7')

    # Run out main function
    main()