import requests
from bs4 import BeautifulSoup
import pandas as pd

df = pd.DataFrame(columns=['link'])


laptop_data=pd.read_csv('laptop_link.csv')
num=0

df2 = pd.DataFrame(columns=['link','img','brand','name','price','discount_price','Color','SSD','RAM','Operating_System','Screen_Size',
'Disk_Drive','Warranty Summary','rating_performance','rating_battery','rating_desing','rating_display',
'rating','count_rating','count_review'])
#'
for link in laptop_data['link']:
    url='https://www.flipkart.com'+link
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
    webpage=requests.get(url,headers=headers).text
    soup=BeautifulSoup(webpage,"html.parser")
    try:
        #name
        for i in soup.find_all('h1',{'class':"yhB1nd"}):
            name=i.text.strip()
        brand = (name.split())[0]
        
        #image
        for item in soup.find_all('img',{'class':"_396cs4 _2amPTt _3qGmMb"}):
            img=item['src']

        #price
        for i in soup.find_all('div',{'class':"_3I9_wc _2p6lqe"}):
            price=str(i.text.strip())
        # price=price.replace(",", "")
        # price=int(price.replace("₹", ""))

        #DiscountPrice
        for i in soup.find_all('div',{'class':"_30jeq3 _16Jk6d"}):
            discount_price=i.text.strip()
        # discount_price=discount_price.replace(",", "")
        # discount_price=int(discount_price.replace("₹", ""))
        
        #feature
        feature=[]
        for i in soup.find_all('li',{'class':"_21lJbe"}):
        #     print(i.text.strip())
            feature.append(i.text.strip())

        #featureName
        featurename=[]
        for i in soup.find_all('td',{'class':"_1hKmbr col col-3-12"}):
        #     print(i.text.strip())
            featurename.append(i.text.strip())
            
        fes = dict(zip(featurename,feature))

        #rating
        for i in soup.find_all('div',{'class':"gUuXy- _16VRIQ"}):
            x=i.text.strip()

        data_name =['rating','count_rating','count_review']
        data=[]

        y=(x.split('&'))[1]
        count_review= [int(i) for i in y.split() if i.isdigit()]
        rating=((x.split())[0])[:3]
        count_rating = ((x.split())[0])[3:]
        
        data.append(float(rating))
        data.append(int(count_rating))
        data.append(count_review[0])

        product_rating = dict(zip(data_name,data))

        #rating_performance
        rating_performance=[]
        for i in soup.find_all('text',{'class':"_2Ix0io"}):
            rating_performance.append(i.text.strip())
            
        rating_performance_name=[]
        for i in soup.find_all('div',{'class':"_3npa3F"}):
            rating_performance_name.append(i.text.strip())
            
        rating_feature = dict(zip(rating_performance_name,rating_performance))

        #df1= pd.DataFrame({'link':link,,'price':price,'rating':rating[0:x],'processer':processer[0:x],'ram':ram[0:x],'os':os[0:x],'ssd':ssd[0:x],'display':display[0:x],'warrenty':Warranty[0:x]})
        df3 = pd.DataFrame({'link':url,'img':img,'brand':brand,'name':name,'price':price,'discount_price':discount_price,
        'Color':fes['Color'] if 'Color' in fes.keys() else 'Null','SSD':fes['SSD'] if 'SSD' in fes.keys() else 'Null',
        'RAM':fes['RAM'] if 'RAM' in fes.keys() else 'Null','Operating_System':fes['Operating System'] if 'Operating System' in fes.keys() else 'Null',
        'Screen_Size':fes['Screen Size'] if 'Screen Size' in fes.keys() else 'Null','Disk_Drive':fes['Disk Drive'] if 'Disk Drive' in fes.keys() else 'Null',
        'Warranty_Summary':fes['Warranty Summary'] if 'Warranty Summary' in fes.keys() else 'Null',
        'rating_performance':rating_feature['Performance'] if 'Performance' in rating_feature.keys() else 'Null' ,
        'rating_battery':rating_feature['Battery'] if 'Battery' in rating_feature.keys() else 'Null',
        'rating_desing':rating_feature['Design'] if 'Design' in rating_feature.keys() else 'Null',
        'rating_display':rating_feature['Display'] if 'Display' in rating_feature.keys() else 'Null',
        'rating':product_rating['rating'] if 'rating' in product_rating.keys() else 'Null',
        'count_rating':product_rating['count_rating'] if 'count_rating' in product_rating.keys() else 'Null',
        'count_review':product_rating['count_review'] if 'count_review' in product_rating.keys() else 'Null'},index=[0])

        print("new line")
        num=num+1
        print(num)
        frames = [df2, df3]
        df2 = pd.concat(frames,ignore_index=True,axis=0)
        
    except:
        pass
print(df2)
df2.to_csv('laptop_data.csv',index=False)


