import pandas as pd
import numpy as np
import os

PIPE_TABLE_FILENAME = r'fluid_software\pipe\pipe_sizes.csv'
# PIPE_TABLE_PATH = os.path.join(os.getcwd(), PIPE_TABLE_FILENAME)

PIPE_DF = pd.read_csv(r'pipe\pipe.py')

def search_by_nps(df, nps, standard_only=False):
    result = df[df['NPS'] == nps]
    if standard_only:
        
        result = result[
            (result['Identification'].isnull() | (result['Identification'] == 'STD'))
        ]
    return result

def search_by_schedule(df, schedule, standard_only=False):
    result = df[df['Schedule'] == schedule]
    if standard_only:
        result = result[
            (result['Identification'].isnull() | (result['Identification'] == 'STD'))
        ]
    return result

def search_by_nps_and_schedule(df, nps, schedule, standard_only=False):
    result = df[(df['NPS'] == nps) & (df['Schedule'] == schedule)]
    if standard_only:
        result = result[result['Identification'].isnull() | (result['Identification'].str.upper() == 'STD')]
    return result

def search_by_nps_and_identification(df, nps, identification, standard_only=False):
    result = df[(df['NPS'] == nps) & (df['Identification'] == identification)]
    if standard_only:
        result = result[result['Identification'].isnull() | (result['Identification'].str.upper() == 'STD')]
    return result

def search_by_inside_diameter(df, inside_diameter, tol=0.01, n=None):
    sorted_df = df.assign(
        diff=np.abs(df['Inside Diameter'] - inside_diameter)
    ).sort_values('diff')
    if n is not None:
        sorted_df = sorted_df.head(n)
    return sorted_df.drop(columns='diff')

def search_by_area(df, area, n=None):
    df = df.assign(diff=np.abs(df['Area'] - area))
    sorted_df = df.sort_values('diff')
    if n is not None:
        sorted_df = sorted_df.head(n)
    return sorted_df.drop(columns='diff')

class Pipe:
    def __init__(self, nps, schedule, outside_diameter, wall_thickness):
        self.nps = nps
        self.schedule = schedule
        self.outside_diameter = outside_diameter
        self.wall_thickness = wall_thickness
        self.inside_diameter = self.outside_diameter - 2 * self.wall_thickness
        self.area = np.pi * (self.inside_diameter / 2) ** 2
    def __repr__(self):
        return (f"<Pipe: NPS={self.nps}, Schedule='{self.schedule}', "
                f"OD={self.outside_diameter:.3f} in, WT={self.wall_thickness:.3f} in, "
                f"ID={self.inside_diameter:.3f} in, Area={self.area:.4f} in^2>")

