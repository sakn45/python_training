
from selenium.webdriver.support.ui import Select
from model.contact import Contact


class ContactHelper:
    def __init__(self, app):
        self.app = app

    def open_add_new(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("edit.php") and len(wd.find_elements_by_name("submit")) > 0):
            wd.find_element_by_link_text("add new").click()

    def create_new(self, contacts):
        wd = self.app.wd
        self.open_add_new()
        # init contacts  creation
        wd.find_element_by_name("firstname").click()
        self.fill_contact_form(contacts)
        # submit contact creation
        wd.find_element_by_xpath("//div[@id='content']/form/input[21]").click()
        self.contact_cache = None

    def fill_contact_form(self, contact):
        wd = self.app.wd
        self.change_fieled_value("firstname", contact.firstname)
        self.change_fieled_value("middlename", contact.middlename)
        self.change_fieled_value("lastname", contact.lastname)
        self.change_fieled_value("nickname", contact.nickname)
        self.change_fieled_value("title", contact.title)
        self.change_fieled_value("company", contact.company)
        self.change_fieled_value("address", contact.address)
        self.change_fieled_value("home", contact.home_number)
        self.change_fieled_value("mobile", contact.mobile_number)
        self.change_fieled_value("work", contact.work_number)
        self.change_fieled_value("fax", contact.fax)
        self.change_fieled_value("email", contact.email)
        self.change_fieled_value("email2", contact.email2)
        self.change_fieled_value("email3", contact.email3)
        self.change_fieled_value("homepage", contact.homepage)
        self.change_fieled1_value("bday", contact.bday)
        self.change_fieled1_value("bmonth", contact.bmonth)
        self.change_fieled_value("byear", contact.byear)
        self.change_fieled1_value("aday", contact.aday)
        self.change_fieled1_value("amonth", contact.amonth)
        self.change_fieled_value("ayear", contact.ayear)
        self.change_fieled_value("address2", contact.address2)
        self.change_fieled_value("phone2", contact.phone2)
        self.change_fieled_value("notes", contact.notes)

    def change_fieled_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def change_fieled1_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            Select(wd.find_element_by_name(field_name)).select_by_visible_text(text)
            wd.find_element_by_name(field_name).click()

    def delete_first_contact(self):
        self.delete_contact_by_index(0)

    def delete_contact_by_index(self, index):
        wd = self.app.wd
        self.app.open_home_page()
        self.select_contact_by_index(index)
        wd.find_element_by_xpath("//input[@value='Delete']").click()
        wd.switch_to.alert.accept()
        self.contact_cache = None

    def select_contact_by_index(self, index):
        wd = self.app.wd
        wd.find_elements_by_name("selected[]")[index].click()

    def select_first_contact(self):
        wd = self.app.wd
        wd.find_element_by_name("selected[]").click()

    def modify_first_contact(self, index):
        self.modify_contact_by_index(index)

    def modify_contact_by_index(self, index, new_contacts_data):
        wd = self.app.wd
        self.app.open_home_page()
        # open modification form
        wd.find_elements_by_xpath("//img[@alt='Edit']")[index].click()
        self.fill_contact_form(new_contacts_data)
        wd.find_element_by_name("update").click()
        self.return_to_home_page()
        self.contact_cache = None

    def return_to_home_page(self):
        wd = self.app.wd
        wd.find_element_by_link_text("home page").click()

    def count(self):
        wd = self.app.wd
        self.app.open_home_page()
        return len(wd.find_elements_by_name("selected[]"))

    contact_cache = None

    def get_contact_list(self):
        if self.contact_cache is None:
            wd = self.app.wd
            self.app.open_home_page()
            self.contact_cache = []
            for element in wd.find_elements_by_name("entry"):
                cells = element.find_elements_by_tag_name("td")
                firstname = cells[2].text
                lastname = cells[1]
                id = cells[0].find_element_by_name("selected[]").get_attribute("value")
                all_phones = cells[5].text.splitlines()
                self.contact_cache.append(Contact(firstname=firstname, lastname=lastname, id=id,
                                                  home_number=all_phones[0], mobile_number=all_phones[1],
                                                  work_number=all_phones[2], phone2=all_phones[3]))
        return list(self.contact_cache)

    def get_contact_info_from_edit_page(self, index):
        wd = self.app.wd
        self.open_contact_to_edit_by_index(index)
        id = wd.find_element_by_name("id").get_attribute("value")
        firstname = wd.find_element_by_name("firstname").get_attribute("value")
        lastname = wd.find_element_by_name("lastname").get_attribute("value")
        home_number = wd.find_element_by_name("home").get_attribute("value")
        mobile_number = wd.find_element_by_name("mobile").get_attribute("value")
        work_number = wd.find_element_by_name("work").get_attribute("value")
        phone2 = wd.find_element_by_name("phone2").get_attribute("value")
        return Contact(firstname=firstname, lastname=lastname, home_number=home_number, mobile_number=mobile_number, work_number=work_number, phone2=phone2, id=id)

    def open_contact_to_edit_by_index(self, index):
        wd = self.app.wd
        self.app.open_home_page()
        raw = wd.find_elements_by_name("entry")[index]
        cell = raw.find_elements_by_tag_name("td")[7]
        cell.find_element_by_tag_name("a").click()

    def open_contact_view_by_index(self, index):
        wd = self.app.wd
        self.app.open_home_page()
        raw = wd.find_elements_by_name("entry")[index]
        cell = raw.find_elements_by_tag_name("td")[6]
        cell.find_element_by_tag_name("a").click()


