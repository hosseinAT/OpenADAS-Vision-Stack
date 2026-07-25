from openadas.distance import estimate_distance_m,calculate_ttc
from openadas.types import Detection
def test_distance(): assert estimate_distance_m(Detection("car",.9,(0,0,180,100),1.8),900.)==9.0
def test_ttc(): assert calculate_ttc(10.,-2.)==5.0 and calculate_ttc(10.,2.) is None
