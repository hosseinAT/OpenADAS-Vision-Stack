def estimate_distance_m(detection,focal_length_px):
 x1,_,x2,_=detection.bbox; width_px=max(x2-x1,1)
 return (detection.real_width_m*focal_length_px)/width_px if detection.real_width_m>0 else None
def calculate_ttc(distance_m,relative_speed_mps):
 if distance_m is None or relative_speed_mps is None or relative_speed_mps>=0: return None
 return distance_m/abs(relative_speed_mps)
