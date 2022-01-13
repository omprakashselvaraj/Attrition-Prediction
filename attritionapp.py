from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd
import pygal

model = pickle.load(open('attr.pkl', 'rb'))
standard = pickle.load(open('ssc.pkl', 'rb'))
app=Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/render')
def render():
    return render_template('input.html')

@app.route('/input', methods=['POST','GET'])
def input():
    #if request.method=="POST":
    msg=""
    detail=request.form
    age=detail['age']
    distance=detail['distance']
    es=detail['es']
    ji=detail['ji']
    jl=detail['joblevel']
    js=detail['js']
    income=detail['income']
    stock=detail['stock']
    twy=detail['twy']
    yac=detail['yac']
    ycr=detail['ycr']
    ycm=detail['ycm']
    mstatus=int(detail['mstatus'])
    ot=int(detail['ot'])
    at=[age,distance,es,ji,jl,js,income,stock,twy,yac,ycr,ycm]
    print(at)
    at=standard.fit_transform([at])
    arr=[]
    for i in at[0]:
        arr.append(i)
    arr.append(mstatus)
    arr.append(ot)
    print(arr)
    prediction=model.predict([arr])
    if prediction==0:
        msg="The eomployee will stay in the company 😁"
    else:
        msg="The employee will leave the company 🙁 "

    data=pd.read_csv("new.csv")
    a=list(data.groupby('Department')['PerformanceRating'].mean())

    bar_chart = pygal.Bar(height=400)
# naming the title
    bar_chart.title = 'ratings'

    bar_chart.add('HR', a[0])
    bar_chart.add('R and D', a[1])
    bar_chart.add('Sales', a[2])

    bar_chart = bar_chart.render_data_uri() 

    c=list(data.groupby('Attrition')['Age'].mean())
    chart = pygal.Bar(height=400)
    chart.title = 'Attrition vs age'
    chart.add('No', c[0])
    chart.add('Yes', c[1])
    chart1 = chart.render_data_uri() 
    
    html = render_template(
    'output.html',
    msg=msg,
    chart=bar_chart,
    chart1=chart1
    
)
    return (html)

      







@app.route('/')
def submit():
    return render_template('input.html')

if __name__ == '__main__':
    app.run(debug=True)