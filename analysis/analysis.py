from pytz import utc
import justpy as jp
import pandas as pd

df = pd.read_csv("data/AAPL.csv", parse_dates=['Date'])
df['Month'] = df['Date'].dt.strftime("%Y-%m")
df_mon = df.groupby(['Month']).mean()

aapl_chart = '''
{
    chart: {
        type: 'spline',
        inverted: false
    },
    title: {
        text: 'AAPL Stock Price Variation'
    },
    subtitle: {
        text: 'Based on Historical Data from 1998'
    },
    xAxis: {
        reversed: false,
        title: {
            enabled: true,
            text: 'Month'
        },
        labels: {
            format: '{value}'
        },
        accessibility: {
            rangeDescription: 'Range: 0 to 80 km.'
        },
        maxPadding: 0.05,
        showLastLabel: true
    },
    yAxis: {
        title: {
            text: 'Stock Price'
        },
        labels: {
            format: '{value}'
        },
        accessibility: {
            rangeDescription: 'Range: -90°C to 20°C.'
        },
        lineWidth: 2
    },
    legend: {
        enabled: false
    },
    tooltip: {
        headerFormat: '<b>{series.name}</b><br/>',
        pointFormat: '{point.x} : {point.y}'
    },
    plotOptions: {
        spline: {
            marker: {
                enable: false
            }
        }
    },
    series: [{
        name: 'Stock Price',
        data: [[0, 15], [10, -50], [20, -56.5], [30, -46.5], [40, -22.1],
            [50, -2.5], [60, -27.7], [70, -55.7], [80, -76.5]]
    }]
}
'''

def app():
    wp = jp.QuasarPage(dark=True)
    hc1 = jp.HighCharts(a=wp, options=aapl_chart)
    hc1.options.xAxis.categories = list(df_mon.index)
    hc1.options.series[0].data = list(df_mon["High"])

    return wp

jp.justpy(app)