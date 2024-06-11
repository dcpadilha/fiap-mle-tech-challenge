import numpy as np  
from typing import Union, TypeAlias  
from pydantic import BaseModel, root_validator  
  
Numero: TypeAlias = Union[int, float]  
  
class NumpyArray(np.ndarray):  
    @classmethod  
    def __get_validators__(cls):  
        yield cls.validate  
  
    @classmethod  
    def validate(cls, value, field, config):  
        if isinstance(value, np.ndarray):  
            return value  
        raise TypeError(f'Expected np.ndarray, received {type(value)}')  
  
class DadosModelo(BaseModel):  
    X: NumpyArray  
    y: NumpyArray  
  
    class Config:  
        arbitrary_types_allowed = True  
  
    @root_validator(pre=True)  
    def convert_to_ndarray(cls, values):  
        for key in ['X', 'y']:  
            if key in values and not isinstance(values[key], np.ndarray):  
                values[key] = np.array(values[key])  
        return values  
  
X = np.random.randn(10)  
y = np.random.randn(10)  
  
dado_externo = {"X": X, "y": y}  
algo = DadosModelo(**dado_externo)  
  
print(algo.X)  
print(type(algo.X))  # Verify that the type is np.ndarray  

