import pandas as pd
import numpy as np
import os

#General commments from Garrett
## 1. In your directory you have 4 instances of the pipe_table(s).csv, you should
## only have one, it should be inside pipe/ and it should contain all the tables

PIPE_TABLE_FILENAME = 'pipe_table.csv'
PIPE_TABLE_PATH = os.path.join(os.getcwd(), PIPE_TABLE_FILENAME)

# Garrett: As discussed, you created the folder structure and know that the
# pipe table exists, you should remove this function since pipe_table.csv will
# always exist.
def ensure_pipe_table_exists(filepath):
    if not os.path.exists(filepath):
        with open(filepath, 'w'):
            pass

def load_pipe_table(filepath):
    ensure_pipe_table_exists(filepath)
    # Garrett: The pass keyword tells python to do nothing if this if statement evauluates
    # to True, what are you trying to make sure happens here?
    if os.path.getsize(filepath) == 0:
        with open(filepath, 'w'):
            pass
    df = pd.read_csv(filepath)
    return df

pipe_df = load_pipe_table(PIPE_TABLE_PATH)

def search_by_nps(df, nps, standard_only=False):
    result = df[df['NPS'] == nps]
    if standard_only:
        # Garrett: As discussed, the idea of a "standard pipe" is that the entry in the 
        # pipe table has any value in 'Identification' or 'Schedule', not that
        # the 'Idenfication' == 'STD'. Something like:
        #'Identification'.isnull() & 'Schedule'.isnull() (This is pseudocode, you'll have to alter it to make it work)
        result = result[
            (result['Identification'].isnull() | (result['Identification'] == 'STD'))
        ]
    return result

def search_by_schedule(df, schedule, standard_only=False):
    result = df[df['Schedule'] == schedule]
    if standard_only:
        #Garrett: See above logic comment
        result = result[
            (result['Identification'].isnull() | (result['Identification'] == 'STD'))
        ]
    return result

def search_by_nps_and_schedule(df, nps, schedule, standard_only=False):
    result = df[(df['NPS'] == nps) & (df['Schedule'] == schedule)]
    # Garrett: Don't worry about having standard_only in this one since they are specifying
    # the schedule in the search already so it will always be standard
    if standard_only:
        result = result[result['Identification'].isnull() | (result['Identification'].str.upper() == 'STD')]
    return result

def search_by_nps_and_identification(df, nps, identification, standard_only=False):
    result = df[(df['NPS'] == nps) & (df['Identification'] == identification)]
    if standard_only:
        result = result[result['Identification'].isnull() | (result['Identification'].str.upper() == 'STD')]
    return result

# Garrett: Add a function identical to search_by_nps_and_schedule, but search_by_nps_and_identificaiton

def search_by_inside_diameter(df, inside_diameter, tol=0.01, n=None):
        # Garrett: I'd recommend removing the tolerance filtering step, you're
        # already capturing this functionality with the n parameter essentially
        filtered = df[np.abs(df['Inside Diameter'] - inside_diameter) < tol]
        sorted_df = filtered.assign(
            diff=np.abs(filtered['Inside Diameter'] - inside_diameter)
        ).sort_values('diff').drop(columns='diff')
        if n is not None:
            return sorted_df.head(n)
        return sorted_df

# Garrett: Make this a sorted df rather than filtering the way you did with the
# search_by_inside_diameter function
def search_by_area(df, area, tol=0.01):
    return df[np.abs(df['Area'] - area) < tol]

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
