import os
import json
import pandas as pd

class DataIngestor:
    def __init__(self, csv_path: str):
        self.data = pd.read_csv(csv_path)

        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week',
        ]

    def create_best5_job(self, question):
        def best5():
            return (self.data.loc[self.data['Question'] == question]
                    .groupby('LocationDesc')['Data_Value']
                    .mean()
                    .sort_values(ascending=question in self.questions_best_is_min)
                    .head(5)
                    .to_json())
        return best5
    
    def create_worst5_job(self, question):
        def worst5():
            return (self.data.loc[self.data['Question'] == question]
                    .groupby('LocationDesc')['Data_Value']
                    .mean()
                    .sort_values(ascending=question in self.questions_best_is_max)
                    .head(5)
                    .to_json())
        return worst5

    def create_states_mean_job(self, question):
        def states_mean():
            return (self.data.loc[self.data['Question'] == question]
                    .groupby('LocationDesc')['Data_Value']
                    .mean()
                    .sort_values(ascending=question in self.questions_best_is_min)
                    .to_json())
        return states_mean
    
    def create_state_mean_job(self, question, state):
        def state_mean():
            return (self.data.loc[(self.data['Question'] == question) & (self.data['LocationDesc'] == state)]
                    .groupby('LocationDesc')['Data_Value']
                    .mean()
                    .to_json())
        return state_mean
    
    def create_global_mean_job(self, question):
        def global_mean():
            return json.dumps({'global_mean': self.data.loc[self.data['Question'] == question]['Data_Value'].mean()})
        return global_mean
    
    def create_diff_from_mean_job(self, question):
        def diff_from_mean():
            return (self.data.loc[self.data['Question'] == question]['Data_Value'].mean() -
                  self.data.loc[self.data['Question'] == question]
                  .groupby('LocationDesc', sort=False)['Data_Value']
                  .mean()).to_json()
        return diff_from_mean
    
    def create_state_diff_from_mean_job(self, question, state):
        def state_diff_from_mean():
            return (self.data.loc[self.data['Question'] == question]['Data_Value'].mean() -
                  self.data.loc[(self.data['Question'] == question) & (self.data['LocationDesc'] == state)]
                  .groupby('LocationDesc')['Data_Value']
                  .mean()).to_json()
        return state_diff_from_mean
    
    def create_mean_by_category_job(self, question):
        def mean_by_category():
            return (self.data.loc[self.data['Question'] == question]
                    .groupby(['LocationDesc','StratificationCategory1','Stratification1'])['Data_Value']
                    .mean()
                    .to_json())
        return mean_by_category
    
    def create_state_mean_by_category_job(self, question, state):
        def state_mean_by_category():
            return (self.data.loc[(self.data['Question'] == question) & (self.data['LocationDesc'] == state)]
                    .groupby(['LocationDesc','StratificationCategory1','Stratification1'])['Data_Value']
                    .mean().reset_index().pivot_table(index='LocationDesc', columns=['StratificationCategory1', 'Stratification1'], values='Data_Value')
                    .to_json(orient='index', double_precision=14))
        return state_mean_by_category
