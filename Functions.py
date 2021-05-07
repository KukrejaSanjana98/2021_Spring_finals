from IPython.core.display import display
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px


def mergedata(data1: pd.DataFrame, data2: pd.DataFrame) -> pd.DataFrame:
    """
    :param data1: This refers to the dataset 1 that is the input :World Happiness Report Dataset
    :param data2: This refers to the dataset 2 that is the input:World Health Expenditure Dataset
    :return:This will return the Clean Dataset
    >>> mergedata('Data/World Happiness Report.csv', 'Data/World Health Expenditure.csv').columns.to_list()
    ['Year', 'Country', 'Expentancy', 'index', 'Health Expenditure']
    """
    df1=pd.read_csv(data1)
    df1.head()
    df2=pd.read_csv(data2)
    df2.head()
    df1['Year']= df1['Year'].astype(str)
    df1['index'] = df1[['Year', 'Country']].apply(lambda x: ''.join(x), axis=1)
    df2['Year']= df2['Year'].astype(str)
    df2['index'] = df2[['Year', 'Country']].apply(lambda x: ''.join(x), axis=1)
    data=pd.merge(df1,df2, on=["index", "index"])
    data=data.drop(columns=['Year_y','Country_y','Happiness Score','Economy (GDP per Capita)','Freedom','Generosity','GDP per Capital','Health Personal'],axis=1)
    clean_data=data.rename(columns={'Year_x':'Year', 'Country_x':'Country','expenditure':'Expenditure'})
    return clean_data


def clean_age(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function cleans the age column of dataset.
    :param df:The input of this function is the dataframe
    :return:This function return the clean dataset

    >>> sample_data = pd.DataFrame({'What is your age?': [10, 15, 20, 30, 40, 50, 60, 70, 80]})
    >>> clean_age(sample_data)['What is your age?'].to_list()
    [20, 30, 40, 50, 60, 70]
    """
    df = df[(df['What is your age?'] >= 18) & (df['What is your age?'] < 75)]
    return df


def clean_gender(dataframe: pd.DataFrame)-> pd.DataFrame:
    """
    This function is used for cleaning of the columns inside the dataset,we will clean the Gender column and merge all the other genders into one value
    param:dataset: This function takes the dataset as  the input to clean the gender column
    return:This function returns the clean dataset after cleaning the gender column

    >>> sample_data2 = pd.DataFrame({'What is your gender?': ['Male','Female','female','FEMALE','Woman','woman','w','womail','W','Female'], 'User_Id': [1,2,3,4,5,6,7,8,9,10] })
    >>> ans = clean_gender(sample_data2)['Gender']
    >>> ans.to_list()
    ['Male', 'Female', 'Female', 'Female', 'Female', 'Female', 'Female', 'Female', 'Female', 'Female']

    """
    genderDistribution = dataframe.loc[:, dataframe.columns.str.contains('gender|Gender', regex=True)]
    nusers = dataframe.index
    dataframe['Gender'] = genderDistribution.apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
    dataframe.loc[dataframe['Gender'].str.contains(
        'Trans|them|trans|Undecided|Contextual|transgender|nb|unicorn|Unicorn|queer|NB|binary|Enby|Human|little|androgynous|Androgyne|Neutral|Agender|Androgynous|Androgynous|Fluid|GenderFluid|Genderflux|genderqueer|Genderqueer',
        regex=True), 'Gender'] = 'Undecided'
    dataframe.loc[dataframe['Gender'].str.contains(
        'Female|female|FEMALE|Woman|woman|w|womail|W|Cis female| Female (cis)|Cis Female|cis female|cis woman|F|f',
        regex=True), 'Gender'] = 'Female'
    cond1 = dataframe['Gender'] != 'Female'
    cond2 = dataframe['Gender'] != 'Undecided'
    dataframe.loc[cond1 & cond2, 'Gender'] = 'Male'
    dataframe.drop(genderDistribution, axis=1, inplace=True)
    dataframe.set_index('User_Id', inplace=True)

    return dataframe


def give_score(dataframe: pd.DataFrame)-> pd.DataFrame:
    """
    This function calculates the MH_Score for every user
    param:dataset The input is the dataframe
    
    >>> sample_data3 = pd.DataFrame({'Have you had a mental health disorder in the past?': ['Possibly', 'Rarely', 'Sometimes'], 'Do you think that team members/co-workers would view you more negatively if they knew you suffered from a mental health issue?':[ 'Yes,I think they would', 'Yes,I think they would', 'Yes,I think they would'], 'Do you think that team members/co-workers would view you more negatively if they knew you suffered from a mental health issue?':['Yes, they would', 'Yes, they would', 'Yes, they would'], 'Do you currently have a mental health disorder?':['Maybe', 'Possibly','Yes'], 'Have you had a mental health disorder in the past?' : ['Maybe','Yes', 'Maybe'], 'If you have a mental health issue, do you feel that it interferes with your work when being treated effectively?': ['Sometimes', 'Rarely', 'Rarely'], 'If you have a mental health issue, do you feel that it interferes with your work when NOT being treated effectively?':['Sometimes' ,'Rarely', 'Sometimes'], 'Do you have a family history of mental illness?':[ 'Yes', 'No', 'Yes'], 'How willing would you be to share with friends and family that you have a mental illness?':['Not open at all', 'Not open at all', 'Not open at all'],'If you have a mental health issue, do you feel that it interferes with your work when being treated effectively?':['Often', 'Often', 'Often'], 'If you have a mental health issue, do you feel that it interferes with your work when NOT being treated effectively?':['Often', 'Rarely', 'Mostly'],'Do you feel that being identified as a person with a mental health issue would hurt your career?':['Yes, I think it would', 'Yes, I think it would', 'Yes, I think it would'],'Do you feel that being identified as a person with a mental health issue would hurt your career?':['Yes, it has', 'Yes, it has', 'Yes, it has'],'Has your employer ever formally discussed mental health (for example, as part of a wellness campaign or other official communication)?':['Yes', 'No', 'Yes'] ,'Would you feel comfortable discussing a mental health disorder with your coworkers?':['Yes', 'Yes', 'No'], 'Have you ever sought treatment for a mental health issue from a mental health professional?': ['Yes', 'No', 'Maybe' ]})
    >>> give_score(sample_data3)['MH_Score'].iloc[2]
    30.0
    """
    nusers = len(dataframe.index)
    for userid in range(1, nusers + 1):

        df_user = dataframe[dataframe.index == userid]
        score = 0
        if df_user[
            'Do you think that team members/co-workers would view you more negatively if they knew you suffered from a mental health issue?'].values == 'Yes,I think they would' or \
                df_user[
                    'Do you think that team members/co-workers would view you more negatively if they knew you suffered from a mental health issue?'].values == 'Yes, they would' or \
                df_user['Do you currently have a mental health disorder?'].values == 'Maybe' or df_user[
            'Do you currently have a mental health disorder?'].values == 'Possibly' or df_user[
            'Have you ever sought treatment for a mental health issue from a mental health professional?'].values == '1' or \
                df_user['Have you had a mental health disorder in the past?'].values == 'Yes' or df_user[
            'Have you had a mental health disorder in the past?'].values == 'Possibly' or df_user[
            'Have you had a mental health disorder in the past?'].values == 'Maybe' or df_user[
            'If you have a mental health issue, do you feel that it interferes with your work when being treated effectively?'].values == 'Sometimes' or \
                df_user[
                    'If you have a mental health issue, do you feel that it interferes with your work when being treated effectively?'].values == 'Rarely' or \
                df_user[
                    'If you have a mental health issue, do you feel that it interferes with your work when NOT being treated effectively?'].values == 'Sometimes' or \
                df_user[
                    'If you have a mental health issue, do you feel that it interferes with your work when NOT being treated effectively?'].values == 'Rarely':
            score += 10
        if df_user['Do you have a family history of mental illness?'].values == 'Yes' or df_user[
            'How willing would you be to share with friends and family that you have a mental illness?'].values == 'Not open at all' or \
                df_user['Do you currently have a mental health disorder?'].values == 'Yes' or df_user[
            'If you have a mental health issue, do you feel that it interferes with your work when being treated effectively?'].values == 'Often' or \
                df_user[
                    'If you have a mental health issue, do you feel that it interferes with your work when NOT being treated effectively?'].values == 'Often' or \
                df_user[
                    'Do you feel that being identified as a person with a mental health issue would hurt your career?'].values == 'Yes, I think it would' or \
                df_user[
                    'Do you feel that being identified as a person with a mental health issue would hurt your career?'].values == 'Yes, it has':
            score += 15
        if df_user[
            'Has your employer ever formally discussed mental health (for example, as part of a wellness campaign or other official communication)?'].values == 'Yes' or \
                df_user[
                    'Would you feel comfortable discussing a mental health disorder with your coworkers?'].values == 'Yes':
            score += 5
        dataframe.loc[dataframe.index == userid, ['MH_Score']] = score

    return dataframe


def hypo1(df: pd.DataFrame, column_name: str):
    df['CompanySize'].value_counts()
    value_count = round(df.groupby(column_name)['MH_Score'].mean(),2)
    crossTab = pd.crosstab(df[column_name], df['MH_Score'],
                           normalize = "index")
    crossTab.columns.name = (column_name  + " vs MH Score")
    display(crossTab)
    fig, ax = plt.subplots(figsize=(10,6))
    cats_vals = [value_count[2],value_count[0],value_count[3],value_count[1]]
    cats = [value_count.index[2],value_count.index[0],value_count.index[3],value_count.index[1]]
    plt.plot(cats, cats_vals)
    plt.xlabel(column_name)
    plt.ylabel("MH_Score (avg)")
    plt.show()


def hypo2(df: pd.DataFrame, col1: str, col2: str):
    crossTab = pd.crosstab(df[col1],df[col2],
                       normalize = "index")
    crossTab.columns.name = "Mental Health discussion with Supervisor"
    display(crossTab)
    crossTab.plot(kind="bar",stacked=True, figsize=(10,5))
    plt.title( "Company vs Mental Health discussion with Supervisor")
    plt.xlabel('CompanySize')
    plt.ylabel('Discussing mental health disorder with Supervisor')


def hypo3(df: pd.DataFrame, col1: str):
    bins = [18, 30, 40, 50, 60, 70]
    labels = ['18-29', '30-39', '40-49', '50-59', '60-75']
    age=df['What is your age?']
    df['agerange'] = pd.cut(age, bins, labels = labels,include_lowest = True)
    crossTab = pd.crosstab(df['agerange'],df[col1],
                           normalize = "index")
    crossTab.columns.name = 'Discuss Mental Health with supervisor'
    display(crossTab)

    crossTab.plot(kind="bar", stacked=True, figsize=(10,5))
    plt.title( "Age vs Mental Health discussion with Supervisor")
    plt.xlabel('Age')
    plt.ylabel('Discussing mental health disorder with Supervisor')


def scatter_plot(dataframe: pd.DataFrame, x: int, y: int, color, size, hover_name, log_x, size_max):
    fig = px.scatter(dataframe, x=x, y=y,
                     color=color, size=size,
                     hover_name=hover_name, log_x=log_x, size_max=size_max)

    return fig


def hypo4b(hdf1: pd.DataFrame, hdf2: pd.DataFrame, hdf3: pd.DataFrame, hdf4: pd.DataFrame):
    fig =make_subplots(rows=2, cols=2,
                        specs=[[{"secondary_y": True}, {"secondary_y": True}],
                               [{"secondary_y": True}, {"secondary_y": True}]])
    # Top left
    fig.add_trace(
        go.Scatter(x=hdf1['Year'], y=hdf1['Health Expenditure'], name="Health Expenditure of UK"),
        row=1, col=1, secondary_y=False)

    fig.add_trace(
        go.Scatter(x=hdf1['Year'], y=hdf1['Expentancy'], name="Health Expentancy of UK"),
        row=1, col=1, secondary_y=True,
    )

    # Top right
    fig.add_trace(
        go.Scatter(x=hdf2['Year'], y=hdf2['Health Expenditure'], name="Health Expenditure of Australia"),
        row=1, col=2, secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=hdf2['Year'], y=hdf2['Expentancy'], name="Health Expentancy of Australia"),
        row=1, col=2, secondary_y=True,
    )

    # Bottom left
    fig.add_trace(
        go.Scatter(x=hdf3['Year'], y=hdf3['Health Expenditure'], name="Health Expenditure of Netherland"),
        row=2, col=1, secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=hdf3['Year'], y=hdf3['Expentancy'], name="Health Expentancy of Netherland"),
        row=2, col=1, secondary_y=True,
    )

    # Bottom right
    fig.add_trace(
        go.Scatter(x=hdf4['Year'], y=hdf4['Health Expenditure'], name="Health Expenditure of Switzerland"),
        row=2, col=2, secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=hdf4['Year'], y=hdf4['Expentancy'], name="Health Expentancy of Switzerland"),
        row=2, col=2, secondary_y=True,
    )

    fig.show()