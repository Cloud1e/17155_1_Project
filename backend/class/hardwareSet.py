class hardwareSet:
    def __init__(self):
        self.__capacity = 0  
        self.__availability = 0  

    def __init__(self, capacity, availability):
        self.__capacity = capacity
        self.__availability = availability

    def get_availability(self):
        return self.__availability

    def get_capacity(self):
        return self.__capacity
    
    def get_remain(self):
        return self.__capacity - self.__availability

    def check_out(self, qty):
        if qty <= self.__availability:
            self.__availability -= qty
            return 0  # success
        else:
            self.__availability = 0
            return -1  
        
    def check_in(self, qty):
        if qty + self.__availability <= self.__capacity:
            self.__availability += qty
            return 0  # success
        else:
            self.__availability = self.__capacity
            return -1  
 