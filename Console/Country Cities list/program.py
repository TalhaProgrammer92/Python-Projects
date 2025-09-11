import pycountry
import geonamescache
import uuid
from phonenumbers import country_code_for_region


def get_country_dialing_code(country_name: str):
    import pycountry

    # normalize input
    country_name = country_name.strip().lower()

    # find country from pycountry
    country = None
    for c in pycountry.countries:
        if c.name.lower() == country_name or country_name in [c.alpha_2.lower(), c.alpha_3.lower()]:
            country = c
            break

    if not country:
        return f"❌ Country '{country_name}' not found."

    # get phone code using alpha_2 code
    dial_code = country_code_for_region(country.alpha_2)

    if dial_code == 0:
        return f"ℹ️ No dialing code found for {country.name}."

    return f"+{dial_code}"


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

def get_cities_JSON(country: str) -> str:
    cities: list[str] = get_cities_by_country(country)
    json: list[str] = []
    country_id = create_guid()

    for city in cities:
        json.append('{' + f'"id":"{create_guid()}","name":"{city}","countryId":"{country_id}"' + '}')

    country_code: str | None = None
    try:
        country_code = get_country_dialing_code(country)
    except Exception:
        pass
    head: str = f'"id":"{country_id}","name":"{country.capitalize()}","code":null,"cities":' if country_code is None else f'"id":"{country_id}","name":"{country.capitalize()}","code":"{country_code}","cities":'

    return '{' + head + '[' + ','.join(json) + ']' + '}'


def main() -> str:
    json: list[str] = []
    print("fetching...")
    for country in get_countries():
        try:
            json.append(get_cities_JSON(country))
        except Exception:
            continue
    print("Done!")
    return '{"countries":[' + ",".join(json) + "]}"

if __name__ == "__main__":
    with open("json.txt", 'w', encoding="utf-8") as f:
        f.write(main())
