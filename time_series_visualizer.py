import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
import calendar
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", 
                sep=",",
                header=0)
df.set_index('date', inplace=True)
df.index = pd.to_datetime(df.index)
df = df[(df['value'] >= df['value'].quantile(0.025)) &  # Removes data if page views are in bottom 2.5%
        (df['value'] <= df['value'].quantile(0.975))]   # Removes data if page views are in top 2.5%

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(15, 7))
    # Date is now an index so has to be accessed differently.
    ax.plot(df.index, df['value'])
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Creates new dataset, with indexs renamed to 'year' and 'month' - Avoids duplicate date names.
    df_bar = df.groupby([df.index.year.rename('year'), df.index.month.rename('month')])['value'].mean()
    # Returns df without indexing with column names year,month and pagecounts
    df_bar = df_bar.reset_index()
    df_bar.columns = ['year', 'month', 'value']

    ### Series and dictionary to set label order and map '1' -> 'January etc.
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    month_dict = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April',
    5: 'May', 6: 'June', 7: 'July', 8: 'August',
    9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    # Mapping '1' -> 'January', etc.
    df_bar['month'] = df_bar['month'].map(month_dict)
    print(df_bar.head(10))

    # PIVOT the data so months become columns
    df_pivot = df_bar.pivot(index='year', columns='month', values='value')
    df_pivot = df_pivot[months]  # Reorder columns to match month order

    # Next quesiton suggests seaborn, this one didn't therefore plot (I tried sns and I believe FCC tests)
    fig, ax = plt.subplots(figsize=(15, 7))
    df_pivot.plot(kind='bar', ax=ax)

    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    ax.legend(title="Months")

    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)

    fig, axes = plt.subplots(ncols = 2, figsize=(20, 7))
    sns.boxplot(data = df_box, x = 'year', y = 'value', ax = axes[0])
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")
    axes[0].set_title("Year-wise Box Plot (Trend)")

    boxplot_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    sns.boxplot(data = df_box, x = 'month', y = 'value', ax = axes[1], order = boxplot_order)
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
