from bs4 import BeautifulSoup
from recipe_to_file import save_recipe
import urllib

# Base URL
baseURL = "http://www.foodnetwork.com"
recipeURL = "http://www.foodnetwork.com/recipes/a-z.html"


def parse_recipe(recipe_link):
    """Function is passed a recipe URL. Proceeds to parse all recipe data and save to dictionary"""
    html_2 = urllib.urlopen(baseURL+recipe_link)
    soup_2 = BeautifulSoup(html_2, "lxml")

    # Get image if available, if not skip recipe
    # get_image_parent = soup_2.find_all("div", {"class": "photo-video"})
    child = ""
    for child in soup_2.find_all("div", {"class": "photo-video"}):
        for image in child.find_all("img"):
            # print image['src']
            image_src = str(image['src'])
            # Don't save recipes without pictures TODO: Still not detecting empty pictures. Try: .isEmpty() ?

    if child is None or child == '':
        # print "no img"
        return None

    # Get recipe name
    name = soup_2.find("h1", {"itemprop": "name"})
    if name is not None:
        name = name.text
    else:
        return None

    # Get all ingredients
    ingredients = soup_2.find_all("li", {"itemprop": "ingredients"})
    ingredient_list = []
    if ingredients is not None:
        for i in ingredients:
            ingredient_list.append(i.text)
    else:
        return None

    # Get directions
    directions = soup_2.find_all("ul", {"class": "recipe-directions-list"})
    directions_list = []
    if directions is not None:
        for step in directions:
            #print step
            directions_list.append(str(step))
    else:
        return None

    # Create recipe structure
    new_recipe = {'name': name, 'ingredients': ingredient_list, 'directions': directions_list, 'img_src': image_src}

    return new_recipe
    # save_recipe(new_recipe)


if __name__ == "__main__":
    # Recipe list
    recipe_list = []

    # Get HTML code [Main Page]
    html = urllib.urlopen(recipeURL)

    # Feed it to Beautifulsoup
    soup = BeautifulSoup(html, "lxml")

    # Find letter buttons
    letters = soup.find("section", {"class": "a-to-z-btns"}).find("ul").find_all("a")

    # Counter
    counter = 0
    for letter in letters:

        # Get HTML code [Main Page]
        html = urllib.urlopen(baseURL+letter['href'])

        # Feed it to Beautifulsoup
        soup = BeautifulSoup(html, "lxml")

        # For letter A, find all A recipe pages [main + all next pages]
        href = soup.find("a", {"class": "btn fig right"})
        href = href['href']

        # Init list with main letter page
        href_list = [letter['href']]
        while True:
            # print "enter:", href
            html3 = urllib.urlopen(baseURL + href)
            soup3 = BeautifulSoup(html3, "lxml")
            next_pages = soup3.find("a", {"class": "btn fig right"})

            # No more Next pages
            if next_pages is None:
                break

            href = next_pages['href']
            href_list += [href]

        i = 0
        for recipe_page in href_list:
            print "Recipe page:", recipe_page
            # Get HTML of each page and feed it to bsoup
            letter_recipe_page = urllib.urlopen(baseURL+recipe_page)
            soup2 = BeautifulSoup(letter_recipe_page, 'lxml')

            # Recipe links are items in a list (li), and that have class col18
            recipe_links = soup2.find_all("li", {"class": "col18"})

            # Go thru all recipes and save them
            for recipe in recipe_links:
                # List of all links to recipes
                link = recipe.find("a")

                result = parse_recipe(link['href'])

                if result is not None:
                    recipe_list.append(result)
                    i += 1
                    counter += 1

                # Prints name of recipe + URL
                # print "Recipe:", link.text, " URL:", link["href"]

                if i > 10:
                    print counter, " recipes"
                    save_recipe(recipe_list)
                    recipe_list = []
                    i = 0

