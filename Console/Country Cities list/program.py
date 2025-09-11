import pycountry
import geonamescache
import uuid

def create_guid():
    return str(uuid.uuid4())

def get_cities_by_country(country_name: str):
    gc = geonamescache.GeonamesCache()
    cities = gc.get_cities()

    # Normalize input (case-insensitive)
    country_name = country_name.strip().lower()

    # Find country by name
    country = None
    for c in pycountry.countries:
        if c.name.lower() == country_name or country_name in [c.alpha_2.lower(), c.alpha_3.lower()]:
            country = c
            break

    if not country:
        # return f"❌ Country '{country_name}' not found."
        raise Exception("❌ Country '{country_name}' not found.")

    country_cities = [city['name'] for city in cities.values() if city['countrycode'] == country.alpha_2]

    if not country_cities:
        # return f"ℹ️ No cities found for {country.name}."
        raise Exception("ℹ️ No cities found for {country.name}.")

    return sorted(set(country_cities))

get_countries = lambda : [country.name for country in pycountry.countries]

def get_cities_JSON(country: str, limit: int = 20) -> str:
    cities: list[str] = get_cities_by_country(country)
    json: list[str] = []
    country_id = create_guid()

    for city in cities[:limit]:
        json.append('{' + f'"id":"{create_guid()}","name":"{city}","countryId":"{country_id}"' + '}')

    head: str = f'"id":"{country_id}","name":"{country.capitalize()}","cities":'

    return '{' + head + '[' + ','.join(json) + ']' + '}'


if __name__ == "__main__":
    # country_input = input("Enter a country name: ")
    # result = get_cities_by_country(country_input)
    #
    # if isinstance(result, list):
    #     print(f"Cities in {country_input.title()}:")
    #     for city in result[:50]:  # showing first 50 to avoid huge output
    #         print("-", city)
    # else:
    #     print(result)
    # print(type(get_countries()))
    visited: list[str] = ['australia', 'afghanistan', 'aruba', 'angola', 'anguilla', 'åland islands', 'australia', 'afghanistan', 'aruba', 'angola', 'anguilla', 'åland islands', 'albania', 'andorra', 'united arab emirates', 'argentina', 'armenia', 'american samoa', 'french southern territories', 'antigua and barbuda', 'austria', 'azerbaijan', 'burundi', 'belgium', 'benin', 'bonaire, sint eustatius and saba', 'burkina faso', 'bangladesh', 'bulgaria', 'bahrain', 'bahamas', 'bosnia and herzegovina', 'saint barthélemy', 'belarus', 'belize', 'bermuda', 'bolivia, plurinational state of', 'brazil', 'barbados', 'brunei darussalam', 'bhutan', 'botswana', 'central african republic', 'canada', 'cocos (keeling) islands', 'switzerland', 'chile', 'china', "côte d'ivoire", 'cameroon', 'congo, the democratic republic of the', 'congo', 'cook islands', 'colombia']

    json: list[str] = []
    print("fetching...")
    for country in get_countries():
        if country.lower() not in visited:
            try:
                json.append(get_cities_JSON(country))
                # visited.append(country.lower())
            except Exception:
                continue
    print('{"countries":[' + ",".join(json) + "]}")
    # print()
    # print(visited)
    # print(len(get_countries()))

# ---------------------------------------------------------------------------------------------------------------------
# from geopy.geocoders import Nominatim
#
#
# def get_major_cities(country_name: str, limit=20):
#     geolocator = Nominatim(user_agent="city_finder")
#     country = geolocator.geocode(country_name, exactly_one=True, addressdetails=True)
#
#     if not country:
#         return f"❌ Country '{country_name}' not found."
#
#     # Search for cities in the country
#     cities = geolocator.geocode(
#         f"cities in {country_name}",
#         exactly_one=False,
#         limit=limit
#     )
#
#     if not cities:
#         return f"ℹ️ No cities found for {country_name}."
#
#     return [c.address.split(",")[0] for c in cities]
#
#
# if __name__ == "__main__":
#     country_input = input("Enter a country name: ")
#     result = get_major_cities(country_input, limit=20)  # Top 20 cities
#
#     if isinstance(result, list):
#         print(f"Major Cities in {country_input.title()}:")
#         for city in result:
#             print("-", city)
#     else:
#         print(result)
