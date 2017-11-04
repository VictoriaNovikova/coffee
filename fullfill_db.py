import requests
import json
from db import Cafe, db_session, Tag, TagsForCafe

api_key='AIzaSyAsXD-BYYqu4ImlaIrfcSuzl-13rwyaiOA'

def get_cafe_json(lat, lng):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={api_key}&location={lat},{lng}&radius=500&type=cafe".format(api_key=api_key, lat=lat, lng=lng)    
    result = requests.get(url)
    if result.status_code == 200:
        return result.json()
    else:
        print("Something went wrong...")

def get_nearest_cafe(lat, lng):    
    geo_json = get_cafe_json(lat, lng)
    if not geo_json:
        return
    cafes = []
    tags_and_cafes = {}
    for data in geo_json.get('results'):
        cafe = Cafe(name=data['name'], lat=data['geometry']['location']['lat'], lng=data['geometry']['location']['lng'], rating=data.get('rating'), address=data['vicinity'])        
        saved_cafe = Cafe.query.filter(Cafe.lat == cafe.lat and Cafe.lng == cafe.lng).first()
        
        if saved_cafe:
            cafe = saved_cafe
        else:
            db_session.add(cafe)
            db_session.commit()

        cafes.append(cafe)
        for type_name in data.get('types'):
            tags_and_cafes.setdefault(type_name, [])
            tags_and_cafes[type_name].append(cafe.id)         

    for tag_name in tags_and_cafes.keys():
        tag = Tag(tag_name=tag_name, localized_name='')
        db_session.add(tag)
        db_session.commit()
        for cafe_id in tags_and_cafes[tag_name]:        
            tag_to_add = TagsForCafe(tag_id=tag.id, cafe_id=cafe_id)
            db_session.add(tag_to_add)

    db_session.commit()
    return cafes


