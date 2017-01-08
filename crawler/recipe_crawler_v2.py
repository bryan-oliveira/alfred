import urllib
from bs4 import BeautifulSoup
from app.database.recipes.recipe_to_file import save_recipe

"""
This module crawls the epicurious website, parses its recipes, and saves them locally.
"""

# Base URL
base = "http://www.epicurious.com"
baseURL = "http://www.epicurious.com/search/?content=recipe"
pageNumber = "&page="


def parse_recipe(url):
    """Function is passed a recipe URL. Proceeds to parse all recipe data and save to dictionary"""
    html = urllib.urlopen(base + url)  # Acutal page

    # Chef's note
    # html = urllib.urlopen("http://www.epicurious.com/recipes/food/views/carrot-tart-with-ricotta-and-almond-filling")
    # Ingredient Sub lists
    # html = urllib.urlopen("http://www.epicurious.com/recipes/food/views/gluten-free-cauliflower-pizza-with-mozzarella-kale-and-lemon")
    # Preparation Sub lists
    # html = urllib.urlopen("http://www.epicurious.com/recipes/food/views/creme-fraiche-potato-salad-with-salmon-roe-green-cabbage-slaw-and-smoked-salmon")

    soup = BeautifulSoup(html, "lxml")

    imgDiv = soup.find("div", {"class": "recipe-image"})

    # Get image if available, if not skip recipe
    if imgDiv is None:
        return False

    imgTag = imgDiv.find("img", {"class": "photo"})

    # Img url; Set url to get biggest img size available; Strip leading //
    imgURL = imgTag['data-srcset'].replace("w_274%2Ch_169", "w_620%2Ch_413")[2:]
    # print "imgURL:", imgURL

    # Get nutritional info, if not skip recipe
    nutritionDiv = soup.find("div", {"class": "nutrition content"})

    if nutritionDiv is None:
        return False

    nutritionInfo = []
    nutritionPair = {}
    nutritionDiv = nutritionDiv.find_all("li")
    for item in nutritionDiv:
        tag = item.find("span").string

        if tag is None:  # Discard empty formatting tags
            break

        value = tag.next_element.string

        nutritionPair[tag] = value
    nutritionInfo.append(nutritionPair)
    # print "nutritionInfo:", nutritionInfo


    # Get title
    titleDiv = soup.find("div", {"class": "title-source"})
    if titleDiv is None:
        return False
    title = titleDiv.find("h1").string
    if title is None:
        return False  # Bug. With above check, ome recipes still don't have a title
    # print "title:", title

    # Get description
    descriptionDiv = soup.find("div", {"class": "dek"})
    description = "None"
    if descriptionDiv is not None:
        description = descriptionDiv.string
    # print "description:", description.string

    # Get Yield
    yieldDiv = soup.find("dd", {"class": "yield"})
    yield_ = "None"
    if yieldDiv:
        yield_ = yieldDiv.string
    # print "yield_:", yield_

    # Get Active Time
    activeTimeDiv = soup.find("dd", {"class": "active-time"})
    activeTime = "None"
    if activeTimeDiv:
        activeTime = activeTimeDiv.string
    # print "activeTime:", activeTime

    # Get Total Time
    totalTimeDiv = soup.find("dd", {"class": "total-time"})
    totalTime = "None"
    if totalTimeDiv:
        totalTime = totalTimeDiv.string
    # print "totalTime:", totalTime

    # Get ingredient list
    ingredientDiv = soup.find_all("ul", {"class": "ingredients"})
    if ingredientDiv is None:
        return False
    ingredientlist = {}
    for subList in ingredientDiv:
        ings = []

        # Get title of sub list of ingredients if available Ex: 1: For the topping; 2: For the cake
        ingTitle = subList.previous_sibling
        if ingTitle is None:
            ingTitle = "None"
        else:
            ingTitle = ingTitle.string

        # Get ingredient items
        for items in subList:
            # print items.text
            ings.append(items.text)

            ingredientlist[ingTitle] = ings
    # print "finalIngList:", finalIngList

    # Get Preparation
    preparationDiv = soup.find_all("ol", {"class": "preparation-steps"})
    preparationSteps = {}
    if preparationDiv:
        for subList in preparationDiv:
            stepList = []

            stepTitle = subList.previous_sibling

            if stepTitle is not None:
                stepTitle = stepTitle.string
            else:
                stepTitle = "None"

            for steps in subList.stripped_strings:
                stepList.append(steps)

            preparationSteps[stepTitle] = stepList
    # print "preparationSteps:", preparationSteps

    # Get Chef notes
    chefNotesDiv = soup.find("div", {"class": "chef-notes-content"})
    chefNotes = "None"
    if chefNotesDiv is not None:
        chefNotes = chefNotesDiv.string
    # print "chefNotes:", chefNotes

    # Get tags
    tagListDiv = soup.find_all("dt", {"itemprop": "recipeCategory"})
    tagList = []
    for tag in tagListDiv:
        tagList.append(tag.string)
    # print "tagList:", tagList

    # Create recipe structure
    new_recipe = {"title": title,
                  "imgURL": imgURL,
                  "description": description,
                  "yield": yield_,
                  "activeTime": activeTime,
                  "totalTime": totalTime,
                  "ingredientList": ingredientlist,
                  "preparation": preparationSteps,
                  "nutritionInfo": nutritionInfo,
                  "chefNotes": chefNotes,
                  "tags": tagList
                  }

    # return None
    save_recipe([new_recipe])
    return True


if __name__ == "__main__":

    # Recipe list
    recipe_list = []

    start = 778
    stop = start + 10

    for page in range(start, stop):

        print "################# PAGE %d ##################" % (page + 1)

        # Get HTML code for page X
        url = baseURL + pageNumber + str(page + 1)  # Page 1 instead of 0
        print url
        html = urllib.urlopen(url)

        # Feed it to Beautifulsoup
        soup = BeautifulSoup(html, "lxml")

        # Find letter buttons
        blocks = soup.find("div", {"class": "results-group"})

        for child in blocks.children:
            linkToRecipe = child.select(" header > h4 > a")

            if linkToRecipe:
                recipeName = linkToRecipe[0].string
                recipeURL = linkToRecipe[0]['href']
                # print recipeName, recipeURL
                parse_recipe(recipeURL)
                # exit()


