from flask import Flask, render_template, request
from flask_cors import CORS,cross_origin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import csv



app = Flask(__name__)

@app.route("/", methods = ['GET'])
@cross_origin()
def homepage():
    return render_template("index.html")

@app.route("/scrapper" , methods = ['POST' , 'GET'])
@cross_origin()
def scrapper():
    if request.method == 'POST':
        try:
            ## declaring url 
            url = request.form['content']

            ## starting chrome webdriver to navigate website
            driver = webdriver.Chrome()
            driver.maximize_window()
            
            ## getting url and putting time
            driver.get(f'{url}')
            time.sleep(5)

            ## creating empty list to store result data
            video_links = [][:5]
            image_url = [][:5]
            details = []


            ## finding elements required using BY module
            video_css = driver.find_elements(By.CSS_SELECTOR ,"div#content > ytd-rich-grid-media > div#dismissible > div#details > div#meta > h3 > a#video-title-link")
            image_css = driver.find_elements(By.CSS_SELECTOR ,"#thumbnail > yt-image > img")
            title_ID = driver.find_elements(By.ID,"video-title-link")
            views_xpath = driver.find_elements(By.XPATH,"//*[@id='metadata-line']/span[1]")
            upload_xpath = driver.find_elements(By.XPATH,"//*[@id='metadata-line']/span[2]")


            ## writing functions to extract data 
            ## for videos 
            for i in video_css:
                links = i.get_attribute('href')
                video_links.append(links)

            ## for images
            for item in image_css:
                src = item.get_attribute('src')
                image_url.append(src)

            ## for titles
            titles = list(map(lambda a : a.text, title_ID))[:5]

            ## for view count
            views = list(map(lambda a : a.text, views_xpath))[:5]

            ## for time of upload
            upload_time = list(map(lambda a : a.text, upload_xpath))[:5]
            
            ## closing the webdriver
            driver.close()
            
            ## iterating through eat list and appending to details variable
            for a,b,c,d,e in zip(titles,views,upload_time,video_links,image_url):
                ## creating a dictionary and storing data in order
                mydict = {'Title': a, 'Views': b, 'Uploaded': c, 'VideoLink': d, 'ThumbnailLink': e}

                ## using for loop to store 5 results in data
                details.append(mydict)
                details = list(details)
                

            ## storing results into a csv file 
            with open("data.csv",mode="w",newline='',encoding='UTF-8') as file:
                writer = csv.writer(file)
                writer.writerows(details)
        
            ## return render_template('result.html')
            return render_template('result.html', reviews=details)     

        except Exception as e:
            return 'something is wrong'
        
    else:
        return render_template('index.html')


if __name__=="__main__":
    app.run(host="0.0.0.0")
