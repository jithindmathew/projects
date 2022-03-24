import numpy as np

def calculate(l):
    if len(l) < 9:
        raise ValueError("List must contain nine numbers.")

    l = np.array(l).reshape(3,3)

    calculations = {
        'mean': [
            np.mean(l, axis=0).tolist(), 
            np.mean(l, axis=1).tolist(), 
            np.mean(l).tolist()
        ],
        'variance': [
            np.var(l, axis=0).tolist(), 
            np.var(l, axis=1).tolist(), 
            np.var(l).tolist()            
        ],
        'standard deviation': [
            np.std(l, axis=0).tolist(), 
            np.std(l, axis=1).tolist(), 
            np.std(l).tolist()             
        ],
        'max': [
            np.max(l, axis=0).tolist(), 
            np.max(l, axis=1).tolist(), 
            np.max(l).tolist()   
        ],
        'min': [
            np.min(l, axis=0).tolist(), 
            np.min(l, axis=1).tolist(), 
            np.min(l).tolist()               
        ],
        'sum': [
            np.sum(l, axis=0).tolist(), 
            np.sum(l, axis=1).tolist(), 
            np.sum(l).tolist()               
        ]
    }
    
    return calculations