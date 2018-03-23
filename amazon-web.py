from flask import Flask, request, render_template,url_for, redirect,session
from werkzeug.utils import secure_filename
from clarifai import rest
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection as Finding
import sys,os

app = Flask(__name__)
appc = ClarifaiApp(api_key='a4a9d232e05d450297270d8a770b2610')
api = Finding(appid="sharmas-omair-PRD-4132041a0-7912df0b", config_file=None)


@app.route('/', methods=['POST', 'GET'])
def play():
    if request.method == 'GET':
        return render_template('play.html')
    elif request.method == 'POST':
	model = appc.models.get('apparel')
        img=request.form['img']
	if img:
		clari=model.predict_by_url(url=img)
        else:
	        fimg=request.files['imgup']
		fimg.save('./'+secure_filename(fimg.filename))
		image = ClImage(file_obj=open(fimg.filename, 'rb'))
		clari=model.predict([image])
	global key		
	key=clari['outputs'][0]['data']['concepts'][0]['name']
   	return redirect(url_for('ebay'))

@app.route('/ebay', methods=['POST', 'GET'])
def ebay():
    if request.method == 'GET':	
	response = api.execute('findItemsAdvanced', {'keywords': key,'itemFilter': [{'name': 'Condition','value': 'New'},{'name': 'LocatedIn','value': 'CA'},{'name': 'globalId','value': 'EBAY-CA'} ]})
	c=response.dict()
	name=[]
	cate=[]
	price=[]
	rating=[]
	delhi=[]
	reid=[]
	for i in range(0,10):
		name.append(c['searchResult']['item'][i]['title'])
		cate.append(c['searchResult']['item'][i]['primaryCategory']['categoryName'])
		price.append(c['searchResult']['item'][i]['sellingStatus']['currentPrice']['value'])
		rating.append(c['searchResult']['item'][i]['paymentMethod'])
		delhi.append(c['searchResult']['item'][i]['shippingInfo']['oneDayShippingAvailable'])
		reid.append(c['searchResult']['item'][i]['viewItemURL'])
	kwargs={
		'name0': name[0],'name1': name[1],'name2': name[2],'name3': name[3],'name4': name[4],
		'cuisines0':cate[0],'cuisines1':cate[1],'cuisines2':cate[2],'cuisines3':cate[3],'cuisines4':cate[4],
		'cost0':price[0],'cost1':price[1],'cost2':price[2],'cost3':price[3],'cost4':price[4],
		'rate0':rating[0],'rate1':rating[1],'rate2':rating[2],'rate3':rating[3],'rate4':rating[4],
		'delivery0':delhi[0],'delivery1':delhi[1],'delivery2':delhi[2],'delivery3':delhi[3],'delivery4':delhi[4],
		'id0':reid[0],'id1':reid[2],'id2':reid[2],'id3':reid[3],'id4':reid[4],'name5':name[5],'name6':name[6],'name7':name[7],'name8':name[8],'name9':name[9],		'cuisines5':cate[5],'cuisines6':cate[6],'cuisines7':cate[7],'cuisines8':cate[8],'cuisines9':cate[9],
		'cost5':price[5],'cost6':price[6],'cost7':price[7],'cost8':price[8],'cost9':price[9],
		'rate5':rating[5],'rate6':rating[6],'rate7':rating[7],'rate8':rating[8],'rate9':rating[9],
		'delivery5':delhi[5],'delivery6':delhi[6],'delivery7':delhi[7],'delivery8':delhi[8],'delivery9':delhi[9],
		'id5':reid[5],'id6':reid[6],'id7':reid[7],'id8':reid[8],'id9':reid[9],
		}
	return render_template('result.html',**kwargs)
    elif request.method == 'POST':
	return redirect(url_for('play'))


if __name__ == '__main__':
    app.debug = True
    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get('PORT', 2580))
    app.run(host=host, port=port)
