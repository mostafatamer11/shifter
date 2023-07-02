import front


class calc(front):
    
    def __init__(self, names:list[str], reqs:dict[str,int], dues:int):
        super()
        self.names = names
        self.reqs = reqs
        self.dues = dues
        self.final = list()
    
    def arrange(self):
        i = 0
        days = self.dues
        while days > 0:
            name = self.names[i]
            if self.reqs[name] == 0:
                self.final.append(name)
            
            else: self.reqs[name] -= 1
            i+=1
            if i == len(self.names): i = 0

            days -= 1
        return self.final

