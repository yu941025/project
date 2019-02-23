__author__ = 'Administrator'
import eye_type

start_url='https://www.tianyancha.com/search/'
#city='杭州'

def get_url(city):
    url=[]
    city_type=eye_type.area_dict[city][0]

    for i in range(1,251):
        for type in eye_type.industry_dict.values():
            for price in eye_type.money_dict.values():
                for lianxi in eye_type.contact_dict.values():
                    for phone  in  eye_type.phone_dict.values():

                        for time in eye_type.time_dict.values():
                            a_url=start_url+type+'-'+price+'-'+lianxi+'-'+phone+"-"+time+'/p'+str(i)+'?'+'base=%s'%city_type
                            url.append(a_url)
    return url




