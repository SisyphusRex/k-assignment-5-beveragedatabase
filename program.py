"""Program code"""



# System Imports


# Internal imports.
from beverage import BeverageRepository
from errors import (
    AlreadyImportedError,
    AlreadyCreatedDatabaseError,
    DatabaseNotCreatedError,
)
from user_interface import UserInterface
from utils import CSVProcessor


# Set a constant for the path to the CSV file
PATH_TO_CSV = "./datafiles/beverage_list.csv"


def main(*args):
    """Method to run program"""

    # Create an instance of User Interface class
    ui = UserInterface()

    # Create an instance of the BeverageCollection class.
    # NOTE: renamed
    beverage_repository = BeverageRepository()

    # Create an instance of the CSVProcessor class.
    csv_processor = CSVProcessor()

    # Display the Welcome Message to the user.
    ui.display_welcome_greeting()

    # Display the Menu and get the response. Store the response in the choice
    # integer. This is the 'primer' run of displaying and getting.
    choice = ui.display_menu_and_get_response()

    # While the choice is not exit program
    # NOTE: Modified while choice !=
    while choice != 7:
        if choice == 1:
            # Load the CSV File and create database
            try:
                csv_processor.import_csv(beverage_repository, PATH_TO_CSV)
                ui.display_import_success()
            except AlreadyImportedError:
                ui.display_already_imported_error()
            except FileNotFoundError:
                ui.display_file_not_found_error()
            except EOFError:
                ui.display_empty_file_error()
            except AlreadyCreatedDatabaseError:
                ui.display_already_created_database_error()

        elif choice == 2:
            # Print Entire List Of Items
            try:
                all_item_string = str(beverage_repository)
                if all_item_string:
                    ui.display_all_items(all_item_string)
                else:
                    ui.display_all_items_error()
            except DatabaseNotCreatedError:
                ui.display_database_not_created_error()

        elif choice == 3:
            # Search for an Item

            try:
                search_query = ui.get_search_query()
                item_info = beverage_repository.find_by_id(search_query)
                if item_info:
                    ui.display_item_found(item_info)
                else:
                    ui.display_item_found_error()
            except DatabaseNotCreatedError:
                ui.display_database_not_created_error()

        elif choice == 4:
            # Collect information for a new item and add it to the collection
            try:
                new_item_info = ui.get_new_item_information()
                if beverage_repository.find_by_id(new_item_info[0]) is None:
                    new_beverage = beverage_repository.create_beverage(
                        new_item_info[0],
                        new_item_info[1],
                        new_item_info[2],
                        float(new_item_info[3]),
                        new_item_info[4] == "True",
                    )
                    beverage_repository.add(new_beverage)
                    ui.display_add_beverage_success()
                else:
                    ui.display_item_found_error()
            except DatabaseNotCreatedError:
                ui.display_database_not_created_error()

        elif choice == 5:
            # Update Existing beverage
            try:
                search_query = ui.get_update_query()
                item_to_update = beverage_repository.find_by_id(search_query)
                if item_to_update:
                    update_menu_choice: int = ui.display_update_menu_and_get_response(
                        item_to_update.id
                    )
                    while update_menu_choice != 5:
                        match update_menu_choice:
                            case 1:
                                # update name
                                new_name = ui.get_string_field_public("Name")
                                beverage_repository.update_name(
                                    item_to_update, new_name
                                )
                            case 2:
                                # update pack
                                new_pack = ui.get_string_field_public("Pack")
                                beverage_repository.update_pack(
                                    item_to_update, new_pack
                                )
                            case 3:
                                # update price
                                new_price = ui.get_decimal_field_public("Price")
                                beverage_repository.update_price(
                                    item_to_update, new_price
                                )
                            case 4:
                                # update active
                                new_active = ui.get_bool_field_public("Active")
                                beverage_repository.update_active(
                                    item_to_update, new_active
                                )
                        update_menu_choice = ui.display_update_menu_and_get_response(
                            item_to_update.id
                        )
                else:
                    ui.display_item_found_error()
            except DatabaseNotCreatedError:
                ui.display_database_not_created_error()

        elif choice == 6:
            # Delete Existing Beverage
            try:
                delete_menu_choice = ui.display_delete_menu_and_get_response()
                while delete_menu_choice != 3:
                    match delete_menu_choice:
                        case 1:
                            # delete by id
                            delete_query = ui.get_delete_query()
                            item_to_delete = beverage_repository.find_by_id(
                                delete_query
                            )
                            if item_to_delete:
                                beverage_repository.delete_beverage(item_to_delete)
                                if item_to_delete is None:
                                    ui.display_delete_success()
                                else:
                                    ui.display_delete_failure()
                            else:
                                ui.display_item_found_error()
                        case 2:
                            # delete if inactive
                            beverage_repository.delete_inactive_beverages()
                            inactive_beverage = (
                                beverage_repository.query_for_one_inactive()
                            )
                            if not inactive_beverage:
                                ui.display_delete_success()
                            else:
                                ui.display_delete_failure()
                    delete_menu_choice = ui.display_delete_menu_and_get_response()
            except DatabaseNotCreatedError:
                ui.display_database_not_created_error()
        # Get the new choice of what to do from the user.
        choice = ui.display_menu_and_get_response()
