





class HeartBeatMonitoring:
    
    ###########################################################################
    ###########################################################################
    
    def __init__(self, client, base_topic):
        self.client = client
        self.base_topic = base_topic
        self.alive = False
        self.enabled = False
        self.heartbeat = 0
        self.observers = []

    def enable(self):
        self.client.subscribe(self.base_topic + "/info")
        self.alive = False
        self.enabled = True
        self.heartbeat = time.time()

    def disable(self):
        self.client.unsubscribe(self.base_topic + "/info")
        self.enabled = False

    def update(self):
        if self.enabled:
            # print("info !!!  ", time.time(), "\n")
            
            elapsed = time.time() - self.heartbeat
            self.heartbeat = time.time()

            old_state = self.alive
            if elapsed > 5 and self.alive:
                self.alive = False
            elif not self.alive:
                self.alive = True

            # Notify observers
            if old_state != self.alive:
                for obs in self.observers:
                    obs(self.alive)

    def add_observer(self, cb):
        self.observers.append(cb)
    
    def rem_observer(self, cb):
        self.observers.remove(cb)
        


