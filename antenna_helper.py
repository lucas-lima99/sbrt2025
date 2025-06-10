import warnings
import numpy as np
import math
import seaborn as sns

warnings.filterwarnings("ignore")


class AntennaHelper:

    def __init__(self, ngain_5,  ngain_10, ngain_15, ngain_20,
                 ngain_25, ngain_30, ngain_35, ngain_40, ngain_45,
                 ngain_50, ngain_55, ngain_60, ngain_65, ngain_70,
                 ngain_75, ngain_80, ngain_85, ngain_90,
                 gain_0, 
                 gain_5, gain_10, gain_15, gain_20,
                 gain_25, gain_30, gain_35, gain_40, gain_45,
                 gain_50, gain_55, gain_60, gain_65, gain_70,
                 gain_75, gain_80, gain_85, gain_90,
                 ):
        """
        Mapa de ganho vertical com os valores de ganho para cada ângulo, seguindo diagrama de radiação.

        """

        self.gain_map={
            -90: ngain_90,
            -85: ngain_85,
            -80: ngain_80,
            -75: ngain_75,
            -70: ngain_70,
            -65: ngain_65,
            -60: ngain_60,
            -55: ngain_55,
            -50: ngain_50,
            -45: ngain_45,
            -40: ngain_40,
            -35: ngain_35,
            -30: ngain_30,
            -25: ngain_25,
            -20: ngain_20,
            -15: ngain_15,
            -10: ngain_10,
            -5: ngain_5,
            0: gain_0,
            5: gain_5,
            10: gain_10,
            15: gain_15,
            20: gain_20,
            25: gain_25,
            30: gain_30,
            35: gain_35,
            40: gain_40,
            45: gain_45,
            50: gain_50,
            55: gain_55,
            60: gain_60,
            65: gain_65,
            70: gain_70,
            75: gain_75,
            80: gain_80,
            85: gain_85,
            90: gain_90,
            
        }

    @staticmethod
    def antenna_elevation(dist,alt1,alt2):
        """
        Calcula o ângulo de elevação entre dois pontos.
        dist: distância horizontal (metros)
        alt1: altitude do ponto 1 (metros)
        alt2: altitude do ponto 2 (metros)
        """
    
        delta_altitude = alt2 - alt1
        elevation_rad = -np.arctan2(delta_altitude, dist)
        elevation_deg = np.degrees(elevation_rad)
        return elevation_deg

    def vertical_attenuation(self, degree):

        """
        Retorna o valor de atenuação (negativo do ganho) para o ângulo. Se o ângulo não estiver tabelado,
        retorna um valor de interpolação.
        degree: ângulo de elevação (em graus). Varia entre 90° e -90° para a antena colinear da UFJF
        """
        print(f'Ângulo de elevação: {degree}°')

        if degree in self.gain_map:
            return self.gain_map[degree]

        # Ordena os ângulos disponíveis
        sorted_angles = sorted(self.gain_map.keys())

        # if degree < sorted_angles[0]: # ângulos abaixo de 0°
        #     print(f'Ângulo abaixo de 0°')
        #     degree = degree * -1
        if degree > sorted_angles[-1]: # ângulos acima de 90 graus e menores que 270
            # 95 vira 85, 100 vira 80, 105 vira 75
            print(f"Ângulo acima de 90°")

            degree = 90-(degree-90)

            # return -self.gain_map[sorted_angles[-1]]
        

        # Verifica os dois ângulos entre os quais o grau se encontra
        for i in range(len(sorted_angles) - 1):
            lowest_angle = sorted_angles[i]
            highest_angle = sorted_angles[i + 1]

            if lowest_angle < degree < highest_angle:
                # Interpolação linear   y = y1 + (x-x1) * (y2-y1)/(x2-x1), y é o ganho, x é elevação (graus)
                low_gain = self.gain_map[lowest_angle]   # y1
                high_gain = self.gain_map[highest_angle] # y2
                interpolated_gain = low_gain + (degree - lowest_angle) * ((high_gain - low_gain) / (highest_angle - lowest_angle))
                return interpolated_gain

        return v_attenuation
    
    def get_angles_gain(self):
        print(f"Formatação -> ângulos (graus): atenuação (dB)\n{self.gain_map}")

    def horizontal_attenuation(self, azimuth):
        #to do..
        h_attenuation = 0.0
        return h_attenuation

    def total_attenuation(self, degree, azimuth):

        v_attenuation = self.vertical_attenuation(degree)
        h_attenuation = self.horizontal_attenuation(azimuth)
        
        return (v_attenuation + h_attenuation)



antenna = AntennaHelper(
    0.0, -0.2, -0.5, -1.0, -1.5,
    -2.0, -2.5, -3.0, -3.5, -4.0,
    -4.5, -5.0, -5.5, -6.0, -6.5,
    -7.0, -7.5, -8.0, -8.5, -0.2, -0.5, -1.0, -1.5,
    -2.0, -2.5, -3.0, -3.5, -4.0,
    -4.5, -5.0, -5.5, -6.0, -6.5,
    -7.0, -7.5, -8.0, -8.5
)

# Cálculo do ângulo de elevação
elev = antenna.antenna_elevation(dist=100, alt1=400, alt2=600)

# Obter a atenuação vertical correspondente ao ângulo de elevação
att = antenna.vertical_attenuation(elev)
# total_att = antenna.total_attenuation(45,1)

# print(f"Elevação: {elev:.2f} graus")
print(f"Atenuação vertical: {att:.2f} dB")
# print(f"Atenuação total: {total_att:.2f} dB")



# antenna.get_angles_gain()
