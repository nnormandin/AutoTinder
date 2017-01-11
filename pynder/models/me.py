import dateutil.parser

from pynder.constants import UPDATABLE_FIELDS, GENDER_MAP_REVERSE, GENDER_MAP


class ProfileDescriptor(object):
    # this is a python descriptor that allows for
    # dynamic updating of profile data

    def __init__(self, id):
        self.id = id

    def __get__(self, instance, owner):
        if hasattr(self, 'value'):
            return self.value
        else:
            return instance._data[self.id]

    def __set__(self, instance, value):
        profile = {}
        for key in UPDATABLE_FIELDS:
            profile[key] = getattr(instance, key)
        profile['gender'] = GENDER_MAP_REVERSE[profile['gender']]
        profile['interested_in'] = [GENDER_MAP_REVERSE[x] for x in
                                    profile['interested_in']]
        profile[self.id] = value
        instance.__init__(instance._api.update_profile(profile), instance._api)
        self.value = value


class GenderDescriptor(ProfileDescriptor):
    # makes gender human readable

    def __get__(self, instance, owner):
        gender = super(GenderDescriptor, self).__get__(instance, owner)
        return GENDER_MAP[gender]

    def __set__(self, instance, value):
        gender = GENDER_MAP_REVERSE[value]
        return super(GenderDescriptor, self).__get__(instance, gender)


class InterestedInDescriptor(ProfileDescriptor):
    # makes gender human readable

    def __get__(self, instance, owner):
        interested_in = super(InterestedInDescriptor, self).\
            __get__(instance, owner)
        return map(lambda x: GENDER_MAP[x], interested_in)

    def __set__(self, instance, value):
        interested_in = map(lambda x: GENDER_MAP_REVERSE[x], value)
        return super(InterestedInDescriptor, self).\
            __get__(instance, interested_in)


class Profile(object):
    bio = ProfileDescriptor('bio')
    discoverable = ProfileDescriptor('discoverable')
    distance_filter = ProfileDescriptor('distance_filter')
    age_filter_min = ProfileDescriptor('age_filter_min')
    age_filter_max = ProfileDescriptor('age_filter_max')
    interested_in = InterestedInDescriptor('interested_in')
    gender = GenderDescriptor('gender')

    def __init__(self, data, api):
        self.id = data['_id']
        self._api = api
        self.create_date = data['create_date']
        self.photos = map(lambda photo: str(photo['url']), data['photos'])
        self.ping_time = data['ping_time']
        self.name = data['name']
        self.create_date = dateutil.parser.parse(self.create_date)
        self.banned = data['banned'] if "banned" in data else False
        self._data = data

    def __repr__(self):
        return self.name
