#       CODED BY:
# Muhammad Ali CS-103
# Abdul Basit CS-105
# Anshara Ayaz CS-083
# Aymen Fatima CS-053

import sys
from abc import ABC, abstractmethod
from datetime import datetime
from tkinter import *

def interface():
    """This function is driver code of this app"""
    while True:
        print('-'*80)
        print('\t\t\t\t\tWELCOME TO SHOPPING PLEX')
        print('-'*80)
        print('Select from following')
        print('\t1) CUSTOMER\n\t2) ADMIN\n\t3) EXIT')
        select = input('Enter your choice: ')

        if select == '1':
            user = Customer()  # creating customer class object
        elif select == '2':
            user = Admin()    # creating admin class object
        elif select == '3':
            sys.exit()
        else:
            print('Enter the correct option number !!\n')
            continue

# --------------------------------------------------------------------------------------------------------------

class User(ABC):
    """An abstract class for the user"""
    def __init__(self):
        """Takes input user id and password of the user"""
        print('\t\tLOGIN YOUR ACCOUNT')
        self.user_id = input('Enter your id: ')
        self.password = input('Enter your password: ')

    @abstractmethod
    def verify_login(self):
        """An Abstract method
        Redefined in child classes to verify the login credentials"""
        pass

# --------------------------------------------------------------------------------------------------------------

class Customer(User):
    """Class for user entered as CUSTOMER, provides all the functionality of the shopping app,
    also allow customer to start shopping, check previous purchases, viewing and updating profile and much more"""
    def __init__(self):
        self.checkout = Order()    # Composition - making order class object
        select = input('\nDo you have an account?? (Y/N): ')
        if select.lower() == 'y':
            super().__init__()
            self.acc_info = self.verify_login()
            if self.acc_info[0] == True:
                self.what_to_do()
            else:
                print(f'ACCOUNT WITH USER NAME {self.user_id} NOT FOUND'
                      f'\nPLEASE CREATE YOUR ACCOUNT or YOU MIGHT ENTER WRONG')
        elif select.lower() == 'n':
            self.create_account()

    def verify_login(self):
        """This method checks for customer's login credentials from the registered customers file"""
        with open('customers_info.txt') as f:
            for line in f:
                line = line.strip()
                info = eval(line)
                if info['user_id'] == self.user_id and info['password'] == self.password:
                    return True, info
            else:
                return False, False

    def create_account(self):
        """This method is for creating account for new customers"""
        while True:
            print('\t\tCREATE YOUR ACCOUNT')
            self.userid = input('Enter your id: ')
            a = 0
            with open('customers_info.txt') as f:   # checks for the entered user_id belongs to other customer
                for info in f:                      # or not, just because each customer have unique user_id
                    info = eval(info)
                    if info['user_id'] == self.userid:
                        print('User with this user id already exists')
                        a = 1
                        break
            if a == 1:
                continue

            self.password = input('Enter your password: ')
            self.fname = input('Enter your first name: ')
            self.lname = input('Enter your last name: ')
            self.email = input('Enter your email: ')
            self.phone = input('Enter your phone: ')
            self.address = input('Enter your address: ')

            if self.password == '' or self.fname == '' or self.lname == '' or self.email == '' or self.phone == '' or self.address == '':
                print('Please Enter all the information !!')
                continue

            print('\t\tSUCCESSFULLY CREATED YOUR ACCOUNT')
            break

        with open('customers_info.txt', 'a') as f:
            f.write(str({'user_id': self.userid, 'password': self.password, 'first name': self.fname,
                         'last name': self.lname, 'address': self.address, 'email': self.email,
                         'phone': self.phone}) + '\n')

        with open('cust_names.txt', 'a') as q:
            q.write(self.userid+',')

        with open('cust_carts.txt', 'a') as p:
            p.write(str([self.userid, []])+'\n')

    def what_to_do(self):
        """This method displays a customer menu and function according to given input"""
        while True:
            print(f'\n\t HELLO {self.user_id}')
            print('Select from following options !')
            print('\t1) START SHOPPING\n\t2) CHECK PREVIOUS HISTORY\n\t3) VIEW ACCOUNT INFO\n\t4) CHANGE ACCOUNT INFO'
                  '\n\t5) BACK')
            select = input('What you want to do?? ')
            if select == '1':
                self.customer_cart = Cart(self.user_id)  # Composition - creating Cart class object
            elif select == '2':
                self.checkout.display_history(self.user_id)
            elif select == '3':
                self.view_account()
                back = input('Press any key to go back ')
            elif select == '4':
                self.change_credentials()
            elif select == '5':
                break
            else:
                print('Please Enter correct option number !!!')
                continue

    def view_account(self):
        """This method is for displaying customer's account details"""
        print('\nYour account details are:')
        n = 1
        for i in self.acc_info[1]:
            print(f'{n}) {i.upper():10} : {self.acc_info[1][i]}')
            n += 1

    def change_credentials(self):
        """This method is for changing account's info of the customer"""
        self.all_cust = []
        keys = list(self.acc_info[1].keys())
        with open('customers_info.txt') as f:
            for line in f:
                line = eval(line)
                if line['user_id'] != self.user_id:
                    self.all_cust.append(line)

        self.view_account()
        while True:
            try:
                ask = int(input('Enter what you want to update (alpha keys to go back): '))
                assert ask > 0
                if ask == 1:
                    print('User ID cannot be updated')
                    continue
                new = input(f'Enter new {keys[ask-1].upper()} : ')
                self.acc_info[1][keys[ask-1]] = new
                self.all_cust.append(self.acc_info[1])
                back = input('Press any key to go back ')
                break
            except ValueError:
                break
            except:
                print('Something Went Wrong !!\n')
                continue

        with open('customers_info.txt', 'w') as p:
            for item in self.all_cust:
                p.write(str(item)+'\n')

# ---------------------------------------------------------------------------------------------------------------

class Admin(User):
    """Class for user entered as ADMIN, manages the shopping app by adding/removing items, change price/stock,
    viewing customer's history and launching discount on special events"""
    def __init__(self):
        super().__init__()
        self.acc_info = self.verify_login()
        self.ord = Order()            # Composition - making order class object
        if self.acc_info[0] == True:
            self.what_to_do()
        else:
            print(f'WRONG CREDENTIALS..CANNOT ACCESS ADMIN')

    def verify_login(self):
        """This method checks for admin login credentials from the admin info file"""
        with open('admin_info.txt') as f:
            for line in f:
                line = line.strip()
                info = eval(line)
                if info['user_id'] == self.user_id and info['password'] == self.password:
                    return True, info
            else:
                return False, False

    def what_to_do(self):
        """Display an admin menu and function according to given input"""
        while True:
            self.prod = Products()     # Composition - making Product class object

            print(f'\n\t HELLO ADMIN ({self.user_id})')
            print('Select from following options !')
            print('\t1) DISPLAY PRODUCTS\n\t2) ADD NEW ITEMS\n\t3) REMOVE ITEMS\n\t4) ADD OR REMOVE STOCK\n\t'
                  '5) CHANGE PRICE OF ITEMS\n\t6) CHECK HISTORY AND SALES\n\t7) LAUNCH SALE/DISCOUNT\n\t8) BACK')
            select = input('What you want to do?? ')
            if select == '1':
                self.show_categories()
                back = input('Press any key to go back ')
            elif select == '2':
                self.show_categories()
                self.add_items()
            elif select == '3':
                self.show_categories()
                self.remove_items()
            elif select == '4':
                self.show_categories()
                self.add_stock()
            elif select == '5':
                self.show_categories()
                self.change_price()
            elif select == '6':
                self.ord.show_all_sales()
            elif select == '7':
                self.ord.apply_discount()
            elif select == '8':
                break
            else:
                print('Please Enter correct option number !!!')
                continue

    def show_categories(self):
        """This method display product categories and get the product details of the entered category"""
        while True:
            print('\nPlease select from the following categories')
            print('\t1) FRUITS AND VEGETABLES\n\t2) FAST FOOD\n\t3) ELECTRONIC ITEMS\n\t4) GARMENTS')

            select = input('Select the category: ')
            if select == '1':
                self.currentlist = self.prod.get_fruits_veg()
                self.prod.display_products(self.currentlist[0])
                break
            elif select == '2':
                self.currentlist = self.prod.get_fastfood()
                self.prod.display_products(self.currentlist[0])
                break
            elif select == '3':
                self.currentlist = self.prod.get_elec_items()
                self.prod.display_products(self.currentlist[0])
                break
            elif select == '4':
                self.currentlist = self.prod.get_garments()
                self.prod.display_products(self.currentlist[0])
                break
            else:
                print('Please Enter correct option number !!!')

    def add_items(self):
        """This method is for adding new item in the product list"""
        lst = self.currentlist[0]
        filename = self.currentlist[1]
        while True:
            try:
                print()
                name = input('Enter product name: ')
                price = int(input('Enter product price: '))
                quantity = int(input('Enter product quantity: '))
                if name == '' or price == '' or quantity == '':
                    print('\n\tEnter Correct Details !!\n')
                    continue
                lst.append([name, price, quantity])
            except ValueError:
                print('Please Enter Integer !!!!!!\n')
                continue
            except:
                print('Something went wrong...TRY AGAIN\n')
                continue

            ask = input('Do you want to ADD more products (Y/N): ')
            if ask.lower() == 'y':
                continue
            else:
                print('\t\tProducts Added successfully')

            with open(filename, 'w') as f:
                for i in lst:
                    f.write(str(i[0]) + ',' + str(i[1]) + ',' + str(i[2]) + '\n')
            break

    def remove_items(self):
        """This method is for permanently removing an item from the product list"""
        lst = self.currentlist[0]
        filename = self.currentlist[1]
        while True:
            try:
                id = int(input('Enter ID of Product you want to Remove: '))
                if 0 < id <= len(lst):
                    lst.pop(id-1)
                else:
                    print('Enter Correct Product ID\n')
                    continue
            except ValueError:
                print('Please Enter Integer !!!!!!\n')
                continue
            except:
                print('Something went wrong...TRY AGAIN\n')
                continue

            print('\t\tPRODUCT REMOVED !!')

            with open(filename, 'w') as f:
                for i in lst:
                    f.write(i[0] + ',' + i[1] + ',' + str(i[2]) + '\n')
            break

    def add_stock(self):
        """This method is for changing/updating stock of the particular product"""
        lst = self.currentlist[0]
        filename = self.currentlist[1]
        while True:
            try:
                id = int(input('Enter Product ID whose Stock you want to update: '))
                if 0 < id <= len(lst):
                    stock = int(input('Enter New Stock: '))
                    if stock < 0:
                        print('Enter Correct Value of Stock\n')
                        continue
                    else:
                        lst[id-1][2] = stock
                else:
                    print('Enter Correct Product ID\n')
                    continue
            except ValueError:
                print('Please Enter Integer !!!!!!\n')
                continue
            except:
                print('Something went wrong...TRY AGAIN\n')
                continue

            ask = input('Do you want to change more stocks (Y/N): ')
            if ask.lower() == 'y':
                continue
            else:
                print('\t\tSTOCK UPDATED !!')

            with open(filename, 'w') as f:
                for i in lst:
                    f.write(i[0] + ',' + i[1] + ',' + str(i[2]) + '\n')
            break

    def change_price(self):
        """This method is for changing price of the particular product"""
        lst = self.currentlist[0]
        filename = self.currentlist[1]
        while True:
            try:
                print()
                id = int(input('Enter Product ID whose Price you want to update: '))
                if 0 < id <= len(lst):
                    price = int(input('Enter new Price: '))
                    if price < 0:
                        print('Enter Correct Price\n')
                        continue
                    else:
                        lst[id-1][1] = price
                else:
                    print('Enter Correct Product ID\n')
                    continue
            except ValueError:
                print('Please Enter Integer !!!!!!\n')
                continue
            except:
                print('Something went wrong...TRY AGAIN\n')
                continue

            ask = input("Do you want to change more Product's price (Y/N): ")
            if ask.lower() == 'y':
                continue
            else:
                print('\t\tPRICE UPDATED !!')

            with open(filename, 'w') as f:
                for i in lst:
                    f.write(i[0] + ',' + str(i[1]) + ',' + str(i[2]) + '\n')
            break

# -----------------------------------------------------------------------------------------------------------

class Cart:
    """Class for managing customer's shopping cart, displaying products, add items to cart, remove from cart,
     placing order and saving cart when order is not placed"""
    def __init__(self, userid):
        self.checkout = Order()     # Composition - making order class object
        self.user_name = userid
        self.my_cart = []
        self.current_list = []
        with open('cust_carts.txt') as f:
            for line in f:
                cart = line.strip()
                cart = eval(cart)
                if cart[0] == self.user_name:
                    self.my_cart = cart[1]
                    break

        self.add_to_cart()

    def show_categories(self):
        """This method display a shopping menu and function according to given input"""
        while True:
            print('\nPlease select from the following categories')
            print('\t1) FRUITS AND VEGETABLES\n\t2) FAST FOOD\n\t3) ELECTRONIC ITEMS\n\t'
                  '4) GARMENTS\n\t5) VIEW CART\n\t6) PLACE ORDER\n\t7) EXIT')

            select = input('Select the category: ')
            if select == '1':
                self.current_list = self.prod.get_fruits_veg()
                self.prod.display_products(self.current_list[0])
                break
            elif select == '2':
                self.current_list = self.prod.get_fastfood()
                self.prod.display_products(self.current_list[0])
                break
            elif select == '3':
                self.current_list = self.prod.get_elec_items()
                self.prod.display_products(self.current_list[0])
                break
            elif select == '4':
                self.current_list = self.prod.get_garments()
                self.prod.display_products(self.current_list[0])
                break
            elif select == '5':
                self.view_cart()
            elif select == '6':
                self.place_order()
            elif select == '7':
                self.update_cart()

    def add_to_cart(self):
        """This method add selected product into the customer's cart"""
        self.prod = Products()       # Composition - making Product class object
        self.show_categories()
        prod_info = self.current_list
        products = prod_info[0]
        filename = prod_info[1]
        while True:
            try:
                print()
                ask = int(input('Enter the product no. you want to add in cart: '))
                if ask > len(products) or ask < 1:
                    print('\nPlease Enter the correct Product ID !!')
                else:
                    quantity = int(input('Enter quantity you want to buy: '))
                    selected = products[ask-1]
                    if int(selected[2]) < quantity:
                        print(f'\n\t{selected[0].upper()} Out of Stock !!')
                    else:
                        selected[2] = int(selected[2]) - quantity
                        total = int(selected[1]) * quantity
                        for i in self.my_cart:
                            if i[0] == selected[0]:
                                i[2] += quantity
                                i[3] += total
                                break
                        else:
                            self.my_cart.append([selected[0], int(selected[1]), quantity, total])

            except ValueError:
                print('\nPlease Enter Integer !!!!!!')
                continue
            except:
                print('\nSomething went wrong...TRY AGAIN')
                continue

            with open(filename, 'w') as f:
                for i in products:
                    f.write(i[0] + ',' + i[1] + ',' + str(i[2]) + '\n')

            select = input('\nDo you want to buy more products (Y/N) ')
            if select.lower() == 'y':
                continue
            else:
                self.add_to_cart()

    def view_cart(self):
        """This method is for viewing current cart items of the customer"""
        print(' ' * 20, '<<<<< YOUR CART >>>>>')
        if len(self.my_cart) == 0:
            print("\tEMPTY CART !!\n\tYou didn't add any item in cart...")
            go = input('Press any key to go back ')

        else:
            print('-' * 80)
            q = ['S.no', 'NAME', 'PRICE', 'QUANTITY', 'TOTAL']
            print(f'{q[0]:>2} :\t {q[1].upper():32}',
                  f'{q[2]:12} {q[3]:14} {q[4]}')
            print('-' * 80)

            n = 1
            for items in self.my_cart:
                print(f'{n:>2} :\t {items[0].upper():32}',
                      f'{str(items[1]):12} {str(items[2]):14} {str(items[3])}')
                n += 1
            print('-' * 80)
            print()
            back = input('Do you want to remove any product from cart (Y/N) : ')
            if back.lower() == 'y':
                self.remove_from_cart()

    def remove_from_cart(self):
        """This method is for removing products from the cart"""
        self.prod2 = Products()
        while True:
            try:
                no = int(input('Enter S.no of product you want to remove: '))
                assert no > 0
                a = self.my_cart.pop(int(no)-1)
                break
            except ValueError:
                print('Please Enter Integer !!!!!!\n')
            except Exception:
                print('Please enter correct S.no\n')

        l1 = self.prod2.get_fruits_veg()
        l2 = self.prod2.get_fastfood()
        l3 = self.prod2.get_elec_items()
        l4 = self.prod2.get_garments()
        all_list = [l1[0], l2[0], l3[0], l4[0]]

        for i in all_list:      # checking for the removed item in all the product lists
            for item in i:
                if item[0] == a[0]:
                    item[2] = int(item[2])+a[2]
                    break

        all_files = [l1[1], l2[1], l3[1], l4[1]]
        for j in range(len(all_files)):
            with open(all_files[j], 'w') as p:    # writing back all the lists in the file
                for k in all_list[j]:
                    p.write(k[0] + ',' + k[1] + ',' + str(k[2]) + '\n')

    def place_order(self):
        """This method is for placing order of items in the customer's cart"""
        ask = input('CONFIRM !! Do you want to Place Order !! (y/n): ')
        if ask.lower() == 'y':
            if len(self.my_cart) == 0:
                print('\tYour Cart is EMPTY !!!!')
                go = input('Press any key to go back ')
            else:
                all_carts = []
                with open('cust_carts.txt') as f:
                    for line in f:
                        line = line.strip()
                        cart = eval(line)
                        all_carts.append(cart)
                for i in all_carts:
                    if i[0] == self.user_name:
                        i[1] = []
                        break
                with open('cust_carts.txt', 'w') as p:
                    for line in all_carts:
                        p.write(str(line) + '\n')

                while True:
                    try:
                        payment = input('Mode of PAYMENT\n1) CASH ON DELIVERY\t 2) CREDIT CARD'
                                        '\t 3) E-WALLET\nEnter Payment Method: ')
                        address = input('Enter the DELIVERY ADDRESS: ')
                        if payment == '' or address == '':
                            raise Exception
                        ask = input('Press Enter to Get RECEIPT ')
                        self.checkout.create_bill(self.user_name, self.my_cart, address)
                        interface()

                    except Exception:
                        print('Please enter correct details !!\n')

    def update_cart(self):
        """This method saves the customer's cart when he/she exits the app without placing order"""
        ask = input('DO REALLY WANT TO EXIT WITHOUT PLACING ORDER..YOUR CART WILL REMAIN STORED?? (Y/N): ')
        if ask.lower() == 'y':
            all_carts = []
            with open('cust_carts.txt') as f:
                for line in f:
                    line = line.strip()
                    cart = eval(line)
                    all_carts.append(cart)

            for i in all_carts:
                if i[0] == self.user_name:
                    i[1] = self.my_cart
                    break
            with open('cust_carts.txt', 'w') as p:
                for line in all_carts:
                    p.write(str(line) + '\n')

            interface()

# --------------------------------------------------------------------------------------------------------------

class Order:
    """Class for manage customer's orders, generating bill of the order and updating and displaying
    history of previous orders"""
    discount = 0

    def __init__(self):
        self.history = []
        self.full_history = []

    def create_bill(self, username, lst, address):
        """This method is for creating bill/receipt of the customer's order, a beautiful GUI will appear on the screen
        having all the products listed with all the information"""
        total_amount = 0
        for items in lst:
            total_amount += items[3]
        a = datetime.now()
        cart = [username, a.strftime('%d-%b-%Y--%I:%M:%S %p'), lst, total_amount]
        self.update_history(cart)

        # GUI code for Receipt
        root = Tk()
        root.geometry('550x730+600+4')
        root.resizable(False, False)
        root.title('BILL RECEIPT')
        root.attributes('-topmost', True)

        Label(root, text='WELCOME TO SHOPPING PLEX', font='Courier 20 bold').pack(pady=(12, 0))
        Label(root, text='Address : Karachi \t Telephone : 111 468 429', font='System').pack(pady=(0, 6))
        Label(root, text=f'User ID : {cart[0].upper()}', font='times 12').pack(anchor=W, padx=22)
        Label(root, text=f'Date and Time : {cart[1]}', font='times 12').pack(anchor=W, padx=22)
        Label(root, text=f'Delivery Address : {address.upper()}', font='times 12').pack(anchor=W, padx=22)
        Label(root, text='*' * 100).pack()

        Label(root, text='Original Receipt', font='Courier 16 bold').pack()
        Label(root, text='*' * 100).pack()

        Label(root, text='  S.No\tPRODUCTS\t\t\tPRICE\tQUANTITY\tTOTAL', font='arial 10 bold').pack(padx=(0, 60))
        Label(root, text='-' * 100).pack()

        prod_frame = Frame(root)
        prod_frame.pack(fill=BOTH, expand=1)

        p_canvas = Canvas(prod_frame)
        p_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        scroll = Scrollbar(prod_frame, orient=VERTICAL, command=p_canvas.yview)
        scroll.pack(side=RIGHT, fill=Y)

        p_canvas.configure(yscrollcommand=scroll.set)
        p_canvas.bind('<Configure>', lambda e: p_canvas.configure(scrollregion=p_canvas.bbox('all')))

        inner_frame = Frame(p_canvas, height=1000, width=1000)
        p_canvas.create_window((0, 0), window=inner_frame, anchor='nw')

        quantity = 0
        y = 10
        a = 1
        for i in cart[2]:
            Label(inner_frame, text=a).place(x=15, y=y)
            Label(inner_frame, text=i[0].upper()).place(x=50, y=y)
            Label(inner_frame, text=i[1]).place(x=280, y=y)
            Label(inner_frame, text=i[2]).place(x=360, y=y)
            Label(inner_frame, text=i[3]).place(x=460, y=y)
            y += 20
            a += 1
            quantity += int(i[2])

        b1 = Button(text='Exit', relief=GROOVE, bg='light grey', borderwidth=4, command=lambda: root.destroy())
        b1.pack(side=BOTTOM, pady=(0, 6), ipadx=16, fill=X)
        Label(text='For Return and Exchange Policy visit Website\nwww.shoppingplex.com', font='times 12').pack(
            side=BOTTOM, fill=X)
        Label(text='-' * 100).pack(side=BOTTOM, fill=X)
        Label(text='|!||' * 12, font='arial 14 bold').pack(side=BOTTOM, fill=X)
        Label(text=f'INVOICE VALUE : Rs {cart[-1]-(cart[-1]*(round(self.discount/100, 4)))}', font='Courier 14 bold')\
            .pack(side=BOTTOM, fill=X)
        Label(text=f'Total Items : {quantity}\t\tDiscount : {self.discount}%', font='times 13 bold')\
            .pack(side=BOTTOM, fill=X)
        Label(text='-' * 100).pack(side=BOTTOM, fill=X)

        root.mainloop()

    @staticmethod
    def update_history(cart):
        """Update history of the customer by writing the current order in the file"""
        with open('history.txt', 'a') as f:
            f.write(str(cart)+'\n')

    def display_history(self, username):
        """This method display all the previous purchases/orders of the customer with all information"""
        self.history = []
        with open('history.txt') as f:
            for line in f:
                line = line.strip()
                history = eval(line)
                if history[0] == username:
                    self.history.append(history)

        if len(self.history) == 0:
            print('Did not bought anything yet\n')
            back = input('Press any key to go back ')
        else:
            for i in self.history:
                print()
                print(f'\t\t\tUSER NAME : {i[0]}\t\t\tDATE and TIME : {i[1]}')
                q = ['S.no', 'NAME', 'PRICE', 'QUANTITY', 'TOTAL']
                print('-' * 80)
                print(f'{q[0]:>2} :\t {q[1].upper():32}',
                      f'{q[2]:12} {q[3]:14} {q[4]}')
                n = 1
                print('-' * 80)
                for items in i[2]:
                    print(f'{n:>2} :\t {items[0].upper():32}',
                          f'{str(items[1]):12} {str(items[2]):14} {str(items[3])}')
                    n += 1
                print('-' * 80)
                print(f'\t\tTOTAL BILL : Rs {i[3]}/=')
                print()

            print('Total Orders Placed :', len(self.history))
            back = input('\nPress any key to go back ')

    def show_all_sales(self):
        """This method is for admin to display all customer's previous purchases/orders"""
        with open('cust_names.txt') as p:
            cust = p.read()
            cust_list = cust.strip(',')
            cust_list = cust_list.split(',')

        print('\t\tCUSTOMERS INFO AND SALES')
        print('Total Customers Registered:', len(cust_list))
        for i in range(1, len(cust_list)+1):
            print(f'\t{i}) {cust_list[i-1].upper()}')

        while True:
            try:
                ask = int(input('Enter Customer no to view its history : '))
                if ask <= 0:
                    raise Exception
                self.display_history(cust_list[ask - 1])
                break

            except ValueError:
                print('Please Enter Integers...\n')
                continue
            except Exception:
                print('Something Went Wrong..\n')
                continue

    @staticmethod
    def apply_discount():
        """This method is for admin to launch discount/sale, discount will be applied on the final total"""
        while True:
            try:
                Order.discount = int(input('Enter the percentage of discount you want to apply: '))
                break
            except ValueError:
                print('Please enter integers !!!\n')
                continue
            except:
                print('Something went wrong !!\n')
                continue

# ----------------------------------------------------------------------------------------------------------------

class Products:
    """Class for managing products of the store, main functionality is to read product items from the files
    and display items in proper format"""
    def __init__(self):
        self.fruits_vegetables = []
        self.fast_food = []
        self.elec_items = []
        self.garments = []

    @staticmethod
    def display_products(prod_list):
        """Display products of the chosen category in the proper and readable format"""
        print('-'*75)
        q = ['ID', 'NAME', 'PRICE', 'QUANTITY']
        print(f'{q[0]:>2} :\t {q[1].upper():32}',
              f'{q[2]:10} {q[3]}')
        print('-'*75)
        n = 1
        for items in prod_list:
            print(f'{n:>2} :\t {items[0].upper():32}',
                  f'{items[1]:10} {items[2]}')
            n += 1
        print('-'*75)

    def get_fruits_veg(self):
        """This method open fruits_vegetables file, read items and store it in fruit_vegetables list"""
        with open('fruits_vegetables.txt') as f:
            for line in f:
                line = line.strip()
                self.fruits_vegetables.append(line.split(','))
        return self.fruits_vegetables, 'fruits_vegetables.txt'

    def get_fastfood(self):
        """This method open fast_food file, read items and store it in fast food list"""
        with open('fast_food.txt') as h:
            for line in h:
                line = line.strip()
                self.fast_food.append(line.split(','))
        return self.fast_food, 'fast_food.txt'

    def get_elec_items(self):
        """This method open electronics_items file, read items and store it in electronics items list"""
        with open('electronics_items.txt') as h:
            for line in h:
                line = line.strip()
                self.elec_items.append(line.split(','))
        return self.elec_items, 'electronics_items.txt'

    def get_garments(self):
        """This method open garments file, read items and store it in garments list"""
        with open('garments.txt') as h:
            for line in h:
                line = line.strip()
                self.garments.append(line.split(','))
        return self.garments, 'garments.txt'

interface()
