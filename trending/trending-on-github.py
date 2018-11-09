import requests
import json


# to add search filters on the requested query
def filters(search_filter, size_per_page, url):
    flag_for_search_filter = str(input("Do you want to add search filter ? Enter Y/N :"))
    if flag_for_search_filter.lower() == 'y':
        search_filter = str(input("Please enter a search filter :"))
    flag_for_page_limit = str(input("Do you want to add a limit on size ? Enter Y/N :"))
    if flag_for_page_limit.lower() == 'y':
        size_per_page = int(input("Please enter a size filter :"))
    print()
    url = 'https://api.github.com/search/repositories?q={query}{&page,per_page,sort,order}'
    if search_filter != "":
        url = 'https://api.github.com/search/repositories?q={' + search_filter + '}{&page,per_page,sort,order}'
    send_request(url, size_per_page)


# to send request to the github url
def send_request(url, size_per_page):
    r = requests.get(url)
    assert r.status_code == 200
    get_data(r, size_per_page)


# to attain the requested repository data
def get_data(r, size_per_page):
    star_watch_count = {}
    json_data = json.loads(r.content)
    items_json = json_data['items']
    og_star_count = 0
    og_watcher_count = 0

    for each_item in items_json:
        name = each_item['full_name']
        description = each_item['description']
        language = each_item['language']
        url = each_item['html_url']
        stars = each_item['stargazers_count']
        watchers = each_item['watchers']

        print("Name :", name)
        print("Description :", description)
        print("Language :", language)
        print("URL :", url)
        print("Stargazers :", stars)
        print()

        og_star_count += stars
        og_watcher_count += watchers

        if name not in star_watch_count:
            star_watch_count[name] = [stars, watchers]
        else:
            given_stars = star_watch_count[name][0]
            given_watchers = star_watch_count[name][1]
            new_count_stars = given_stars + stars
            new_count_watchers = given_watchers + watchers
            star_watch_count[name] = [new_count_stars, new_count_watchers]
        if size_per_page == len(star_watch_count):
            break

    print("Watchers count overall :", og_watcher_count)
    print("Starts count overall : ", og_star_count)
    print("Page length : ", len(star_watch_count))


def main():
    search_filter = ""
    size_per_page = ""
    url = ""
    filters(search_filter, size_per_page, url)


if __name__ == "__main__":
    main()
