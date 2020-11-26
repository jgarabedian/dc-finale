from pymongo import MongoClient
from bson.objectid import ObjectId
from pprint import pprint
import os
from dotenv import load_dotenv
load_dotenv()

DB_PWD = os.getenv("DB_PWD")
client = MongoClient(
    f"mongodb+srv://jgarabedian:{DB_PWD}@jackworkspace.djiex.mongodb.net/dcfinale?retryWrites=true&w=majority")
db = client.dcfinale
collection = db.activities


def get_completed_activities():
    return collection.find({'date': {'$ne': ''}})


def get_activities():
    return collection.find()


def get_activity(act_id):
    return collection.find_one({'_id': ObjectId(act_id)})


def del_activity(act_id):
    return collection.delete_one({'_id': ObjectId(act_id)})


def insert_activity(form):
    friends = form['act_friends'].split(',')
    activity = {
        'name': form['act_name'],
        'date': form['act_date'],
        'location': form['act_location'],
        'address': form['act_address'],
        'friends': friends,
        'notes': form['act_notes'],
        'category': form['act_category']
    }
    collection.insert_one(activity)
    return


def update_activity(act_id, form):
    filter_id = {'_id': ObjectId(act_id)}
    friends = form['act_friends'].split(',')
    new_vals = {
        'name': form['act_name'],
        'date': form['act_date'],
        'location': form['act_location'],
        'address': form['act_address'],
        'friends': friends,
        'notes': form['act_notes'],
        'category': form['act_category']
    }
    collection.update_one(filter_id, {'$set': new_vals})


def test():
    activity = {
        'name': 'Armenian Dinner',
        'date': '2020-12-05',
        'location': 'My House',
        'address': '930 M St',
        'friends': ['Tim', 'Angelo', 'Andrea']
    }
    # result = db.activities.insert_one(activity)
    # pprint(result.inserted_id)
    all_activities = get_activities()

    filter_val = {'_id': all_activities[0].get('_id')}
    new_val = {'$set': {'date': ''}}

    # update the value
    # collection.update_one(filter_val, new_val)

    pprint(get_activities()[0])

    # pprint(all_activities[0].get('_id'))


