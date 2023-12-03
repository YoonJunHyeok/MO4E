from abc import ABC

class Predictor(ABC):
    # 추상클래스 - Predictor 상속받은 애는 밑에 두 함수 무조건 구현해야함
    @abstractmethod
    def load_model(model_path: str):
        pass
    
    @abstractmethod
    def predict(input):
        pass