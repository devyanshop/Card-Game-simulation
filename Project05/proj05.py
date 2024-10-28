######################################################################################################################
#
# CARD GAME SIMULATION-DEVYANSH BHANSALI
#
########################################################################################################################

import csv
from operator import itemgetter
import statistics

"\nFile not Found. Please try again!"

"{'Name'}{'Type'}{'Race'}{'Archetype'}{'TCGPlayer'}"
"{}{}{}{}{}"
"\n{'Totals'}{''}{''}{''}{}"

"\nThe price of the least expensive card(s) is {}"
"\nThe price of the most expensive card(s) is {}"
"\nThe price of the median card(s) is {}"
"\t{}"  # display the cards after the search

"\nInvalid option. Please try again!"
"\nEnter cards file name: "
"\nThere are {} cards in the dataset."
"\nEnter query: "
"\nEnter category to search: "
"\nIncorrect category was selected!"
"\nSearch results"
"\nThere are {} cards with '{}' in the '{}' category."
"\nThere are no cards with '{}' in the '{}' category."
"\nEnter decklist filename: "
"\nThanks for your support in Yu-Gi-Oh! TCG"

MENU = "\nYu-Gi-Oh! Card Data Analysis" \
       "\n1) Check All Cards" \
       "\n2) Search Cards" \
       "\n3) View Decklist" \
       "\n4) Exit" \

CATEGORIES = ["id", "name", "type", "desc", "race", "archetype", "card price"]


def open_file(filename):
    try:
        filePointer = open(filename, "r", encoding="utf-8")
        return filePointer
    except:
        return
   

def read_card_data(filePointer):
    card_dataList = []
    csv_reader = csv.reader(filePointer)
    header_skipped = False

    for row in csv_reader:
        if not header_skipped:
            header_skipped = True
            continue  # Skip the header row
        truncated_name = row[1][:45] if len(row) > 1 else ''
        column_7_float = float(row[6])
        card_row_data = (row[0], truncated_name, row[2], row[3], row[4], row[5], column_7_float)
        card_dataList.append(card_row_data)

    sorted_cardData = sorted(card_dataList, key=lambda x: (x[6], x[1]))
    return sorted_cardData


def read_decklist(filePointer,cardData):
    cardIds = [line.strip() for line in filePointer]
    deck_list = []
    "\nSearch results"
    if cardIds:
        for card_id in cardIds:
            for row in cardData:
                if card_id == row[0]:
                    row_data = tuple(row)
                    deck_list.append(row_data)
    else:
        print(" Error in file access..")
    sorted_deck = sorted(deck_list, key=lambda x: (x[6], x[1]))
    return sorted_deck



def search_cards(cardData, searchQuery, category_index):
    print("\nSearch results")
    data_list = []
    for row in card_data:
        checkStr = row[category_index]
        if (searchQuery in checkStr):
            data_list.append(tuple(row))

    return data_list



def compute_stats(card_data):
    value_list = []

    for row in card_data:
        value_list.append(row[6])

    smallest = value_list[0]
    largest = value_list[0]

    for value in range(0, len(value_list)):
        if (value_list[value] < smallest):
            smallest = value_list[value]
        if (value_list[value] > largest):
            largest = value_list[value]

    midIndex = len(value_list) // 2
    median_value = value_list[midIndex]
    min_cards = []
    max_cards = []
    median_cards= []
    for row in card_data:
        if (float(row[6]) == smallest):
            min_cards.append(tuple(row))
        if (float(row[6]) == largest):
            max_cards.append(tuple(row))
        if (float(row[6]) == median_value):
            median_cards.append(tuple(row))
    min_cards_sorted = sorted(min_cards, key=itemgetter(1))
    max_cards_sorted = sorted(max_cards, key=itemgetter(1))
    median_cards_sorted = sorted(median_cards, key=itemgetter(1))

    return min_cards_sorted, smallest, max_cards_sorted, largest, median_cards_sorted, median_value


    
def display_data(card_data):
    total = 0.0
    count = 1
    print(f"{'Name':<50}{'Type':<30}{'Race':<20}{'Archetype':<30}{'TCGPlayer':<12}")
    for row in card_data:
        print(f"{row[1]:<50}{row[2]:<30}{row[4]:<20}{row[5]:<40}{row[6]:<28,.2f}")
        count = count + 1
        total += row[6]
        if (count > 50):
            break
    print(f"\n{'Totals':<50}{' ':<30}{' ':<20}{' ':<40}{total:<12,.2f}")
    comp_stat = compute_stats(card_data)

    display_stats(comp_stat[0], comp_stat[1], comp_stat[2], comp_stat[3], comp_stat[4], comp_stat[5])

        
def display_stats(min_cards, min_price, max_cards, max_price, median_cards, median_price):
    print(f"\nThe price of the least expensive card(s) is {min_price:.2f}")
    for cardVal in min_cards:
        print("   ", cardVal[1])
    print(f"\nThe price of the most expensive card(s) is {max_price:.2f}")
    for cardVal in max_cards:
        print("   ", cardVal[1])
    print(f"\nThe price of the median card(s) is {median_price:.2f}")
    for cardVal in median_cards:
        print("   ", cardVal[1])
        
def main():
    while True:
        fname = input("\nEnter cards file name: ")
        fp = open_file(fname)
        if (not fp):
            print("\nFile not Found. Please try again!")
        else:
            break

    while True:

        fp = open_file(fname)
        csv_reader1 = csv.reader(fp)

        print(MENU)
        try:
            ch = int(input("Enter option: "))
        except:
            print("\nInvalid option. Please try again!")
            continue
        if (ch == 1):
            dataList = read_card_data(fp)
            print(f"\nThere are {len(dataList)} cards in the dataset.")

            display_data(dataList)
            # print(dataList)

        elif (ch == 2):
            header = next(csv_reader1)
            header_7 = header[:7]
            card_data = read_card_data(fp)
            query = input("\nEnter query: ")
            while True:
                try:
                    category = input("\nEnter category to search: ")
                    category = category.lower()
                    category_index = header_7.index(category)
                    break
                    print("\nIncorrect category was selected!")
                except:
                    print("\nIncorrect category was selected!")

            data_list_Search = search_cards(card_data, query, category_index)
            if data_list_Search == []:
                print(f"\nThere are no cards with '{query}' in the '{CATEGORIES[category_index]}' category.")
            else:
                print(f"\nThere are {len(data_list_Search)} cards with '{query}' in the '{CATEGORIES[category_index]}' category.")
                display_data(data_list_Search)
        elif (ch == 3):
            card_data = read_card_data(fp)
            ydk_fname = input("\nEnter decklist filename: ")
            try:
                ydk_file = open(ydk_fname, 'r')
                d_List = read_decklist(ydk_file, card_data)
                display_data(d_List)
            except FileNotFoundError:
                print(f"Error: File '{ydk_fname}' not found.")

        elif (ch == 4):
            print("\nThanks for your support in Yu-Gi-Oh! TCG")
            break
        else:
            print("\nInvalid option. Please try again!")
            continue


if __name__ == '__main__':
    main()
    

