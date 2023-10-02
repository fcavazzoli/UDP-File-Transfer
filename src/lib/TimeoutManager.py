from time import perf_counter as now

# Constants
ALPHA = 0.125
BETA = 0.25
INITIAL_ESTIMATED_RTT = 0.0
INITIAL_DEVIATION_RTT = 0.0
INITIAL_TIMEOUT_INTERVAL = 1.0
INITIAL_SEND_TIME = -1

# Congestion control.
# Jacobson/Karels algorithm for estimating the Round-Trip Time (RTT) & also the deviation of the RTT.
class TimeoutManager:
    def __init__(self):
        self.alpha = ALPHA
        self.beta = BETA
        self.estimated_rtt = INITIAL_ESTIMATED_RTT
        self.dev_rtt = INITIAL_DEVIATION_RTT
        self.timeout_interval = INITIAL_TIMEOUT_INTERVAL
        
        #The time when a packet or network message was originally sent from the sender to the receiver.
        self.send_time = INITIAL_SEND_TIME

    def calculate_timeout(self, sample_rtt):
        self.estimated_rtt = self.calculate_estimated_rtt(self, sample_rtt)
        self.dev_rtt = self.calculate_dev_rtt(self, sample_rtt)
        self.timeout_interval = self.calculate_timeout_interval(self)

    def get_timeout_interval(self):
        return max(0.01, min(self.timeout_interval, 1.0))

    def handle_timeout_event(self):
        self.timeout_interval *= 2.0

    def calculate_estimated_rtt(self, sample_rtt):
            return ((1 - self.alpha) * self.estimated_rtt + self.alpha * sample_rtt)
    
    def calculate_dev_rtt(self, sample_rtt):
         return ((1 - self.beta) * self.dev_rtt + self.beta * abs(sample_rtt - self.estimated_rtt))

    def calculate_timeout_interval(self):
         return self.estimated_rtt + 4 * self.dev_rtt
    
    def calculate_timeout_from_now(self, start):
         return self.calculate_timeout(now() - start)
    