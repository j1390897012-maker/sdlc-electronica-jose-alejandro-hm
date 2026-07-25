
class AlertStrategy:
        def send(self, message: str) -> None:
           pass




class AlertManager:
    def __init__(self, strategy: AlertStrategy) -> None:
        self.strategy = strategy
    
    
    def alert(self, message: str) -> None:
       self.strategy.send(message)




class ConsoleAlert(AlertStrategy):
    def send(self, message:str)->None:
        print(message)

class FileAlert(AlertStrategy):
    def __init__(self, filename: str) -> None:
        self.filename = filename
    
    def send(self, message:str)->None:
        with open(self.filename, "a") as file:
            file.write(message + "\n" )
   







