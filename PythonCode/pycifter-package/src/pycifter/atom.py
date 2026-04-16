import numpy as np
class Atom:
  def __init__(self, inputList:list[str],conversionMatrix,radii: dict[str,float],nonMetalRadii: dict[str,float]):
    
    #Sample CIF file row for reference
    # K1 K 0.09311(7) 0.48374(6) 0.27798(6)

    self.covalentRadius:float=0
    elemname=inputList.pop(0) # Gets the atom identifier
    self.identifier=elemname
    ind1,ind2=0,0
    for i in range(len(elemname)):
      if(str.isdecimal(elemname[i])):
        ind1=i
        break
    for i in range(len(elemname)-1,-1,-1):
      if(str.isdecimal(elemname[i])):
        ind2=i
        break
    
    if(ind1==0 and ind2==0):
      self.atomLetter=""
      self.atomNum=1
      self.element=elemname
    else:
      self.atomLetter=elemname[ind2+1:]
      self.element=elemname[:ind1]
      self.atomNum=elemname[ind1:ind2+1]



    self.symbol=inputList.pop(0) # pops the symbol
    positionVectorWithUncertainty:list[str]=[inputList.pop(0),inputList.pop(0),inputList.pop(0)]
    intermediaryVectors:list[float]=[0,0,0]
    for v in range(3):
      elem=positionVectorWithUncertainty[v]
      if ('(' in elem ):
        intermediaryVectors[v]=float(elem[:elem.index("(")])
      else:
        intermediaryVectors[v]=float(elem)
      
    positionVectorCleanedSpherical=np.array(intermediaryVectors)

    self.positionVector=np.matmul(conversionMatrix,positionVectorCleanedSpherical)
    self.remainingNumbers=inputList

    if(self.symbol in radii):
      self.covalentRadius=radii[self.symbol]
    elif(self.symbol in nonMetalRadii):
      self.covalentRadius=nonMetalRadii[self.symbol]
  
  def __str__(self):
    return self.identifier
  
  def __repr__(self):
    return self.identifier
  

  def getDistance(self,other:Atom) -> float:
    distanceVector=[round(self.positionVector[i]-other.positionVector[i],6) for i in range(3)]
    output=0
    for j in distanceVector:
      output+=j**2
    
    return round(output**0.5,3)
  
  def __eq__(self, other:Atom) -> bool:
    for i in range(3):
      if(self.positionVector[i]!=other.positionVector[i]):
        return False
    
    return True
  
  
  def __hash__(self):
    return hash(tuple(self.positionVector))
  


  